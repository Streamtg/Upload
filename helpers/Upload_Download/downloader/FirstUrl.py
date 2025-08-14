from helpers.Upload_Download.downloader.ReadyToDownload import ReadyToDownload

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientConnectorDNSError, ClientResponseError
import re
from urllib.parse import unquote, urlparse

from globals.utils import log_admin

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
    :return: L'extension du fichier s'il est trouvé, Une chaine vide dans le cas contraire
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
    return content_type_to_extension.get(c_type, "")

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
            ext = "." + items[-1]
            filename = " ".join(items[0:-1])
            return filename, ext
        return None
    except Exception as e:

        return None

async def get_file_size_with_range(url):
    try:
        async with ClientSession() as session:
            async with session.get(url, headers={"Range": "bytes=0-0"}) as response:
                content_range = response.headers.get("Content-Range")
                if content_range:
                    # Format attendu: bytes 0-0/12345
                    size = int(content_range.split("/")[-1])
                    return float(size)
                return 0.0
    except Exception:
        return 0.0

async def get_file_size(headers : dict, url : str) -> float:
    """
    Fonction asynchrone qui essaye de trouver le poids d'un fichier depuis les headers HTTP
    :param headers: Entetes HTTP
    :param url: Lien Url du fichier
    :return: Un float relatif au poid du fichier en Mo si trouvé, autrement 0
    """
    size = headers.get("Content-Length")
    if not size :
        try:
            return await get_file_size_with_range(url)
        except Exception:
            return 0.0
    return float(size)

class FirstUrl:

    def __init__(self, url : str, chat_id : int):
        self.url = url
        self.chat_id = chat_id

    async def get_file_infos(self) -> ReadyToDownload :
        """
        Fonction asynchrone qui essaye de trouver le nom adéquat pour le fichier,
        depuis soit les headers ou le lien, si aucune correspondace n'est trouvé lève une ValueError
        :return: ReadyToDownload si le lien est valide et pointe vers un fichier, son extension et sa
        taille (Si la taille n'est pas trouvé, on retourne 0) dans le cas contraire
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
                    response_url = response.url.__str__()
                    #On verifie si on a atteint le lien final, si oui on sort de la boucle
                    if response_url == url:
                        break
                    #Sinon, on continue à suivre les redirections
                    url = response_url
                    redirects -= 1
                    continue

                headers = response.headers
                size = await get_file_size(headers, url)
                #On essaie de trouver le nom du fichier et son extension depuis les headers HTTP
                filename = await get_filename_from_headers(headers)
                if filename:
                    items = filename.split(".")
                    if len(items) >= 2:
                        ext = "." + items[-1]
                        filename = " ".join(items[0:-1])
                        return ReadyToDownload(filename, ext, size, url, self.chat_id)
                    ext = await get_extension_from_header(headers)
                    return ReadyToDownload(filename, ext, size, url, self.chat_id)

                #Si on ne trouve pas de correspondance dans les headers, on essaie de l'extraire directement du lien de download
                try:
                    filename, ext = await get_file_infos_from_url(url)
                except TypeError:
                    raise ValueError("Le lien de téléchargement ne permet pas de trouver le nom du fichier❌")
                else:
                    return ReadyToDownload(filename, ext, size, url, self.chat_id)
            except (ClientResponseError, ClientConnectorDNSError):
                raise ValueError("Ce lien de téléchargement n'est pas valide❌")
            except ValueError as e:
                raise ValueError(e)
            except Exception as e:
                await log_admin(
                    f"Une Erreur ({e.__class__.__name__}) est survenue : {e}",
                    "get_file_infos"
                )
                raise ValueError("Une erreur est survenue❌")