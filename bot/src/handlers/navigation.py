from aiogram import Router, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from src.utils.user_state import ensure_user_in_state

router = Router()


# функция обновления UI
async def update_screen(callback: CallbackQuery, text: str, kb: InlineKeyboardMarkup):
    """
    пытается редачить уже отправленное ботом сообщение..
    если невозможно (любой ecxeption))  и отправит  новое.
    """
    try:
        await callback.message.edit_text(text, reply_markup=kb)
    except Exception:
        await callback.message.answer(text, reply_markup=kb)


# Главное меню
def main_menu_ui():
    text = "Добро пожаловать! Выбери действие:"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить активность", callback_data="go:add_activity"),
            InlineKeyboardButton(text="Статистика", callback_data="go:my_stats"),
        ],
        [
            InlineKeyboardButton(text="Друзья", callback_data="go:friends"),
            InlineKeyboardButton(text="Достижения", callback_data="go:achievements"),
        ],
        [
            InlineKeyboardButton(text="Вызовы", callback_data="go:challenge"),
            InlineKeyboardButton(text="Лидерборд", callback_data="go:leaderboard"),
        ],
        [
            InlineKeyboardButton(text="История", callback_data="go:history"),
            InlineKeyboardButton(text="Профиль", callback_data="go:profile"),
        ]
    ])
    return text, kb


# /menu
@router.message(Command("menu"))
async def show_menu(message: types.Message):
    text, kb = main_menu_ui()
    await message.answer(text, reply_markup=kb)


# Навигация
@router.callback_query(lambda c: c.data.startswith("go:"))
async def navigate(callback: CallbackQuery, state: FSMContext):
    target = callback.data.split(":")[1]
    data = await ensure_user_in_state(state, callback)
    if not data:
        await callback.answer("Сначала нажми /start", show_alert=True)
        return
    # Главное мен
    if target == "menu":
        text, kb = main_menu_ui()
        return await update_screen(callback, text, kb)

    # Добавить активность FSM
    if target == "add_activity":
        from src.handlers.add_activity import add_activity_command
        await callback.answer()
        return await add_activity_command(callback.message, state)

    # Статистика
    if target == "my_stats":
        from src.handlers.my_stats import my_stats_screen
        text, kb = await my_stats_screen(state, callback)
        return await update_screen(callback, text, kb)

    #  Друзья
    if target == "friends":
        from src.handlers.friends import friends_screen
        text, kb = await friends_screen()
        return await update_screen(callback, text, kb)

    # Достижения
    if target == "achievements":
        from src.handlers.achievements import achievements_screen
        text, kb = await achievements_screen(state)
        return await update_screen(callback, text, kb)

    #  Вызовы
    if target == "challenge":
        from src.handlers.challenge import challenge_screen
        text, kb = await challenge_screen()
        return await update_screen(callback, text, kb)

    #  Лидербор
    if target == "leaderboard":
        from src.handlers.leaderboard import leaderboard_screen
        text, kb = await leaderboard_screen(state)
        return await update_screen(callback, text, kb)

    # История
    if target == "history":
        from src.handlers.history import history_screen
        text, kb = await history_screen()
        return await update_screen(callback, text, kb)

    #  Профиль
    if target == "profile":
        from src.handlers.profile import profile_screen

        text, kb = await profile_screen(state, callback)
        return await update_screen(callback, text, kb)

    await callback.answer()
