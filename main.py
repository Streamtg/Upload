import uvloop
#Module de speed up
uvloop.install()


from pyrogram import Client
from pyrogram.types import BotCommand

from config import Config
from aiohttp import web
import asyncio

from globals.utils import log_admin
from globals.web_services import web_server
from  helpers.commands.handlers import register_commands_handlers
from helpers.Upload_Download.handlers import register_download_upload_handlers


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="RapidUploader",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
        )

    async def start(self):
        try:
            await super().start()
            register_commands_handlers(self)
            register_download_upload_handlers(self)

            #Ajout des commandes du Bot
            await self.set_bot_commands(
                [
                    BotCommand("start", "🚀 Lance le bot"),
                    BotCommand("settings", "⚙️ Montre les paramètres "),
                    BotCommand("set_thumb", "📸 Mets à jour votre miniature"),
                    BotCommand("show_thumb", "🖼 Montre votre miniature actuelle"),
                    BotCommand("del_thumb", "🗑🖼 Supprime votre miniature actuelle"),
                    BotCommand("set_caption", "📜 Mets à jour la légende des fichiers qui seront envoyés"),
                    BotCommand("del_caption", "🗑 Supprime la légende actuelle"),
                    BotCommand("set_prefix", "⬅️ Mets à jour le préfixe des fichiers qui seront envoyés"),
                    BotCommand("del_prefix", "🗑 Supprime le préfixe"),
                    BotCommand("set_suffix", "➡️ Mets à jour le suffixe des fichiers qui seront envoyés"),
                    BotCommand("del_suffix", "🗑 Supprime le suffixe actuel"),
                    BotCommand("help", "🆘 Affiche ce message d'aide"),
                ],
                language_code='fr'
            )

            await log_admin("Bot démarré avec succès ✅")
        except Exception as error:
            await log_admin(f"❌ Erreur critique lors du démarrage du bot : {error}")

    async def stop(self, *args):
        await super().stop()
        await log_admin("Bot stoppé avec succès ✅")

async def start_web_server():

    # Configuration du serveur Web
    server = web.AppRunner(await web_server())
    await server.setup()
    bind_address = "0.0.0.0"
    site = web.TCPSite(server, bind_address, Config.PORT)
    await site.start()

bot_instance = Bot()


def main():
    async def start_services():
        await asyncio.gather(
            bot_instance.start(),
            start_web_server()
        )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_services())
    loop.run_forever()


if __name__ == "__main__":
    main()