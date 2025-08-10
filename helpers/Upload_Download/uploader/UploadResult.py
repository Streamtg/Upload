from dataclasses import dataclass

@dataclass
class UploadResult:
    duration: float
    file_path: str
    chat_id : int
    success: bool = True
    error: str | None = None

