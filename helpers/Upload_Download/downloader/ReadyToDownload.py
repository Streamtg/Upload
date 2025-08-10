import time

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorDNSError, ClientResponseError
import aiofiles
import os
from pyrogram.client import Client
from pyrogram.enums import ParseMode
import globals.messages as messages
from config import Config
from helpers.Upload_Download.downloader.DownloadResult import DownloadResult
from helpers.utils import log_admin
from helpers.Upload_Download.utils import progress_func, sanitize_filename, humanbytes




class ReadyToDownload:

    def __init__(self, filename: str, file_extension: str, file_size: float, file_download_url: str, chat_request_id : int):
        self._filename = filename
        self._file_size = file_size
        self._file_extension = file_extension
        self._download_url = file_download_url
        self._chat_id = chat_request_id

    @property
    def file_size(self):
        return self._file_size

    @property
    def file_size_human(self):
        return humanbytes(self._file_size)

    @property
    def file_download_url(self):
        return self._download_url

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, new_filename : str):
        self._filename = new_filename

    @property
    def filename_with_ext(self):
        return self._filename + self._file_extension

    @property
    def chat_id(self):
        return self._chat_id

    async def download_file(
            self,
            bot : Client,
            chat_id : int,
            path : str = Config.DOWNLOAD_DIR,
    ) -> DownloadResult:
        """
        Fonction asynchrone qui télécharge un fichier, notifie son avancement sur un message
        et l'enregistre vers le chemin spécifié
        :param bot: Instance du bot Telegram
        :param chat_id: Id de la discussion dans laquelle le téléchargement a été lancé
        :param path: Chemin vers lequel le fichier sera téléchargé
        :return: DownloadResult, le résultat du téléchargement
        """
        filename_with_ext = sanitize_filename(self.filename_with_ext)
        file_path = path + filename_with_ext

        first_msg = await bot.send_message(
            chat_id,
            messages.DOWNLOAD_START.format(filename_with_ext),
            parse_mode=ParseMode.HTML
        )
        try:
            if not os.path.isdir(path):
                os.makedirs(path, exist_ok=True)
            try:
                async with ClientSession() as session:
                    async with session.get(self._download_url) as response:
                        response.raise_for_status()
                        total_size = self._file_size
                        current_size = 0
                        start = time.time()

                        async with aiofiles.open(file_path, "wb") as f:
                            async for chunck in response.content.iter_chunked(10240):
                                await f.write(chunck)
                                #Si on n'a pas pu obtenir le poids du fichier, on continue le téléchargement
                                # sans afficher la progression
                                if not total_size:
                                    continue
                                current_size += len(chunck)

                                #On modifie la barre de progression
                                await progress_func(
                                    current=current_size,
                                    total=total_size,
                                    message="🤖ᴛéʟᴇᴄʜᴀʀɢᴇᴍᴇɴᴛ ᴇɴ ᴄᴏᴜʀꜱ..",
                                    first_msg=first_msg,
                                    start=start
                                )
                #On envoie un message de fin de téléchargement
                await first_msg.edit_text(
                    messages.DOWNLOAD_FINISHED,
                    ParseMode.HTML
                )
                return DownloadResult(
                    file_path=file_path,
                    chat_id=chat_id,
                    file_final_name=filename_with_ext,
                    success=True,
                    editable_message=first_msg
                )
            except (ClientResponseError, ClientConnectorDNSError):
                await first_msg.edit_text(
                    "Une erreur est survenue lors du télécharment❌"
                )
                return DownloadResult(
                    success=False,
                    error="Erreur de connexion",
                    chat_id=chat_id,
                    editable_message=first_msg,
                )
        except Exception as e:
            await first_msg.edit_text(
                    "Une erreur est survenue lors du télécharment❌"
            )
            await log_admin(
                f"Une erreur innatendue s'est produite lors d'un téléchargement : {e}",
                "download_file"
            )
            return DownloadResult(
                    success=False,
                    error=str(e),
                    chat_id=chat_id,
                    editable_message=first_msg,
                )