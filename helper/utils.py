from aiohttp import ClientSession
from config import Config

async def log_admin(log_text : str, scope : str = "[Renamer Bot]") -> None:
    """
     Fonction asynchrone pour se notifier sur le bon fonctionnement l'execution du code, fpnctio fonctionne
     directement par l'API brut de Telegram Bot (Requete GET HTTP)
    :param log_text: Texte à recevoir
    :type log_text: str
    :param scope: Scope dans lequel la fonction est executé afin de facilité le deboguage
    :type scope: str
    :return: Rien du tout, si l'envoi de la notification ne reussit pas, on affiche l'erreur dans la console
    :rtype: None
    """
    url = f"https://api.telegram.org/bot{Config.LOG_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id" : Config.DEVELOPPER_ID,
        "text" : f"[{scope}] : {log_text}"
    }
    async with ClientSession() as session:
        try:
            async with session.post(url, data=data) as response:
                if response.status != 200:
                    print("❌ Échec de la notification Telegram vers vous meme")
        except Exception as e:
            print(f"❌ Erreur notification: {e}\n\nErreur voulu envoyé : [{scope}] : {text}")