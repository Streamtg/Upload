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