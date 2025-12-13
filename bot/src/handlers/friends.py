from aiogram import Router, F
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    CallbackQuery, Message
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

router = Router()


# ===============================
#      MOCK DATA (заменим на API)
# ===============================
FAKE_FRIENDS = ["kirill", "maxim", "anton"]
FAKE_REQUESTS = ["petya", "maria"]


# ===============================
#       FSM — ввод username
# ===============================
class AddFriendFSM(StatesGroup):
    entering_username = State()


# ===============================
#     УТИЛИТА ДЛЯ ИДЕАЛЬНОГО UX
# ===============================
async def clear_friends_messages(state: FSMContext, event: CallbackQuery | Message):
    """Удаляет ВСЕ сообщения, связанные с экраном 'Друзья',
    оставляя только меню, как в add_activity."""
    data = await state.get_data()
    msgs = data.get("friends_msgs", [])
    menu_id = data.get("menu_id")  # меню НЕ трогаем

    bot = event.bot
    chat_id = (
        event.message.chat.id
        if isinstance(event, CallbackQuery)
        else event.chat.id
    )

    for msg_id in msgs:
        if msg_id == menu_id:
            continue
        try:
            await bot.delete_message(chat_id, msg_id)
        except:
            pass

    await state.update_data(friends_msgs=[])


async def remember(state: FSMContext, msg: Message):
    """Запоминает message_id для последующего удаления."""
    data = await state.get_data()
    arr = data.get("friends_msgs", [])
    arr.append(msg.message_id)
    await state.update_data(friends_msgs=arr)


# ===========================================================
#          ГЛАВНОЕ МЕНЮ ДРУЗЕЙ
# ===========================================================
async def friends_screen():
    text = "👥 <b>Друзья</b>\n\nВыбери действие:"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📃 Список друзей", callback_data="fr:list")],
        [InlineKeyboardButton(text=f"📬 Заявки ({len(FAKE_REQUESTS)})", callback_data="fr:req")],
        [InlineKeyboardButton(text="➕ Добавить друга", callback_data="fr:add")],
        [InlineKeyboardButton(text="⬅ Меню", callback_data="fr:menu")],

    ])
    return text, kb


# ===========================================================
#            СПИСОК ДРУЗЕЙ
# ===========================================================
async def friends_list_screen():
    if not FAKE_FRIENDS:
        text = "У тебя пока нет друзей 😢"
    else:
        text = "👥 <b>Твои друзья:</b>\n\n"
        for f in FAKE_FRIENDS:
            text += f"• {f}\n"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад", callback_data="fr:back")]
    ])
    return text, kb


# ===========================================================
#           СПИСОК ЗАЯВОК
# ===========================================================
async def friend_requests_screen():
    if not FAKE_REQUESTS:
        text = "📭 У тебя нет входящих заявок."
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data="fr:back")]
        ])
        return text, kb

    text = "📬 <b>Входящие заявки:</b>\n\n"
    kb_rows = []

    for user in FAKE_REQUESTS:
        kb_rows.append([
            InlineKeyboardButton(text=f"@{user}", callback_data="none"),
            InlineKeyboardButton(text="✔", callback_data=f"fr:accept:{user}"),
            InlineKeyboardButton(text="✖", callback_data=f"fr:decline:{user}")
        ])

    kb_rows.append([InlineKeyboardButton(text="⬅ Назад", callback_data="fr:back")])

    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    return text, kb


# ===========================================================
#           ДОБАВИТЬ ДРУГА (ввод username)
# ===========================================================
async def add_friend_screen():
    text = "Введите username друга (через @):"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Отмена", callback_data="fr:cancel")]
    ])
    return text, kb


# ===========================================================
#      ОБРАБОТЧИКИ CALLBACK
# ===========================================================
@router.callback_query(F.data == "go:friends")
async def open_friends(callback: CallbackQuery, state: FSMContext):
    """Открыть главное меню друзей"""
    await clear_friends_messages(state, callback)

    # сохранить id меню
    await state.update_data(menu_id=callback.message.message_id,
                            friends_msgs=[callback.message.message_id])

    text, kb = await friends_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


@router.callback_query(F.data == "fr:back")
async def back_from_friends(callback: CallbackQuery, state: FSMContext):
    """Вернуться в главное меню друзей"""
    await clear_friends_messages(state, callback)

    text, kb = await friends_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


@router.callback_query(F.data == "fr:list")
async def show_list(callback: CallbackQuery, state: FSMContext):
    await clear_friends_messages(state, callback)

    text, kb = await friends_list_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


@router.callback_query(F.data == "fr:req")
async def show_requests(callback: CallbackQuery, state: FSMContext):
    await clear_friends_messages(state, callback)

    text, kb = await friend_requests_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


# принять заявку
@router.callback_query(lambda c: c.data.startswith("fr:accept"))
async def accept_request(callback: CallbackQuery, state: FSMContext):
    user = callback.data.split(":")[2]
    if user in FAKE_REQUESTS:
        FAKE_REQUESTS.remove(user)
        FAKE_FRIENDS.append(user)

    await show_requests(callback, state)


# отклонить заявку
@router.callback_query(lambda c: c.data.startswith("fr:decline"))
async def decline_request(callback: CallbackQuery, state: FSMContext):
    user = callback.data.split(":")[2]
    if user in FAKE_REQUESTS:
        FAKE_REQUESTS.remove(user)

    await show_requests(callback, state)


# добавить друга
@router.callback_query(F.data == "fr:add")
async def add_friend(callback: CallbackQuery, state: FSMContext):
    await clear_friends_messages(state, callback)
    await state.set_state(AddFriendFSM.entering_username)

    text, kb = await add_friend_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


# ввод username друга
@router.message(AddFriendFSM.entering_username)
async def input_friend(message: Message, state: FSMContext):

    # неверный ввод — удаляем сообщение и продолжаем ждать
    username = message.text.strip()
    await remember(state, message)

    if not username.startswith("@") or len(username) < 3:
        await message.delete()
        return

    # имитация добавления
    FAKE_REQUESTS.append(username[1:])

    msg = await message.answer(
        f"Заявка отправлена пользователю {username}!",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="fr:back")]]
        )
    )
    await remember(state, msg)

    await state.clear()

@router.callback_query(F.data == "fr:cancel")
async def cancel_add_friend(callback: CallbackQuery, state: FSMContext):
    await clear_friends_messages(state, callback)
    await state.clear()

    # Вернуться в главное меню друзей
    text, kb = await friends_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()

@router.callback_query(F.data == "fr:menu")
async def exit_to_menu(callback: CallbackQuery, state: FSMContext):
    # Удаляем все сообщения friends FSM
    await clear_friends_messages(state, callback)
    await state.clear()

    # НЕ отправляем меню заново — оно уже есть в чате
    await callback.answer()
