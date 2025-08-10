#Fichier Python pour contenir les configurations du bot

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    PORT = os.getenv("PORT", "10000")

    DEVELOPPER_ID = int(os.getenv("DEVELOPPER_ID"))

    LOG_BOT_TOKEN = int(os.getenv("LOG_BOT_TOKEN"))

    DOWNLOAD_DIR = "./downloads/"

    FIREBASE_URL = os.getenv("FIREBASE_URL")

    FIREBASE_KEY = os.getenv("FIREBASE_KEY")

