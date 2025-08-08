from dataclasses import dataclass

@dataclass
class DownloadResult:
    file_path : str
    file_final_name : str
    success : bool
    chat_id : int

    def __str__(self):
        return f"DownloadResult(file_path={self.file_path}, file_final_name={self.file_final_name}, success={self.success}, chat_id={self.chat_id})"

