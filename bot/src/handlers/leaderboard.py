from aiogram import Router, types
from aiogram.filters import Command
router = Router()

# ВРЕМЕННАЯ ЗАГЛУШКА — потом заменим на запрос в API
FAKE_LEADERBOARD = [
    {"username": "kirill", "points": 1200},
    {"username": "maxim",  "points": 950},
    {"username": "dima",   "points": 800},
    {"username": "anton",  "points": 500},
]


async def get_leaderboard_data():
    """
    Сейчас: возвращает заглушку.
    Потом: здесь будет запрос к API, типо:
      async with aiohttp.ClientSession() as session:
          async with session.get("http://api:8000/api/leaderboard") as resp:
              return await resp.json()
    """
    return FAKE_LEADERBOARD


@router.message(Command("leaderboard"))
async def leaderboard_handler(message: types.Message):
    leaderboard = await get_leaderboard_data()

    if not leaderboard:
        await message.answer("Пока никого нет в таблице лидеров 😢")
        return

    text = "🏆 <b>Таблица лидеров Sporty</b>\n\n"

    medals = ["🥇", "🥈", "🥉"]

    for index, user in enumerate(leaderboard, start=1):
        medal = medals[index - 1] if index <= 3 else f"{index}."
        username = user.get("username", "—")
        points = user.get("points", 0)
        text += f"{medal} <b>{username}</b> — {points} очков\n"

    await message.answer(text)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def leaderboard_screen():
    leaderboard = FAKE_LEADERBOARD

    if not leaderboard:
        return "Пока никого нет в таблице лидеров 😢", InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
        )

    text = "🏆 <b>Таблица лидеров Sporty</b>\n\n"
    medals = ["🥇", "🥈", "🥉"]

    for index, user in enumerate(leaderboard, start=1):
        medal = medals[index - 1] if index <= 3 else f"{index}."
        text += f"{medal} <b>{user['username']}</b> — {user['points']} очков\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]
    ])

    return text, kb
