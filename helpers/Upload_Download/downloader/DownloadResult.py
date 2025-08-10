from dataclasses import dataclass

from pyrogram.types import Message
from helpers.Upload_Download.uploader.CustomUpload import upload_file
from helpers.Upload_Download.uploader.UploadResult import UploadResult


@dataclass
class DownloadResult:
    chat_id : int
    file_final_name : str = None
    editable_message : Message = None
    file_path : str = None
    error : str = None
    success : bool = True

    async def upload_file(self, bot, caption : str = None, thumbnail : str = None) -> UploadResult:
        """
        Upload un fichier téléchargé vers Telegram.
        """
        if not caption:
            caption = self.file_final_name if self.file_final_name else "Fichier téléchargé"

        upload_result = await upload_file(
            bot,
            self,
            caption=caption,
            thumbnail=thumbnail
        )
        return upload_result


    def __str__(self):
        return f"DownloadResult(file_path={self.file_path}, file_final_name={self.file_final_name}, success={self.success}, chat_id={self.chat_id})"

