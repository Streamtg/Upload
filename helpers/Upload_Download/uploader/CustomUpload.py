import time


from pyrogram import Client
from globals import messages
from helpers.Upload_Download.uploader.UploadResult import UploadResult
from helpers.Upload_Download.uploader.ffmpeg import take_screen_shot, extract_duration

from helpers.Upload_Download.utils import progress_func, TimeFormatter


async def upload_file(
        bot: Client,
        file : object,
        thumbnail: str | None = None,
        caption: str | None = None
) -> UploadResult:
    """
    Fonction pour Uploader un fichier local vers Telegram
    :param thumbnail: Miniature du fichier à envoyer (optionnel)
    :param caption: Légende du fichier à envoyer (optionnel)
    :param bot: Une instance du bot
    :param file: Un objet DownloadResult contenant les attributs nécessaires
    :return: un objet UploadResult
    """
    try:
        #Si l'utilisateur n'a pas spécifié de miniature, on en prend une aléatoire
        duration = 0
        if not thumbnail:
            try:
                # On essaye d'extraire la durée du fichier pour prendre un moment aléatoire
                duration = await extract_duration(file.file_path)
                # On prend un moment aléatoire dans la durée du fichier
                if duration:
                    random_moment = int(time.time() * 1000) % duration if duration > 0 else 0
                    thumbnail = await take_screen_shot(file.file_path, str(file.chat_id), random_moment)
            except:
                pass
        if "{duration}" in caption:
            if duration > 0:
                duration /= 1000    #Conversion en millisecondes pour la fonction TimeFormatter
            caption = caption.format(duration=TimeFormatter(duration))

        await file.editable_message.edit_text(messages.FILE_UPLOADING)
        start = time.time()
        send_file = await bot.send_document(
            chat_id=file.chat_id,
            document=file.file_path,
            caption=caption,
            thumb=thumbnail,
            progress=progress_func,
            progress_args=(
                messages.FILE_UPLOADING,
                file.editable_message,
                start)
        )
        end = time.time()
        if send_file:
            await file.editable_message.delete()
            return UploadResult(
                chat_id=file.chat_id,
                duration= end - start,
                file_path=file.file_path,
            )
        else:
            await file.editable_message.edit_text(messages.FILE_UPLOAD_FAILED)
            return UploadResult(
                chat_id=file.chat_id,
                duration=0,
                file_path=file.file_path,
                success=False
            )
    except Exception as e:
        await file.editable_message.edit_text(messages.FILE_UPLOAD_FAILED)
        return UploadResult(
            chat_id=file.chat_id,
            duration=0,
            file_path=file.file_path,
            success=False,
            error=str(e)
        )






