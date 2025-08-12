import os

from pyrogram import filters
from pyromod import Client
from pyrogram.types import CallbackQuery
from pyrogram.types import Message, ForceReply
from pyromod.exceptions import ListenerTimeout, ListenerStopped
import globals.messages as messages
from helpers.Upload_Download.downloader.FirstUrl import FirstUrl
from helpers.Upload_Download.downloader.ReadyToDownload import ReadyToDownload
from globals.database import bd
from asyncio import create_task
from helpers.Upload_Download.components import generate_rename_or_not_button, add_prefix_suffix, parse_caption
from globals.data_ground import UserData

async def background_download_and_upload(bot: Client, file_data : ReadyToDownload):
    """
    Fonction pour télécharger un fichier en arrière-plan et l'envoyer à l'utilisateur.
    """
    chat_id = file_data.chat_id
    custom_thumbnail, download_result, custom_caption, prefix, sufix = None, None, None, None, None
    try:
        utils = await bd.get_user_download_utils(chat_id)   #Récupere toutes les données utiles pour le téléchargement
        prefix = utils['prefix']
        sufix = utils['suffix']
        file_name = file_data.filename

        #Ajout du préfixe et du suffixe personnalisé au nom du fichier
        file_data.filename = add_prefix_suffix(file_name, prefix, sufix)

        download_result = await file_data.download_file(
            bot,
            chat_id
        )
        if not download_result.success:
            await bot.send_message(
                chat_id,
                messages.DOWNLOAD_FAILED.format(download_result.error)
            )
            return


        custom_thumbnail = utils['thumbnail']
        custom_caption = utils['caption']
        if custom_caption:
            custom_caption = await parse_caption(file_data, custom_caption)
        if custom_thumbnail:
            try:
                custom_thumbnail = await bot.download_media(custom_thumbnail)
            except:
                custom_thumbnail = None  # Si la miniature personnalisée échoue, on la met à None
                pass
        upload_result = await download_result.upload_file(
            bot,
            caption=custom_caption,
            thumbnail=custom_thumbnail,  # Vous pouvez spécifier une miniature si nécessaire
        )
        if not upload_result.success:
            await bot.send_message(
                chat_id,
                messages.UPLOAD_FAILED.format(upload_result.error),
            )
            return
    except Exception as e:
        await bot.send_message(
            chat_id,
            messages.ERROR_OCCURRED.format(str(e)),
        )
    finally:
        # Nettoyage des données de téléchargement de l'utilisateur
        if download_result:
            if os.path.exists(download_result.file_path):
                os.remove(download_result.file_path)
        if custom_thumbnail:
            if os.path.exists(custom_thumbnail):
                os.remove(custom_thumbnail)
        await UserData.remove_download(chat_id)  # Nettoyage des données de téléchargement de l'utilisateur



async def detect_link(_ , message: Message):
    """
    Fonction pour détecter un lien dans un message et lancer le téléchargement du fichier associé.
    """
    first_msg = await message.reply_text(
        messages.DETECTING_LINK,
        reply_to_message_id=message.id
    )
    user_id = message.chat.id
    # Vérification si l'utilisateur est déjà en train de télécharger un fichier
    if await UserData.in_downloads(user_id):
        await first_msg.edit_text(
            messages.ALREADY_IN_DOWNLOAD
        )
        return
    link = message.text.strip()
    if not link:
        await first_msg.edit_text(
            messages.NO_LINK_DETECTED
        )
        return

    # Vérification si le lien est valide
    file_data = FirstUrl(link, user_id)
    try:
        file_data = await file_data.get_file_infos()
        file_size = file_data.file_size
        if file_size > 2000 * 1024 * 1024:  # Limite de 2 Go pour les bots Telegram
            await first_msg.edit_text(
                messages.FILE_TOO_LARGE
            )
            return

        # Enregistrement de l'utilisateur dans les téléchargements
        await UserData.add_download(user_id, file_data)

        await first_msg.edit_text(
            messages.FILE_READY_TO_DOWNLOAD.format(
                f"<a href='{file_data.file_download_url}'>lien</a>",
                file_data.filename_with_ext,
                f"{file_data.file_size_human if file_size > 0 else 'unknown'} Mo"
            ),
            reply_markup=generate_rename_or_not_button()
        )
    except ValueError as e:
        await first_msg.edit_text(
            e.__str__()
        )
        return
    except Exception as e:
        await UserData.remove_download(user_id)
        await first_msg.edit_text(
            messages.ERROR_OCCURRED.format(str(e))
        )

async def rename_file(bot : Client, update: CallbackQuery):
    """
    Fonction pour renommer un fichier avant de le télécharger.
    """
    user_id = update.from_user.id
    try:
        await update.message.delete()
        file_data = await UserData.get_download(user_id)

        if not file_data:
            await bot.send_message(
                user_id,
                messages.FILE_NOT_FOUND,
            )
            return
        new_name_message = await bot.ask(
            chat_id=user_id,
            text=messages.ASK_NEW_FILENAME.format(file_data.filename_with_ext),
            reply_to_message_id=update.message.id,
            reply_markup=ForceReply(placeholder=messages.NEW_FILENAME_PLACEHOLDER),
            filters=filters.text,
            timeout=1800  # Timeout de 30 minutes pour la réponse
            )

        new_filename = new_name_message.text.strip()
        if not await UserData.update_download_name(user_id, new_filename):
            await UserData.remove_download(user_id)
            return
        file_new_data = await UserData.get_download(user_id)

        create_task(background_download_and_upload(bot, file_new_data))
    except (ListenerTimeout, ListenerStopped):
        await bot.send_message(
            user_id,
            messages.RENAME_TIMEOUT,
        )
        await UserData.remove_download(user_id)
    except Exception as e:
        await bot.send_message(
            user_id,
            messages.ERROR_OCCURRED.format(str(e)),
        )
        await UserData.remove_download(user_id)
        return


async def download_file(bot: Client, update: CallbackQuery):
    """
    Fonction pour démarrer le téléchargement d'un fichier sans renommer.
    """
    await update.message.delete()

    user_id = update.from_user.id
    file_data = await UserData.get_download(user_id)

    if not file_data:
        await bot.send_message(
            user_id,
            messages.FILE_NOT_FOUND
        )
        return

    create_task(background_download_and_upload(bot, file_data))

async def download_cancel(_, update: CallbackQuery):
    await update.message.edit_text("Téléchargement annulé✅")

    # Suppression des données de téléchargement de l'utilisateur
    await UserData.remove_download(update.from_user.id)















