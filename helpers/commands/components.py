from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_settings_keyboard() -> InlineKeyboardMarkup:
    """
    Génère un clavier de paramètres avec des boutons pour les différentes options.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🖼 VOIR MINIATURE", callback_data="show_thumbnail"),
            ],
            [
                InlineKeyboardButton("📸 DÉFINIR MINIATURE", callback_data="set_thumbnail"),
            ],
            [
                InlineKeyboardButton("❌ Supprimer Miniature", callback_data="delete_thumbnail")
            ],

            [
                InlineKeyboardButton("🤖RENAME INFO", callback_data="info_rename"),
            ],

            [
                InlineKeyboardButton("ℹ️ Aide", callback_data="help"),
            ],
            [
                InlineKeyboardButton("✖️ FERMER", callback_data="close"),
            ]
        ]
    )

def generate_help_keyboard() -> InlineKeyboardMarkup:
    """
    Génère un clavier d'aide avec des boutons pour les différentes options.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("™️ A-PROPOS", callback_data="about"),
                InlineKeyboardButton("⚙️ PARAMÈTRES", callback_data="settings"),
            ],
            [
                InlineKeyboardButton("✖️ FERMER", callback_data="close"),
            ]
        ]
    )