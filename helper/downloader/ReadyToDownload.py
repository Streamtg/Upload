import time

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorDNSError, ClientResponseError
import aiofiles
import re
import os
from telegram.constants import ParseMode
from telegram import Bot
import helper.messages as messages
from config import Config
from helper.downloader.DownloadResult import DownloadResult
from helper.utils import log_admin
from helper.downloader.download_utils import generate_download_cancel_button


#--------Méthodes statiques--------
async def calcul_pourcentage(current_size, total_size):
    return current_size * 100 / total_size

def sanitize_filename(name):
    """
    Fonction de nettoyage basique. Merci Claude
    :param name: Nom à netoyer
    :return:
    """
    return re.sub(r'[\\/:*?"<>|]', '', name)

async def afficher_carre(progress :int | float) -> str:
    progress = int(progress)
    done = progress // 10
    remaining = 10 - done
    return ("█" * done) + ("░" * remaining)

def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    #https://github.com/AbirHasan2005/Rename-Bot/blob/main/bot/core/display.py
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(round(size, 2)) + " " + Dic_powerN[n] + 'B'

def TimeFormatter(milliseconds: int) -> str:
    """
    Source : https://github.com/AbirHasan2005/Rename-Bot/blob/main/bot/core/display.py
    :param milliseconds: Millisecondes
    :return: Un formattage parlant pas en millisecondes
    """
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " days, ") if days else "") + \
          ((str(hours) + " hours, ") if hours else "") + \
          ((str(minutes) + " min, ") if minutes else "") + \
          ((str(seconds) + " sec, ") if seconds else "") + \
          ((str(milliseconds) + " millisec, ") if milliseconds else "")
    return tmp[:-2]

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

    async def download_file(
            self,
            bot : Bot,
            chat_id : int,
            path : str = Config.DOWNLOAD_DIR,
    ) -> DownloadResult | None :
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
        try:
            first_msg = await bot.send_message(
                chat_id,
                messages.DOWNLOAD_START.format(filename_with_ext),
                parse_mode=ParseMode.HTML
            )
            if not os.path.isdir(path):
                os.makedirs(path, exist_ok=True)
            try:
                async with ClientSession() as session:
                    async with session.get(self._download_url) as response:
                        response.raise_for_status()
                        total_size = self._file_size
                        current_size = 0
                        already_modified = set()
                        start = time.time()

                        async with aiofiles.open(file_path, "wb") as f:
                            async for chunck in response.content.iter_chunked(10240):
                                await f.write(chunck)
                                current_size += len(chunck)
                                #Si on n'a pas pu obtenir le poids du fichier, on continue le téléchargement
                                # sans afficher la progression
                                if not total_size:
                                    continue
                                pourcentage = await calcul_pourcentage(current_size, total_size)

                                #On modifie la barre de progression tous les 5% d'avancés
                                #Ca va etre un peu brutal!!!!!
                                if int(pourcentage) % 5 == 0 and int(pourcentage) not in already_modified:
                                    now = time.time()
                                    diff = now - start
                                    speed = current_size / diff
                                    elapsed_time = round(diff) * 1000
                                    time_to_completion = round((total_size - current_size) / speed) * 1000
                                    estimated_total_time = elapsed_time + time_to_completion
                                    estimated_total_time = TimeFormatter(estimated_total_time)
                                    msg = f"{await afficher_carre(pourcentage)}\n" + \
                                        messages.PROGRESS.format(
                                            f"{pourcentage:.2f}",
                                            humanbytes(current_size),
                                            humanbytes(total_size),
                                            humanbytes(speed),
                                            estimated_total_time if estimated_total_time != '' else "0 s"
                                        )
                                    await first_msg.edit_text(
                                        msg,
                                        ParseMode.HTML,
                                        generate_download_cancel_button()
                                    )
                                    already_modified.add(int(pourcentage))
                await first_msg.edit_text(
                    messages.DOWNLOAD_FINISHED,
                    ParseMode.HTML
                )
                return DownloadResult(
                    file_path=file_path,
                    chat_id=chat_id,
                    file_final_name=filename_with_ext,
                    success=True,
                )
            except (ClientResponseError, ClientConnectorDNSError):
                await first_msg.edit_text(
                    "Une erreur est survenue lors du télécharment❌"
                )
                return None
        except Exception as e:
            await first_msg.edit_text(
                    "Une erreur est survenue lors du télécharment❌"
            )
            await log_admin(
                f"Une erreur innatendue s'est produite lors d'un téléchargement : {e}",
                "download_file"
            )
            return None

 # Just for testing purposes, should be replaced with actual Bot and chat_id
