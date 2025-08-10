import uuid

from helpers.Upload_Download.downloader.ReadyToDownload import ReadyToDownload
from helpers.Upload_Download.downloader.DownloadResult import DownloadResult

class UserData:
    """
    Classe pour stocker les données utilisateur.
    """
    __DATA : dict = {}  # Dictionnaire pour stocker les données utilisateur

    @classmethod
    async def get_on_downloads(cls) -> dict:
        """
        Retourne le dictionnaire des utilisateurs en cours de téléchargement.
        """
        return cls.__DATA.get('on_downloads', {})

    @classmethod
    async def add_download(cls, user_id: int, download_object : ReadyToDownload):
        """
        Ajoute un utilisateur et son ID de téléchargement au dictionnaire.
        """
        if 'on_downloads' not in cls.__DATA:
            cls.__DATA['on_downloads'] = {}
        cls.__DATA['on_downloads'][user_id] = download_object


    @classmethod
    async def update_download_name(cls, user_id: int, new_name: str) -> bool:
        """
        Met à jour le nom du fichier pour l'utilisateur en cours de téléchargement.
        """
        if 'on_downloads' in cls.__DATA and user_id in cls.__DATA['on_downloads']:
            download_object = cls.__DATA['on_downloads'][user_id]
            download_object.filename = new_name
            return True
        return False


    @classmethod
    async def remove_download(cls, user_id: int):
        """
        Supprime l'utilisateur du dictionnaire des téléchargements.
        """
        if 'on_downloads' in cls.__DATA and user_id in cls.__DATA['on_downloads']:
            del cls.__DATA['on_downloads'][user_id]
    @classmethod
    async def get_download(cls, user_id: int) -> ReadyToDownload | None:
        """
        Retourne l'objet de téléchargement associé à l'utilisateur.
        """
        return cls.__DATA.get('on_downloads', {}).get(user_id, None)

    @classmethod
    async def in_downloads(cls, user_id: int) -> bool:
        """
        Vérifie si l'utilisateur est en cours de téléchargement.
        """
        return user_id in cls.__DATA.get('on_downloads', {})
