from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import httpx

from src.services.api_client import api_client
from src.utils.user_state import ensure_user_in_state, clear_state_preserve_user

router = Router()


class AddActivity(StatesGroup):
    choosing_type = State()
    entering_distance = State()
    entering_duration = State()


async def clear_fsm_messages(state: FSMContext, event: CallbackQuery | Message):
    data = await state.get_data()
    msgs = data.get("msgs", [])
    menu_id = data.get("menu_id")

    bot = event.bot
    chat_id = event.message.chat.id if isinstance(event, CallbackQuery) else event.chat.id

    for msg_id in msgs:
        if msg_id == menu_id:
            continue
        try:
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except Exception:
            pass

    await state.update_data(msgs=[])


async def remember_message(state: FSMContext, message: Message):
    data = await state.get_data()
    msgs = data.get("msgs", [])
    msgs.append(message.message_id)
    await state.update_data(msgs=msgs)



def activity_type_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🏃 Бег", callback_data="act:type:run"),
                InlineKeyboardButton(text="🚴 Велосипед", callback_data="act:type:bike"),
            ],
            [
                InlineKeyboardButton(text="🏊 Плавание", callback_data="act:type:swim"),
                InlineKeyboardButton(text="🏋 Тренировка", callback_data="act:type:workout"),
            ],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="act:cancel")],
        ]
    )


@router.message(F.text == "/add_activity")
async def add_activity_command(message: Message, state: FSMContext):
    existing_data = await ensure_user_in_state(state, message)
    if not existing_data or not existing_data.get("user_id"):
        await message.answer("Сначала нажми /start, чтобы зарегистрироваться.")
        return

    user_id = existing_data.get("user_id")
    telegram_id = existing_data.get("telegram_id")
    username = existing_data.get("username")
    await clear_state_preserve_user(state)
    await state.update_data(
        user_id=user_id,
        telegram_id=telegram_id,
        username=username,
        menu_id=message.message_id,
        msgs=[message.message_id],
    )
    await state.set_state(AddActivity.choosing_type)

    msg = await message.answer("🏃 <b>Выбери тип активности:</b>", reply_markup=activity_type_keyboard())
    await remember_message(state, msg)


@router.callback_query(F.data.startswith("act:type"))
async def choose_activity_type(callback: CallbackQuery, state: FSMContext):
    await clear_fsm_messages(state, callback)
    activity_type = callback.data.split(":")[2]
    await state.update_data(activity_type=activity_type)
    await state.set_state(AddActivity.entering_distance)

    msg = await callback.message.answer(
        f"Вы выбрали: <b>{activity_type}</b>\nВведите дистанцию (км):",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="act:cancel")]]
        ),
    )
    await remember_message(state, msg)


@router.message(AddActivity.entering_distance)
async def input_distance(message: Message, state: FSMContext):
    txt = message.text.strip().replace(",", ".")
    try:
        value = float(txt)
        if value <= 0:
            raise ValueError
    except Exception:
        await message.delete()
        return

    await remember_message(state, message)
    await state.update_data(distance=value)
    await state.set_state(AddActivity.entering_duration)

    msg = await message.answer(
        f"Дистанция: <b>{value} км</b>\nВведите время (мин):",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="act:cancel")]]
        ),
    )
    await remember_message(state, msg)


@router.message(AddActivity.entering_duration)
async def input_duration(message: Message, state: FSMContext):
    txt = message.text.strip()
    if not txt.isdigit() or int(txt) <= 0:
        await message.delete()
        return

    await remember_message(state, message)

    duration = int(txt)
    data = await ensure_user_in_state(state, message)
    user_id = data.get("user_id") if data else None
    if not user_id:
        await message.answer("Сначала нажми /start, чтобы зарегистрироваться.")
        await clear_state_preserve_user(state)
        return

    try:
        activity = await api_client.create_activity(
            user_id=user_id,
            type_=data.get("activity_type"),
            distance=data.get("distance"),
            duration=duration,
        )
    except httpx.HTTPStatusError:
        await message.answer("Не удалось сохранить активность. Попробуйте ещё раз.")
        await clear_state_preserve_user(state)
        return

    points = activity.get("points", 0) if isinstance(activity, dict) else 0

    msg = await message.answer(
        f"🏁 <b>Тренировка добавлена!</b>\n\n"
        f"Тип: {data.get('activity_type')}\n"
        f"Дистанция: {data.get('distance')} км\n"
        f"Время: {duration} мин\n"
        f"Очки: <b>{points}</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="➕ Добавить ещё", callback_data="act:again")],
                [InlineKeyboardButton(text="⬅ В меню", callback_data="act:menu")],
            ]
        ),
    )
    await remember_message(state, msg)


@router.callback_query(F.data == "act:again")
async def again(callback: CallbackQuery, state: FSMContext):
    await clear_fsm_messages(state, callback)
    await add_activity_command(callback.message, state)


@router.callback_query(F.data == "act:cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    await clear_fsm_messages(state, callback)
    await clear_state_preserve_user(state)


@router.callback_query(F.data == "act:menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await clear_fsm_messages(state, callback)
    await clear_state_preserve_user(state)
