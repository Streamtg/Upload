import time

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorDNSError, ClientResponseError
import aiofiles
import re
from urllib.parse import unquote, urlparse
import asyncio
import os
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from telegram import Update
import helper.messages as messages
from config import Config
from helper.utils import log_admin


#----Méthodes statiques----
async def get_filename_from_headers(headers : dict) -> str | None:
    """
    Fonction asynchrone pour essayer de récuperer un nom de fichier depuis les
    entetes HTTP
    :param headers: En-tetes HTTP
    :return: Le nom du fichier s'il est trouvé, None dans le cas contraire
    """
    content_disposition = headers.get("Content-Disposition")
    if not content_disposition:
        return None
    if 'filename' in content_disposition:
        #On crée un pattern pour recuperer le nom complet du fichier
        pattern = r'filename\*?=([^;]+)'
        res = re.search(pattern, content_disposition)
        if res:
            filename = res.group(1)
            #Essayer de decoder le nom du fichier, car parfois encodé
            if filename.startswith('UTF-8'):
                try:
                    filename = filename.encode('latin-1').decode('utf-8')
                except (UnicodeEncodeError, UnicodeDecodeError):
                    pass
            return unquote(filename).replace('"', "")
    return None

async def get_extension_from_header(headers : dict) -> str | None:
    """
    Fonction asynchrone pour essayer de récuperer l'extension d'un fichier depuis les
    entetes HTTP
    :param headers: En-tetes HTTP
    :return: L'extension du fichier s'il est trouvé, None dans le cas contraire
    """
    c_type = headers.get("Content-Type")
    content_type_to_extension = {
        # Archives
        'application/zip': '.zip',
        'application/x-rar-compressed': '.rar',
        'application/x-7z-compressed': '.7z',
        'application/x-tar': '.tar',
        'application/gzip': '.gz',
        # Vidéos
        'video/mp4': '.mp4',
        'video/x-msvideo': '.avi',
        'video/x-matroska': '.mkv',
        'video/webm': '.webm',
        'video/mpeg': '.mpeg',
        # Audio
        'audio/mpeg': '.mp3',
        'audio/wav': '.wav',
        'audio/ogg': '.ogg',
        'audio/flac': '.flac',
        'audio/webm': '.webm',
        'audio/aac': '.aac',
    }
    return content_type_to_extension.get(c_type)

async def get_file_infos_from_url(url : str) -> tuple[str, str] | None:
    """
    Fonction asynchrone qui essaye de trouver le nom d'un fichier et son extension depuis une url
    :param url: Url
    :return: Un tuple contenant le nom et l'extension du fichier si trouvé, autrement None
    """
    try:
        file_infos = unquote(urlparse(url).path.split('/')[-1])
        if not file_infos:
            return None
        items = file_infos.split(".")
        if len(items) >= 2:
            ext = items[-1]
            filename = " ".join(items[0:-1])
            return filename, ext
        return None
    except:
        return None

async def get_file_size(headers : dict) -> float:
    """
    Fonction asynchrone qui essaye de trouver le poids d'un fichier depuis les headers HTTP
    :param headers: Entetes HTTP
    :return: Un float relatif au poid du fichier en Mo si trouvé, autrement 0
    """
    size = headers.get("Content-Length")
    if not size : return 0.0
    return float(size) / 1e+6       #Conversion d'octet en Mb
