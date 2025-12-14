from aiogram import Router, types
from aiogram.filters import Command
from src.handlers.navigation import main_menu_ui
from aiogram.fsm.context import FSMContext
from src.services import api_client
from src.services.api_client import ApiError
import requests

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    username = message.from_user.username  # может быть None

    try:
        user = api_client.ensure_user(telegram_id=telegram_id, username=username)
        await state.update_data(user_id=user["id"])
    except (requests.exceptions.RequestException, ApiError):
        await message.answer("⚠️ Сервис временно недоступен. Попробуй позже.")
        return

    await message.answer(
        "👋 Добро пожаловать, это Sporty Bot! Используй меню ниже:",
        reply_markup=main_menu_ui()[1]
    )
