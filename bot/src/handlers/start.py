from aiogram import Router, types
from aiogram.filters import Command
from src.handlers.navigation import main_menu_ui

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer(
        "👋 Добро пожаловать, это Sporty Bot! Используй меню ниже:",
        reply_markup = main_menu_ui()[1]  # [1] потому что функция возвращает (text, kb)
        # и нам нужна только клавиатура


    )