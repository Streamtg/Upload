import re
import time

from pyrogram.types import Message

from helpers import messages
from helpers.Upload_Download.components import generate_cancel_button


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

async def progress_func(
    current : float,
    total : float,
    message : str,
    first_msg : Message,
    start : float,
) -> None:
    """
    Fonction asynchrone pour afficher la progression du téléchargement
    :param current: Taille actuelle du fichier téléchargé
    :param total: Taille totale du fichier à télécharger
    :param message: Message à afficher pendant le téléchargement
    :param first_msg: Message initial envoyé pour le téléchargement
    :param start: Temps de début du téléchargement
    :return: Rien du tout, la fonction modifie le message initial pour afficher la progression
    """
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        pourcentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        estimated_total_time = TimeFormatter(estimated_total_time)
        msg = f"{await afficher_carre(pourcentage)}\n" + \
              messages.PROGRESS.format(
                  f"{pourcentage:.2f}",
                  humanbytes(current),
                  humanbytes(total),
                  humanbytes(speed),
                  estimated_total_time if estimated_total_time != '' else "0 s"
              )
        try:
            await first_msg.edit_text(
                f'{message}\n\n{msg}',
                reply_markup=generate_cancel_button()
            )
        except:
            pass

def sanitize_filename(name):
    """
    Fonction de nettoyage basique. Merci Claude
    :param name: Nom à netoyer
    :return:
    """
    return re.sub(r'[\\/:*?"<>|!]', '', name)