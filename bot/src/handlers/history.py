from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==================================================
#        API-заглушка (ПОТОМ ЗАМЕНИМ НА HTTP)
# ==================================================
async def get_history_data(user_id: int):
    """
    Сейчас возвращает заглушку.
    Потом здесь будет запрос к API наример такой:

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"http://api:8000/history/{user_id}"
        ) as resp:
            return await resp.json()
    """
    return [
        {
            "date": "12.12.2025",
            "type": "Бег",
            "distance": 5,
            "time": 30,
            "points": 120,
        },
        {
            "date": "11.12.2025",
            "type": "Ходьба",
            "distance": 3,
            "time": 40,
            "points": 80,
        },
    ]



# UI-ЭКРАН

async def history_screen(user_id: int | None = None):
    history = await get_history_data(user_id)

    if not history:
        text = "📜 <b>История тренировок</b>\n\nТренировок пока нет."
    else:
        lines = ["📜 <b>История тренировок</b>\n"]
        for h in history:
            lines.append(
                f"• {h['date']} — {h['type']}\n"
                f"  {h['distance']} км · {h['time']} мин · {h['points']} очков\n"
            )
        text = "\n".join(lines)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]
    ])

    return text, kb
