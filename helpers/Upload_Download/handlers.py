from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from helpers.Upload_Download.callbacks.download_cb import detect_link, rename_file, download_file, download_cancel

def register_download_upload_handlers(bot):
    """
    Enregistre les gestionnaires pour le téléchargement et l'upload de fichiers.
    :param bot: Instance du client Pyrogram
    """
    bot.add_handler(MessageHandler(detect_link, filters.regex(pattern=r'^https?://') & filters.private))
    bot.add_handler(CallbackQueryHandler(rename_file, filters.regex("^rename$")))
    bot.add_handler(CallbackQueryHandler(download_file, filters.regex("^download$")))
    bot.add_handler(CallbackQueryHandler(download_cancel, filters.regex("^cancel_download$")))

