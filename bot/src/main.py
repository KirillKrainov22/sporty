import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from src.config import BOT_TOKEN
from src.handlers import start as start_handlers
from src.handlers import add_activity as add_activity_handlers
from src.handlers import my_stats as my_stats_handlers
from src.handlers import leaderboard as leaderboard_handlers  # NEW
from src.handlers import friends as friends_handlers
from src.handlers import achievements as achievements_handlers
from src.handlers import challenge as challenge_handlers
from src.handlers import navigation as navigation_handlers


async def main():
    print(">>> STARTING BOT...")

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        #задаёт дефолтные свойства чтобы tg понимал HTML-теги в текстах).

    )
    dp = Dispatcher()

    # Подключаем обработчики команд
    dp.include_router(start_handlers.router)
    dp.include_router(add_activity_handlers.router)
    dp.include_router(my_stats_handlers.router)
    dp.include_router(leaderboard_handlers.router)
    dp.include_router(friends_handlers.router)
    dp.include_router(achievements_handlers.router)
    dp.include_router(challenge_handlers.router)
    dp.include_router(navigation_handlers.router)

    print("🤖 Bot is running...")
    await dp.start_polling(bot)


# as
if __name__ == "__main__":
    asyncio.run(main())