from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram import filters
from helpers.commands.callbacks.smalls import set_thumbnail, show_thumbnail, delete_thumbnail

def register_commands_handlers(bot):
    """
    Enregistre les gestionnaires pour les commandes de l'application.
    :param bot: Instance du client Pyrogram
    """
    bot.add_handler(MessageHandler(set_thumbnail, filters.command("set_thumb") & filters.private))
    bot.add_handler(MessageHandler(show_thumbnail, filters.command("show_thumb") & filters.private))
    bot.add_handler(MessageHandler(delete_thumbnail, filters.command("del_thumb") & filters.private))
    # Vous pouvez ajouter d'autres gestionnaires de commandes ici si nécessaire.