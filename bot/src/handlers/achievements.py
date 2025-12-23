from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import httpx

from src.services.api_client import api_client

router = Router()


async def _fetch_achievements(state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    if not user_id:
        return None
    return await api_client.get_user_achievements(user_id)


@router.message(Command("achievements"))
async def achievements_handler(message: types.Message, state: FSMContext):
    try:
        achievements = await _fetch_achievements(state)
    except httpx.HTTPStatusError:
        achievements = None

    if not achievements:
        await message.answer("Достижения пока недоступны. Нажми /start и попробуй снова.")
        return

    earned_text = "<b>Полученные достижения:</b>\n"
    unearned_text = "\n<b>Недоступные достижения:</b>\n"

    has_earned = False
    has_unearned = False

    for ach in achievements:
        if ach.get("earned"):
            earned_text += f"• {ach.get('title')} ({ach.get('code')})\n"
            has_earned = True
        else:
            unearned_text += f"• {ach.get('title')} ({ach.get('code')})\n"
            has_unearned = True

    text = ""
    text += earned_text if has_earned else "<b>Полученных достижений нет.</b>\n"
    text += unearned_text if has_unearned else ""

    await message.answer(text)


async def achievements_screen(state: FSMContext):
    try:
        achievements = await _fetch_achievements(state)
    except httpx.HTTPStatusError:
        achievements = None

    if not achievements:
        return (
            "Достижения пока недоступны. Нажми /start и попробуй снова.",
            InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
            ),
        )

    earned = "<b>Полученные достижения:</b>\n"
    unearned = "\n<b>Недоступные достижения:</b>\n"
    has_e = False
    has_u = False

    for ach in achievements:
        if ach.get("earned"):
            earned += f"• {ach.get('title')} ({ach.get('code')})\n"
            has_e = True
        else:
            unearned += f"• {ach.get('title')} ({ach.get('code')})\n"
            has_u = True

    text = ""
    text += earned if has_e else "<b>Полученных достижений нет.</b>\n"
    text += unearned if has_u else ""

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
    )

    return text, kb