# head = {'Date': 'Fri, 18 Jul 2025 05:05:34 GMT', 'Content-Type': 'video/x-matroska', 'Content-Length': '3624392', 'Connection': 'keep-alive', 'Server': 'cloudflare', 'Expires': 'Wed, 11 Jan 1984 05:00:00 GMT', 'Cache-Control': 'no-cache, must-revalidate, max-age=0', 'X-Robots-Tag': 'noindex, nofollow', 'Robots': 'none', 'Content-Description': 'File Transfer', 'Content-Disposition': 'attachment; filename="normal.txt"; filename*=UTF-8''%E2%82%ACrates.txt', 'Content-Transfer-Encoding': 'binary', 'X-Frame-Options': 'SAMEORIGIN', 'X-Content-Type-Options': 'nosniff', 'X-Xss-Protection': '1; mode=block', 'X-Permitted-Cross-Domain-Policies': 'master-only', 'Referrer-Policy': 'same-origin', 'Alt-Svc': 'h3=":443"; ma=86400', 'Cf-Cache-Status': 'BYPASS', 'Speculation-Rules': '"/cdn-cgi/speculation"', 'Vary': 'accept-encoding', 'Report-To': '{"group":"cf-nel","max_age":604800,"endpoints":[{"url":"https://a.nel.cloudflare.com/report/v4?s=CaYv36w2Ua7gls5K62uaBKAxIQeqFF4B0%2FeQYkq0Tw43mb3H%2FlYk7HzmS8l4EtfSZCYu2wGM7q3HRJsP%2FaJY%2Bg5ZMSG54l03vvdLuz9slMSn7cYUKZaEhjM%3D"}]}', 'Nel': '{"report_to":"cf-nel","success_fraction":0.0,"max_age":604800}', 'Set-Cookie': '__wpdm_client=1cf4ea093b65cb827a6d012a3678bce6; HttpOnly; Secure; Path=/', 'CF-RAY': '960f71d79d2e02af-CDG'}

async def afficher_carre(progress :int | float) -> str:
    progress = int(progress)
    done = progress // 10
    remaining = 10 - done
    return ("▣" * done) + (remaining * "▢")

async def calcul_pourcentage(current_size, total_size):
    return current_size * 100 / total_size

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

def sanitize_filename(name):
    """
    Fonction de nettoyage basique. Merci Claude
    :param name: Nom à netoyer
    :return:
    """
    return re.sub(r'[\\/:*?"<>|]', '', name)

