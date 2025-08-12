
import firebase_admin
from firebase_admin import db
from json import loads
from requests.exceptions import RequestException
from config import Config
from firebase_admin.exceptions import FirebaseError
from helpers.utils import log_admin

FIREBASE_KEY = loads(Config.FIREBASE_KEY)   # Votre clé privée Firebase

FIREBASE_URL = Config.FIREBASE_URL  # URL de votre base de données Firebase

# Initialisation de l'application Firebase
cred = firebase_admin.credentials.Certificate(FIREBASE_KEY)

firebase_admin.initialize_app(
    cred,
    {
    'databaseURL': FIREBASE_URL
    }
)

class Database:
    """
    Classe pour gérer la connexion à Firebase et les opérations de base de données.
    """
    def __init__(self):
        self.retries = 3
        self.timeout = 10
        while self.retries > 0:
            try:
                if not firebase_admin._apps:
                    firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_URL})
                self.ref = db.reference("Upload&Rename_Bot")
                return
            except RequestException as e:
                self.retries -= 1
                if self.retries == 0:
                    from asyncio import run
                    run(log_admin(f"Impossible de se connecter à Firebase après 3 essais: {e}", ))
                    raise ConnectionError(f"Impossible de se connecter à Firebase après 3 essais: {e}")

    async def _user_exists(self, user_id: int) -> bool:
        user_ref = self.ref.child('users').child(str(user_id))
        return user_ref.get() is not None

    async def add_user(self, user_id: int, username: str):
        """
        Ajoute un utilisateur à la base de données Firebase.
        :param user_id: ID Telegram de l'utilisateur
        :param username: Username Telegram de l'utilisateur
        """
        try:
            if await self._user_exists(user_id):
                return
            user_data = {
                'user_id': user_id,
                'username': username,
            }
            self.ref.child('users').child(str(user_id)).set(user_data)
        except FirebaseError as e:
            await log_admin(f"Erreur lors de l'ajout de l'utilisateur {user_id} à Firebase: {e}")

    async def get_user(self, user_id: int) -> object | None:
        """
        Récupère les informations d'un utilisateur à partir de son ID.
        :param user_id: ID Telegram de l'utilisateur
        :return: Un dictionnaire contenant les informations de l'utilisateur ou None si l'utilisateur n'existe pas
        """
        try:
            if not await self._user_exists(user_id):
                return None
            return (self.ref
                    .child('users')
                    .child(str(user_id))
                    .get())
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la récupération de l'utilisateur {user_id} de Firebase: {e}")
            return None

    async def delete_user(self, user_id: int):
        """
        Supprime un utilisateur de la base de données Firebase.
        :param user_id: ID Telegram de l'utilisateur
        """
        try:
            if not await self._user_exists(user_id):
                return
            (self.ref
             .child('users')
             .child(str(user_id))
             .delete())
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la suppression de l'utilisateur {user_id} de Firebase: {e}")

    async def get_all_users(self) -> list[object]:
        """
        Récupère tous les utilisateurs de la base de données Firebase.
        :return: Une liste de dictionnaires contenant les informations de tous les utilisateurs
        """
        try:
            users = self.ref.child('users').get()
            if not users:
                return []
            return [user for user in users.values()]
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la récupération de tous les utilisateurs de Firebase: {e}")
            return []
        except Exception as e:
            await log_admin(f"Erreur inattendue lors de la récupération de tous les utilisateurs: {e}")
            return []

    async def set_user_prefix(self, user_id: int, prefix: str):
        """
        Définit le préfixe personnalisé d'un utilisateur.
        :param user_id: ID Telegram de l'utilisateur
        :param prefix: Le nouveau préfixe à définir
        """
        try:
            (self.ref
            .child('users')
            .child(str(user_id))
            .update(
                {'prefix': prefix}
            ))
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la définition du préfixe pour l'utilisateur {user_id}: {e}")

    async def set_user_suffix(self, user_id: int, suffix: str):
        """
        Définit le suffixe personnalisé d'un utilisateur.
        :param user_id: ID Telegram de l'utilisateur
        :param suffix: Le nouveau suffixe à définir
        """
        try:
            (self.ref
            .child('users')
            .child(str(user_id))
            .update(
                {'suffix': suffix}
            ))
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la définition du suffixe pour l'utilisateur {user_id}: {e}")

    async def set_user_thumbnail(self, user_id: int, thumbnail: str):
        """
        Définit la miniature personnalisée d'un utilisateur.
        :param user_id: ID Telegram de l'utilisateur
        :param thumbnail: Le nouveau lien de la miniature à définir
        """
        try:
            (self.ref
             .child('users')
             .child(str(user_id))
             .update(
                {'thumbnail': thumbnail}
             ))
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la définition de la miniature pour l'utilisateur {user_id}: {e}")

    async def set_user_caption(self, user_id : int, caption : str):
        """
        Défini la légende pour les uploads d'un utilisateur
        :param user_id: Telegram user id
        :param caption: La légende
        :return: None
        """
        try:
            (self.ref
             .child('users')
             .child(str(user_id))
             .update(
                {'caption': caption}
             ))
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la définition de la légende pour l'utilisateur {user_id}: {e}")

    async def get_user_caption(self, user_id : int) -> str | None:
        """
        Recupere la légende pour les uploads d'un utilisateur
        :param user_id: Telegram user id
        :return: La légende si tout se passe bien
        """
        try:
            user = await self.get_user(user_id)
            return user.get('caption') if user else None
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la récupération de la légende pour l'utilisateur {user_id}: {e}")
            return None

    async def delete_user_thumbnail(self, user_id: int):
        """
        Supprime la miniature personnalisée d'un utilisateur.
        :param user_id: ID Telegram de l'utilisateur
        """
        try:
            (self.ref
             .child('users')
             .child(str(user_id))
             .update(
                {'thumbnail': None}
             ))
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la suppression de la miniature pour l'utilisateur {user_id}: {e}")

    async def get_user_prefix(self, user_id: int) -> str | None:
        """
        Récupère le préfixe personnalisé d'un utilisateur.
        :param user_id: ID Telegram de l'utilisateur
        :return: Le préfixe de l'utilisateur ou None si aucun préfixe n'est défini
        """
        try:
            user = await self.get_user(user_id)
            return user.get('prefix') if user else None
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la récupération du préfixe pour l'utilisateur {user_id}: {e}")
            return None

    async def get_user_suffix(self, user_id: int) -> str | None:
        """
        Récupère le suffixe personnalisé d'un utilisateur.
        :param user_id: ID Telegram de l'utilisateur
        :return: Le suffixe de l'utilisateur ou None si aucun suffixe n'est défini
        """
        try:
            user = await self.get_user(user_id)
            return user.get('suffix') if user else None
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la récupération du suffixe pour l'utilisateur {user_id}: {e}")
            return None

    async def get_user_thumbnail(self, user_id: int) -> str | None:
        """
        Récupère la miniature personnalisée d'un utilisateur.
        :param user_id: ID Telegram de l'utilisateur
        :return: Le lien de la miniature de l'utilisateur ou None si aucune miniature n'est définie
        """
        try:
            user = await self.get_user(user_id)
            return user.get('thumbnail') if user else None
        except FirebaseError as e:
            await log_admin(f"Erreur lors de la récupération de la miniature pour l'utilisateur {user_id}: {e}")
            return None

bd = Database()