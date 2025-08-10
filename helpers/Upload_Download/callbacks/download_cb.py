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
from helpers.Upload_Download.components import generate_rename_or_not_button
from globals.data_ground import UserData

async def background_download_and_upload(bot: Client, file_data : ReadyToDownload):
    """
    Fonction pour télécharger un fichier en arrière-plan et l'envoyer à l'utilisateur.
    """
    chat_id = file_data.chat_id
    download_result = None
    try:

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

        custom_thumbnail = await bd.get_user_thumbnail(chat_id)   # Récupération de la miniature personnalisée de l'utilisateur

        upload_result = await download_result.upload_file(
            bot,
            caption=file_data.filename_with_ext,
            thumbnail=custom_thumbnail  # Vous pouvez spécifier une miniature si nécessaire
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
        await UserData.remove_download(chat_id)  # Nettoyage des données de téléchargement de l'utilisateur



async def detect_link(bot : Client, message: Message):
    """
    Fonction pour détecter un lien dans un message et lancer le téléchargement du fichier associé.
    """
    user_id = message.chat.id
    # Vérification si l'utilisateur est déjà en train de télécharger un fichier
    if await UserData.in_downloads(user_id):
        await bot.send_message(
            user_id,
            messages.ALREADY_IN_DOWNLOAD,
            reply_to_message_id=message.id
        )
        return

    link = message.text.strip()
    if not link:
        return
    file_data = FirstUrl(link, user_id)
    try:
        file_data = await file_data.get_file_infos()
        file_size = file_data.file_size
        if file_size > 2000 * 1024 * 1024:  # Limite de 2 Go pour les bots Telegram
            await bot.send_message(
                user_id,
                messages.FILE_TOO_LARGE,
                reply_to_message_id=message.id
            )
            return
        # Enregistrement de l'utilisateur dans les téléchargements
        await UserData.add_download(user_id, file_data)

        await bot.send_message(
            user_id,
            messages.FILE_READY_TO_DOWNLOAD.format(
                f"<a href='{file_data.file_download_url}'>lien</a>",
                file_data.filename_with_ext,
                f"{file_data.file_size_human if file_size > 0 else 'unknown'} Mo"
            ),
            reply_to_message_id=message.id,
            reply_markup=generate_rename_or_not_button()
        )
    except ValueError as e:
        await bot.send_message(
            user_id,
            e.__str__(),
            reply_to_message_id=message.id
        )
        return

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