class Downloader:

    def __init__(self, url : str):
        self.url = url

    async def get_file_infos(self) -> dict :
        """
        Fonction asynchrone qui essaye de trouver le nom adéquat pour le fichier,
        depuis soit les headers ou le lien, si aucune correspondace n'est trouvé retourne None
        :return: None si aucune correspondace n'est trouvé, un dictionnaire contenant le nom du fichier,
         son extension et sa taille (Si la taille n'est pas trouvé, on retourne 0) dans le cas contraire
        :raise ValueError si le lien de téléchargement n'est pas atteignable ou que l'on n'arrive pas à recuperer
        le nom du fichier
        """
        async with ClientSession() as session:
            try:
                url = self.url
                redirects = 2
                while True:
                    if redirects == 0:
                        raise ValueError("Ce lien n'est pas un lien de téléchargement direct❌")
                    response = await session.head(url, allow_redirects=True)
                    response.raise_for_status()
                    if response.url == url:
                        break
                    url = response.url
                    redirects -= 1
                    continue
                self.url = url
                headers = response.headers
                size = await get_file_size(headers)
                #On essaie de trouver le nom du fichier et son extension depuis les headers HTTP
                filename = await get_filename_from_headers(headers)
                if filename:
                    items = filename.split(".")
                    if len(items) >= 2:
                        ext = items[-1]
                        filename = " ".join(items[0:-1])
                        return {"filename" : filename, "extension" : ext, "size" : size}
                    ext = await get_extension_from_header(headers)
                    return {"filename" : filename, "extension" : ext, "size" : size}

                #Si on ne trouve pas de correspondance dans les headers, on essaie de l'extraire directement du lien de download
                try:
                    filename, ext = await get_file_infos_from_url(str(url))
                except TypeError:
                    raise ValueError("Le lien de téléchargement ne permet pas de trouver le nom du fichier❌")
                return {"filename" : filename, "extension" : ext, "size" : size}
            except (ClientResponseError, ClientConnectorDNSError):
                raise ValueError("Ce lien de téléchargement n'est pas valide❌")
            except Exception as e:
                await log_admin(
                    f"Une Erreur ({e.__class__.__name__}) est survenue : {e}",
                    "get_file_infos"
                )
                raise ValueError("Une erreur est survenue❌")

    async def download_file(
            self,
            filename_with_ext : str,
            context : ContextTypes.DEFAULT_TYPE,
            chat_id : str | int,
            msg_id : int,
            path : str = Config.DOWNLOAD_DIR,
    ) -> bool:
        """
        Fonction asynchrone qui télécharge un fichier, notifie son avancement sur un message
        et l'enregistre vers le chemin spécifié
        :param filename_with_ext: Nom du fichier avec l'extension
        :param context: Objet context englobant toutes les methosdes relatives au bot
        :param chat_id: Id de la discussion dans laquelle le téléchargement a été lancé
        :param msg_id: Id du message sur lequel l'avancée du telechargement sera visisble
        :param path: Chemin vers lequel le fichier sera téléchargé
        :return: Un booleen True si le téléchargement se termine sans aucune erreur, False sinon
        """
        try:
            await context.bot.edit_message_text(
                messages.DOWNLOAD_START.format(filename_with_ext),
                chat_id,
                msg_id,
                parse_mode=ParseMode.HTML
            )
            if not os.path.isdir(path):
                os.makedirs(path, exist_ok=True)
            try:
                async with ClientSession() as session:
                    async with session.get(self.url) as response:
                        response.raise_for_status()
                        #On essaie de recuperer le poidds total du fichier dupuis les headers
                        #On recupere 0 si le poids n'existe pas
                        total_size = int(response.headers.get('Content-Length', 0))
                        current_size = 0
                        already_modified = set()
                        start = time.time()
                        filename_with_ext = sanitize_filename(filename_with_ext)
                        async with aiofiles.open(path + filename_with_ext, "wb") as f:
                            async for chunck in response.content.iter_chunked(10240):
                                await f.write(chunck)
                                current_size += len(chunck)
                                #Si on n'a pas pu obtenir le poids du fichier, on continue le téléchargement sans afficher
                                #la progression
                                if total_size == 0:
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
                                    msg = f"{afficher_carre(pourcentage)}\n" + \
                                        messages.PROGRESS.format(
                                            pourcentage,
                                            humanbytes(current_size),
                                            humanbytes(total_size),
                                            humanbytes(speed),
                                            estimated_total_time if estimated_total_time != '' else "0 s"
                                        )
                                    await context.bot.edit_message_text(
                                        msg,
                                        chat_id,
                                        msg_id,
                                        ParseMode.HTML
                                    )
                                    already_modified.add(int(pourcentage))
                await context.bot.edit_message_text(
                    messages.DOWNLOAD_FINISHED,
                    chat_id,
                    msg_id,
                    ParseMode.HTML
                )
                return True
            except (ClientResponseError, ClientConnectorDNSError):
                await context.bot.edit_message_text(
                    "Une erreur est survenue lors du télécharment❌",
                    chat_id,
                    msg_id,
                )
                return False

        except Exception as e:
            await context.bot.edit_message_text(
                    "Une erreur est survenue lors du télécharment❌",
                    chat_id,
                    msg_id,
            )
            await log_admin(
                f"Une erreur innatendue s'est produite lors d'un téléchargement : {e}",
                "download_file"
            )
            return False









async def main():
    uri = "https://www.learningcontainr.com/download/sample-mkv-video-files/?wpdmdl=2565&refresh=6874d237570321752486455"
    instance = Downloader(uri)
    try:
        res = await instance.get_file_infos()
        print(f"Réussi : {res}")
    except ValueError as e:
        print(f"Erreur : {e}")
if __name__ == '__main__':
    # print(os.path.isdir(Config.DOWNLOAD_DIR))
    # print(os.mkdir(Config.DOWNLOAD_DIR))
    pass