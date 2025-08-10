from dataclasses import dataclass

from pyrogram.types import Message


@dataclass
class DownloadResult:
    chat_id : int
    file_final_name : str = None
    editable_message : Message = None
    file_path : str = None
    error : str = None
    success : bool = True


    def __str__(self):
        return f"DownloadResult(file_path={self.file_path}, file_final_name={self.file_final_name}, success={self.success}, chat_id={self.chat_id})"

