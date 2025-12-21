from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import httpx

from src.services.api_client import api_client
from src.utils.user_state import ensure_user_in_state

router = Router()


def _format_username(username: str | None) -> str:
    if not username:
        return "—"
    return f"@{username}"

async def _load_user(state: FSMContext, event: types.Message | CallbackQuery | None = None) -> tuple[
    int | None, str | None]:
    data = await ensure_user_in_state(state, event)
    if not data:
        return None, None
    return data.get("user_id"), data.get("telegram_id")

async def profile_screen(state: FSMContext, event: types.Message | CallbackQuery | None = None):
    user_id, telegram_id = await _load_user(state, event)


    if not telegram_id:
        return "Сначала нажми /start", InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
        )

    try:
        user = await api_client.get_user_by_telegram_id(telegram_id)
    except httpx.HTTPStatusError:
        return "Не удалось загрузить профиль", InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
        )

    text = (
        "👤 <b>Профиль</b>\n\n"
        f"Имя: {_format_username(user.get('username'))}\n"
        f"Telegram ID: <code>{telegram_id}</code>\n"
        f"Очки: <b>{user.get('points', 0)}</b>\n"
        f"Уровень: <b>{user.get('level', 0)}</b>\n"
        f"User ID: <code>{user_id or user.get('id')}</code>"
    )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
    )

    return text, kb


@router.message(Command("profile"))
async def profile_handler(message: types.Message, state: FSMContext):
    text, kb = await profile_screen(state, message)
    await message.answer(text, reply_markup=kb)