from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import httpx

from src.services.api_client import api_client

router = Router()


class AddFriendFSM(StatesGroup):
    entering_id = State()


async def clear_friends_messages(state: FSMContext, event: CallbackQuery | Message):
    data = await state.get_data()
    msgs = data.get("friends_msgs", [])
    menu_id = data.get("menu_id")

    bot = event.bot
    chat_id = event.message.chat.id if isinstance(event, CallbackQuery) else event.chat.id

    for msg_id in msgs:
        if msg_id == menu_id:
            continue
        try:
            await bot.delete_message(chat_id, msg_id)
        except Exception:
            pass

    await state.update_data(friends_msgs=[])


async def remember(state: FSMContext, msg: Message):
    data = await state.get_data()
    arr = data.get("friends_msgs", [])
    arr.append(msg.message_id)
    await state.update_data(friends_msgs=arr)


def friends_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📃 Список друзей", callback_data="fr:list")],
            [InlineKeyboardButton(text="➕ Добавить друга", callback_data="fr:add")],
            [InlineKeyboardButton(text="⬅ Меню", callback_data="fr:menu")],
        ]
    )


async def friends_screen():
    return "👥 <b>Друзья</b>\n\nВыбери действие:", friends_keyboard()


async def friends_list_screen(user_id: int):
    try:
        friends = await api_client.get_user_friends(user_id)
    except httpx.HTTPStatusError:
        friends = None

    if not friends:
        text = "У тебя пока нет друзей или запрос не удался"
    else:
        text = "👥 <b>Твои друзья:</b>\n\n"
        for f in friends:
            text += (
                f"• связь {f.get('id')} — user_id={f.get('user_id')} ↔ friend_id={f.get('friend_id')}"
                f" (статус: {f.get('status')})\n"
            )

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="fr:back")]]
    )
    return text, kb


async def add_friend_screen():
    text = "Введите user_id друга для отправки запроса"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Отмена", callback_data="fr:cancel")]]
    )
    return text, kb


@router.callback_query(F.data == "go:friends")
async def open_friends(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")

    if not user_id:
        await callback.answer("Сначала нажми /start 🙂", show_alert=True)
        return

    await clear_friends_messages(state, callback)
    await state.update_data(menu_id=callback.message.message_id, friends_msgs=[callback.message.message_id])

    text, kb = await friends_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


@router.callback_query(F.data == "fr:back")
async def back_from_friends(callback: CallbackQuery, state: FSMContext):
    await clear_friends_messages(state, callback)
    text, kb = await friends_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


@router.callback_query(F.data == "fr:list")
async def show_list(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    await clear_friends_messages(state, callback)

    text, kb = await friends_list_screen(user_id)
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


@router.callback_query(F.data == "fr:add")
async def add_friend(callback: CallbackQuery, state: FSMContext):
    await clear_friends_messages(state, callback)
    await state.set_state(AddFriendFSM.entering_id)
    text, kb = await add_friend_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


@router.message(AddFriendFSM.entering_id)
async def input_friend_id(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text.isdigit():
        await message.delete()
        return

    friend_id = int(text)
    data = await state.get_data()
    user_id = data.get("user_id")
    await remember(state, message)

    try:
        await api_client.add_friend(user_id=user_id, friend_id=friend_id)
        msg = await message.answer(
            f"Заявка отправлена пользователю с ID {friend_id}",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="fr:back")]]
            ),
        )
        await remember(state, msg)
    except httpx.HTTPStatusError:
        msg = await message.answer(
            "Не удалось отправить запрос в друзья. Проверьте ID пользователя.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="fr:back")]]
            ),
        )
        await remember(state, msg)
    finally:
        await state.clear()


@router.callback_query(F.data == "fr:cancel")
async def cancel_add_friend(callback: CallbackQuery, state: FSMContext):
    await clear_friends_messages(state, callback)
    await state.clear()
    text, kb = await friends_screen()
    msg = await callback.message.answer(text, reply_markup=kb)
    await remember(state, msg)
    await callback.answer()


@router.callback_query(F.data == "fr:menu")
async def exit_to_menu(callback: CallbackQuery, state: FSMContext):
    await clear_friends_messages(state, callback)
    await state.clear()
    await callback.answer()
