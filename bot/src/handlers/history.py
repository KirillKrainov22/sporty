from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def history_screen(user_id: int | None = None):
    text = (
        "📜 <b>История тренировок</b>\n\n"
        "История недоступна: текущий API не предоставляет эндпоинт для списка активностей."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]])
    return text, kb
