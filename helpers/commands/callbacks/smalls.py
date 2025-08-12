from pyromod import Client
from pyrogram.types import CallbackQuery
from pyrogram.types import Message
from pyromod.exceptions import ListenerTimeout, ListenerStopped
import globals.messages as messages
from globals.database import bd
from helpers.commands.components import generate_settings_keyboard, generate_help_keyboard


async def set_thumbnail(bot : Client, message : Message) :
    """
    Fonction pour définir une miniature pour le téléchargement.
    """
    user_id = message.from_user.id
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            await message.reply_text(messages.REPLY_TO_PHOTO)
            return
        reply_photo = message.reply_to_message.photo
        photo_id = reply_photo.file_id
        await bd.set_user_thumbnail(user_id, photo_id)
        await message.reply_text(messages.THUMBNAIL_SET)
    except (ListenerStopped, ListenerTimeout):
        await bot.send_message(
            user_id,
            messages.SEND_THUMBNAIL_TIMEOUT,
        )
    except Exception as e:
        await message.reply_text(messages.ERROR_OCCURRED.format(str(e)))

async def delete_thumbnail(_, message : Message) :
    """
    Fonction pour supprimer la miniature définie par l'utilisateur.
    """
    user_id = message.from_user.id
    try:
        await bd.delete_user_thumbnail(user_id)
        await message.reply_text(messages.THUMBNAIL_DELETED)
    except Exception as e:
        await message.reply_text(messages.ERROR_OCCURRED.format(str(e)))

async def show_thumbnail(bot : Client, message : Message) :
    """
    Fonction pour afficher la miniature définie par l'utilisateur.
    """
    user_id = message.from_user.id
    try:
        thumbnail = await bd.get_user_thumbnail(user_id)
        if thumbnail:
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=thumbnail,
                caption=messages.CURRENT_THUMBNAIL
            )
        else:
            await message.reply_text(messages.NO_THUMBNAIL_SET)
    except Exception as e:
        await message.reply_text(messages.ERROR_OCCURRED.format(str(e)))

async def settings(_, message : Message) :
    """
    Fonction pour afficher les paramètres.
    """
    try:

        await message.reply_text(
            messages.SETTINGS,
            reply_markup=generate_settings_keyboard()
        )
    except Exception as e:
        await message.reply_text(messages.ERROR_OCCURRED.format(str(e)))

async def help_command(_, message : Message) :
    """
    Fonction pour afficher l'aide.
    """
    try:
        await message.reply_text(
            messages.HELP,
            reply_markup=generate_help_keyboard()
        )
    except Exception as e:
        await message.reply_text(messages.ERROR_OCCURRED.format(str(e)))

async def calback_queries_func(bot: Client, query: CallbackQuery):
    """
    Fonction pour gérer les requêtes de rappel.
    """
    user_id = query.from_user.id
    try:
        if query.data == "set_thumbnail":
            await query.message.reply_text(
                messages.REPLY_TO_PHOTO,
            )
            return
        elif query.data == "delete_thumbnail":
            await bd.delete_user_thumbnail(user_id)
            await query.message.reply_text(messages.THUMBNAIL_DELETED)
        elif query.data == "show_thumbnail":
            thumbnail = await bd.get_user_thumbnail(user_id)
            if thumbnail:
                await bot.send_photo(
                    chat_id=user_id,
                    photo=thumbnail,
                    caption=messages.CURRENT_THUMBNAIL
                )
            else:
                await query.message.reply_text(messages.NO_THUMBNAIL_SET)
            return
        elif query.data == "info_rename":
            sfx = await bd.get_user_suffix(user_id)
            prfx = await bd.get_user_prefix(user_id)
            custom_caption = await bd.get_user_caption(user_id)
            await query.message.reply_text(
                messages.INFO_RENAME.format(prfx, sfx, custom_caption),
            )
        elif query.data == "help":
            await query.message.edit_text(
                messages.HELP,
                reply_markup=generate_help_keyboard()
            )
            return
        elif query.data == "about":
            await query.message.edit_text(
                messages.ABOUT,
                disable_web_page_preview=True
            )
        elif query.data == "settings":
            await query.message.edit_text(
                messages.SETTINGS,
                reply_markup=generate_settings_keyboard()
            )
            return
        elif query.data == "close":
            await query.message.delete()
    except Exception as e:
        await query.answer(messages.ERROR_OCCURRED.format(str(e)), show_alert=True)

async def set_caption(_, message : Message):
    try:
        args = message.text.split()[1:]
        if not args:
            await message.reply_text(
                messages.SET_CAPTION
            )
            return
        caption = " ".join(args)
        await bd.set_user_caption(message.from_user.id, caption)
        await message.reply_text(
            messages.CAPTION_SET_DONE
        )
    except Exception as e:
        await message.reply_text(messages.ERROR_OCCURRED.format(str(e)))

async def del_caption(_, message : Message):
    try:
        await bd.delete_user_caption(message.from_user.id)
        await message.reply_text(
            messages.CAPTION_DELETE
        )
    except Exception as e:
        await message.reply_text(messages.ERROR_OCCURRED.format(str(e)))




