from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from helpers.commands.callbacks.smalls import (
    set_thumbnail,
    delete_thumbnail,
    show_thumbnail,
    settings,
    calback_queries_func,
    help_command,
    set_caption
)

def register_commands_handlers(bot):
    """
    Enregistre les gestionnaires pour les commandes de l'application.
    :param bot: Instance du client Pyrogram
    """
    bot.add_handler(MessageHandler(set_thumbnail, filters.command("set_thumb") & filters.private))
    bot.add_handler(MessageHandler(show_thumbnail, filters.command("show_thumb") & filters.private))
    bot.add_handler(MessageHandler(delete_thumbnail, filters.command("del_thumb") & filters.private))
    bot.add_handler(MessageHandler(settings, filters.command("settings") & filters.private))
    bot.add_handler(CallbackQueryHandler(calback_queries_func, filters.regex("^(set_thumbnail|delete_thumbnail|show_thumbnail|close|settings|info_rename|help|about)$")))
    bot.add_handler(MessageHandler(help_command, filters.command("help") & filters.private))
    bot.add_handler(MessageHandler(set_caption, filters.command("set_caption") & filters.private))

    # Vous pouvez ajouter d'autres gestionnaires de commandes ici si nécessaire.