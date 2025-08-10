from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_cancel_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("ANNULER❌", callback_data="cancel_download")]
        ]
    )
