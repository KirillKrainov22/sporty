from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

router = Router()


#      ЗАГЛУШКИ (потом API)
# Пример списка достижений (как будто из БД)
# earned=True  → пользователь получил достижение
# earned=False → пока нет
FAKE_ACHIEVEMENTS = [
    {"code": "first_run", "title": "Первый забег", "earned": True},
    {"code": "100km_month", "title": "Марафонец (100 км за месяц)", "earned": False},
    {"code": "streak_10", "title": "Серия 10 дней подряд", "earned": True},
    {"code": "friends_10", "title": "10 добавленных друзей", "earned": False},
    {"code": "challenge_winner", "title": "Победить 5 вызовов", "earned": False},
]


async def get_user_achievements():
    """
    возвращает достижения пользователя.
    сейчас заглушка

    Потом здесь будет запрос к API:
    формат должен совпадать с FAKE_ACHIEVEMENTS.
    """
    return FAKE_ACHIEVEMENTS


# КОМАНДА /achievements
@router.message(Command("achievements"))
async def achievements_handler(message: types.Message):
    """
    Показывает список достижений пользователя.
    Делим на: полученные / не полученные.
    """

    achievements = await get_user_achievements()

    if not achievements:
        await message.answer("Достижений пока нет.")
        return

    earned_text = "<b>Полученные достижения:</b>\n"
    unearned_text = "\n<b>Недоступные достижения:</b>\n"

    has_earned = False
    has_unearned = False

    # Формируем текст
    for ach in achievements:
        if ach["earned"]:
            earned_text += f"• {ach['title']}\n"
            has_earned = True
        else:
            unearned_text += f"• {ach['title']}\n"
            has_unearned = True

    text = ""

    if has_earned:
        text += earned_text
    else:
        text += "<b>Полученных достижений нет.</b>\n"

    if has_unearned:
        text += unearned_text

    await message.answer(text)



from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
# экран
async def achievements_screen():
    achievements = FAKE_ACHIEVEMENTS

    if not achievements:
        return "Достижений пока нет.", InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]]
        )

    earned = "<b>Полученные достижения:</b>\n"
    unearned = "\n<b>Недоступные достижения:</b>\n"
    has_e = False
    has_u = False

    for ach in achievements:
        if ach["earned"]:
            earned += f"• {ach['title']}\n"
            has_e = True
        else:
            unearned += f"• {ach['title']}\n"
            has_u = True

    text = ""
    text += earned if has_e else "<b>Полученных достижений нет.</b>\n"
    text += unearned if has_u else ""

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")]
    ])

    return text, kb


