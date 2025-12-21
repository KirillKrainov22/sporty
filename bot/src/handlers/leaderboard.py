from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
import httpx

from src.services.api_client import api_client

router = Router()


async def _fetch_leaderboard(user_id: int | None = None):
    if user_id:
        return await api_client.get_friends_leaderboard(user_id)
    return await api_client.get_leaderboard()


@router.message(Command("leaderboard"))
async def leaderboard_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    try:
        leaderboard = await _fetch_leaderboard(user_id)
    except httpx.HTTPStatusError:
        await message.answer("Не удалось получить лидерборд")
        return

    if not leaderboard:
        await message.answer("Пока никого нет в таблице лидеров 😢")
        return

    text = "🏆 <b>Таблица лидеров Sporty</b>\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for index, user in enumerate(leaderboard, start=1):
        medal = medals[index - 1] if index <= 3 else f"{index}."
        username = user.get("username") or str(user.get("user_id"))
        points = user.get("points", 0)
        text += f"{medal} <b>{username}</b> — {points} очков\n"

    await message.answer(text)


async def leaderboard_screen(state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    try:
        leaderboard = await _fetch_leaderboard(user_id)
    except httpx.HTTPStatusError:
        return "Не удалось получить лидерборд", InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
        )

    if not leaderboard:
        return "Пока никого нет в таблице лидеров 😢", InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
        )

    text = "🏆 <b>Таблица лидеров Sporty</b>\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for index, user in enumerate(leaderboard, start=1):
        medal = medals[index - 1] if index <= 3 else f"{index}."
        username = user.get("username") or str(user.get("user_id"))
        text += f"{medal} <b>{username}</b> — {user.get('points', 0)} очков\n"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
    )

    return text, kb
