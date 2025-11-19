import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.config import BOT_TOKEN
from src.handlers import start as start_handlers
from src.handlers import add_activity as add_activity_handlers
from src.handlers import my_stats as my_stats_handlers

## aiogram 3.x полностью асинхронный, поэтому main — это async-функция:
async def main():
    print(">>> STARTING BOT...")

    # Создаём бота с HTML-форматированием по умолчанию
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Подключаем обработчики команд
    dp.include_router(start_handlers.router)
    dp.include_router(add_activity_handlers.router)
    dp.include_router(my_stats_handlers.router)

    print("🤖 Bot is running...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
