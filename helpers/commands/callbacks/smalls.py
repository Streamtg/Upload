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

async def set_thumbnail(bot : Client, message : Message) :
    """
    Fonction pour définir une miniature pour le téléchargement.
    """
    user_id = message.from_user.id
    try:
        if not message.reply_to_message or not message.reply_to_message.photo:
            reply_photo = await bot.ask(
                chat_id=message.chat.id,
                text=messages.SEND_THUMBNAIL,
                filters=filters.photo,
                reply_markup=ForceReply(selective=True),
                timeout=20
            )
            await bd.set_user_thumbnail(user_id, reply_photo.photo.file_id)
            await reply_photo.reply_text(messages.THUMBNAIL_SET)
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

async def delete_thumbnail(bot : Client, message : Message) :
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




