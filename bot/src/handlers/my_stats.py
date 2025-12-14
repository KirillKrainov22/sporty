from aiogram import Router, types
from aiogram.filters import Command
import requests
from src.services import api_client
from src.services.api_client import ApiError
from aiogram.fsm.context import FSMContext

router = Router()


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def my_stats_screen(state: FSMContext, telegram_id: int, username: str | None):
    data = await state.get_data()
    user_id = data.get("user_id")

    if not user_id:
        user = api_client.ensure_user(telegram_id, username)
        user_id = user["id"]
        await state.update_data(user_id=user_id)

    stats = api_client.get_user_stats(user_id)

    text = (
        "📊 <b>Твоя статистика</b>\n\n"
        f"Очки: <b>{stats['points']}</b>\n"
        f"Уровень: <b>{stats['level']}</b>\n"
        f"Место в рейтинге: <b>{stats['global_rank']}</b>\n\n"
        f"Всего активностей: <b>{stats['total_activities']}</b>\n"
        f"Дистанция всего: <b>{stats['total_distance']}</b> км\n"
        f"Время всего: <b>{int(stats['total_duration'] / 60)}</b> мин\n"
    )

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]
    ])

    return text, kb
