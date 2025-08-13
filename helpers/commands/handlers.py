from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from helpers.commands.callbacks.smalls import (
    start,
    set_thumbnail,
    delete_thumbnail,
    show_thumbnail,
    settings,
    calback_queries_func,
    help_command,
    set_caption,
    del_caption,
    set_prefix,
    set_suffix,
    del_prefix,
    del_suffix
)

def register_commands_handlers(bot):
    """
    Enregistre les gestionnaires pour les commandes de l'application.
    :param bot: Instance du client Pyrogram
    """
    bot.add_handler(MessageHandler(start, filters.command("start") & filters.private))
    bot.add_handler(MessageHandler(set_thumbnail, filters.command("set_thumb") & filters.private))
    bot.add_handler(MessageHandler(show_thumbnail, filters.command("show_thumb") & filters.private))
    bot.add_handler(MessageHandler(delete_thumbnail, filters.command("del_thumb") & filters.private))
    bot.add_handler(MessageHandler(settings, filters.command("settings") & filters.private))
    bot.add_handler(CallbackQueryHandler(calback_queries_func, filters.regex("^(set_thumbnail|delete_thumbnail|show_thumbnail|close|settings|info_rename|help|about)$")))
    bot.add_handler(MessageHandler(help_command, filters.command("help") & filters.private))
    bot.add_handler(MessageHandler(set_caption, filters.command("set_caption") & filters.private))
    bot.add_handler(MessageHandler(set_prefix, filters.command("set_prefix") & filters.private))
    bot.add_handler(MessageHandler(set_suffix, filters.command("set_suffix") & filters.private))
    bot.add_handler(MessageHandler(del_caption, filters.command("del_caption") & filters.private))
    bot.add_handler(MessageHandler(del_suffix, filters.command("del_suffix") & filters.private))
    bot.add_handler(MessageHandler(del_prefix, filters.command("del_prefix") & filters.private))


    # Vous pouvez ajouter d'autres gestionnaires de commandes ici si nécessaire.