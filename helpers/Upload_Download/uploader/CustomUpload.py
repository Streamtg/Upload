import time


from pyrogram import Client
from globals import messages
from helpers.Upload_Download.uploader.UploadResult import UploadResult

from helpers.Upload_Download.utils import progress_func


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






