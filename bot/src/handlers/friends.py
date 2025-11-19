from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

# FSM для корректного ввода username
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()

# ------------------------------
#  ЗАГЛУШКИ (потом заменятся API)
# ------------------------------

# Список текущих друзей
FAKE_FRIENDS = ["kirill", "maxim", "dima"]

# Список входящих заявок в друзья
FAKE_REQUESTS = ["anton"]

# Список всех пользователей (имитация БД)
ALL_USERS = ["kirill", "maxim", "dima", "anton", "sergey"]


async def fake_find_user(username: str):
    """Имитация поиска пользователя в БД."""
    return username if username in ALL_USERS else None


# ------------------------------
#     FSM СОСТОЯНИЯ
# ------------------------------

class AddFriendState(StatesGroup):
    waiting_for_username = State()


# --------------------------------
#       КОМАНДА /friends
# --------------------------------

@router.message(Command("friends"))
async def friends_menu(message: types.Message):
    """Главное меню управления друзьями."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕ Добавить друга", callback_data="friends_add")],
        [InlineKeyboardButton(text="📋 Мои друзья", callback_data="friends_list")],
        [InlineKeyboardButton(text="✔ Принять заявки", callback_data="friends_requests")],
    ])

    await message.answer("Выбери действие:", reply_markup=keyboard)


# --------------------------------
#     НАЧАЛО ДОБАВЛЕНИЯ ДРУГА
# --------------------------------

@router.callback_query(lambda c: c.data == "friends_add")
async def add_friend_start(callback: CallbackQuery, state: FSMContext):
    """Сообщаем пользователю, чтобы он ввёл username друга."""
    await callback.message.answer(
        "Введи username пользователя, которого хочешь добавить.\n\n"
        "Например: <b>maxim</b>"
    )
    await state.set_state(AddFriendState.waiting_for_username)
    await callback.answer()


# --------------------------------
#     ОБРАБОТКА ВВОДА USERNAME
# --------------------------------

@router.message(AddFriendState.waiting_for_username)
async def add_friend_process(message: types.Message, state: FSMContext):
    username = message.text.strip().lower()

    # Ищем пользователя
    found = await fake_find_user(username)
    if not found:
        await message.answer("❌ Пользователь не найден.")
        return

    if username in FAKE_FRIENDS:
        await message.answer("⚠ Этот пользователь уже в твоих друзьях.")
        return

    if username in FAKE_REQUESTS:
        await message.answer("⚠ Заявка этому пользователю уже отправлена.")
        return

    # Добавляем заявку
    FAKE_REQUESTS.append(username)

    await message.answer(f"📨 Заявка отправлена пользователю <b>{username}</b>!")
    await state.clear()


# --------------------------------
#      СПИСОК ДРУЗЕЙ
# --------------------------------

@router.callback_query(lambda c: c.data == "friends_list")
async def show_friends(callback: CallbackQuery):

    if not FAKE_FRIENDS:
        await callback.message.answer("У тебя пока нет друзей 😢")
        await callback.answer()
        return

    text = "👥 <b>Твои друзья</b>:\n\n"
    for f in FAKE_FRIENDS:
        text += f"• {f}\n"

    await callback.message.answer(text)
    await callback.answer()


# --------------------------------
#      ВХОДЯЩИЕ ЗАЯВКИ
# --------------------------------

@router.callback_query(lambda c: c.data == "friends_requests")
async def show_requests(callback: CallbackQuery):

    if not FAKE_REQUESTS:
        await callback.message.answer("Нет новых заявок 🙌")
        await callback.answer()
        return

    text = "📝 <b>Заявки в друзья</b>:\n\n"

    # Кнопки "Принять"
    keyboard = []
    for username in FAKE_REQUESTS:
        keyboard.append([
            InlineKeyboardButton(
                text=f"✔ Принять: {username}",
                callback_data=f"accept_friend:{username}"
            )
        ])

    await callback.message.answer(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard)
    )

    await callback.answer()


# --------------------------------
#      ПРИНЯТЬ ДРУГА
# --------------------------------

@router.callback_query(lambda c: c.data.startswith("accept_friend:"))
async def accept_friend(callback: CallbackQuery):
    """
    Принимаем заявку: перемещаем друга
    FAKE_REQUESTS → FAKE_FRIENDS.
    """

    username = callback.data.split(":", 1)[1]

    # убираем из заявок
    if username in FAKE_REQUESTS:
        FAKE_REQUESTS.remove(username)

    # добавляем в друзья
    if username not in FAKE_FRIENDS:
        FAKE_FRIENDS.append(username)

    await callback.message.answer(
        f"🎉 Пользователь <b>{username}</b> теперь твой друг!"
    )

    await callback.answer()
