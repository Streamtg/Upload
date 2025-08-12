from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_cancel_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ANNULER❌", callback_data="cancel_download_all")]
        ]
    )

def generate_rename_or_not_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("📄DEFAULT", callback_data=f"download"),
                InlineKeyboardButton("✏️ RENOMMER", callback_data=f"rename")
            ],
            [InlineKeyboardButton("ANNULER❌", callback_data=f"cancel_download")]
        ]
    )

def add_prefix_suffix(base_name : str, prefix :str, suffix : str) -> str:
    final_name = f"{prefix if prefix else ''} {base_name} {suffix if suffix else ''}"
    return final_name.strip()

async def parse_caption(file_data : "helpers.Upload_Download.downloader.ReadyToDownload import ReadyToDownload", custom_caption : str) -> str:
    return custom_caption.format(filename = file_data.filename, filesize = file_data.file_size, duration='{duration}')
