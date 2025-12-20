import os
from dotenv import load_dotenv

load_dotenv()  # ищет .env в папке bot

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("❌ BOT_TOKEN не найден! Добавь его в файл .env в папке bot")
