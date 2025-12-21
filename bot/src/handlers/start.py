from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import httpx

from src.handlers.navigation import main_menu_ui
from src.services.api_client import api_client

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    username = message.from_user.username

    try:
        user = await api_client.create_user(telegram_id=telegram_id, username=username)
    except httpx.HTTPStatusError:
        await message.answer(
            "Не удалось зарегистрировать пользователя в API. Попробуйте позже."
        )
        return

    await state.update_data(user_id=user["id"], telegram_id=telegram_id)

    await message.answer(
        "👋 Добро пожаловать, это Sporty Bot! Используй меню ниже:",
        reply_markup=main_menu_ui()[1],
    )
