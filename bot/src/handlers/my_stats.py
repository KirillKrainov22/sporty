from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import httpx

from src.services.api_client import api_client

router = Router()


def _format_stats(stats: dict) -> str:
    return (
        "📊 <b>Твоя статистика</b>\n\n"
        f"Очки: <b>{stats.get('points', 0)}</b>\n"
        f"Уровень: <b>{stats.get('level', 0)}</b>\n"
        f"Всего активностей: <b>{stats.get('total_activities', 0)}</b>\n"
        f"Суммарная дистанция: <b>{stats.get('total_distance', 0)}</b>\n"
        f"Суммарная длительность: <b>{stats.get('total_duration', 0)}</b>\n"
        f"Глобальный ранг: <b>{stats.get('global_rank', '—')}</b>"
    )


async def _get_user_stats(state: FSMContext) -> dict | None:
    data = await state.get_data()
    user_id = data.get("user_id")
    if not user_id:
        return None
    return await api_client.get_user_stats(user_id)


@router.message(Command("my_stats"))
async def my_stats(message: types.Message, state: FSMContext):
    try:
        stats = await _get_user_stats(state)
    except httpx.HTTPStatusError:
        await message.answer("Не удалось получить статистику пользователя")
        return

    if not stats:
        await message.answer("Сначала нажми /start, чтобы зарегистрироваться.")
        return

    await message.answer(_format_stats(stats))


async def my_stats_screen(state: FSMContext):
    try:
        stats = await _get_user_stats(state)
    except httpx.HTTPStatusError:
        return "Не удалось получить статистику", InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
        )

    if not stats:
        return "Сначала нажми /start", InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
        )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
    )
    return _format_stats(stats), kb
