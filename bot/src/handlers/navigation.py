from aiogram import Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
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

@router.message(Command("menu"))
async def show_menu(message):
    await message.answer("Выбери действие:", reply_markup=main_menu_kb())

@router.callback_query(lambda c: c.data.startswith("go:"))
async def navigate(callback: CallbackQuery, state: FSMContext):
    target = callback.data.split(":")[1]
    msg = callback.message

    if target == "add_activity":
        from src.handlers.add_activity import add_activity_command
        await add_activity_command(msg, state)

    elif target == "my_stats":
        from src.handlers.my_stats import my_stats
        await my_stats(msg)

    elif target == "friends":
        from src.handlers.friends import friends_menu
        await friends_menu(msg)

    elif target == "achievements":
        from src.handlers.achievements import achievements_handler
        await achievements_handler(msg)

    elif target == "challenge":
        from src.handlers.challenge import challenge_menu
        await challenge_menu(msg)

    elif target == "leaderboard":
        from src.handlers.leaderboard import leaderboard_handler
        await leaderboard_handler(msg)

    elif target == "history":
        await msg.answer("История пока не реализована.")

    elif target == "profile":
        await msg.answer("Профиль пока не реализован.")

    await callback.answer()
