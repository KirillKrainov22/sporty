from aiogram import Router, F
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

router = Router()



#  FSM СОСТОЯНИЯ
class AddActivity(StatesGroup):
    choosing_type = State()
    entering_distance = State()
    entering_duration = State()


#   МОК ПОД API
def calculate_points(activity_type: str, distance: float, duration: int) -> int:
    base = {
        "run": 10,
        "bike": 5,
        "swim": 12,
        "workout": 7
    }.get(activity_type, 5)

    return int(base * distance + duration * 0.5)



# УДАЛЕНИЕ ВСЕХ СООБЩЕНИЙ FSM
async def clear_fsm_messages(state: FSMContext, event: CallbackQuery | Message):
    data = await state.get_data()

    msgs = data.get("msgs", [])
    menu_id = data.get("menu_id")  # это НЕ удаляем

    bot = event.bot

    chat_id = (
        event.message.chat.id
        if isinstance(event, CallbackQuery)
        else event.chat.id
    )

    # Удаляем все сообщения  кроме меню
    for msg_id in msgs:
        if msg_id == menu_id:
            continue
        try:
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except:
            pass

    await state.clear()



# СОХРАНЕНИЕ MESSAGE_ID
async def remember_message(state: FSMContext, message: Message):
    data = await state.get_data()
    msgs = data.get("msgs", [])
    msgs.append(message.message_id)
    await state.update_data(msgs=msgs)



#  КЛАВИАТУРА ТИПОВ АКТИВНОСТЕЙ
def activity_type_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🏃 Бег", callback_data="act:type:run"),
            InlineKeyboardButton(text="🚴 Велосипед", callback_data="act:type:bike"),
        ],
        [
            InlineKeyboardButton(text="🏊 Плавание", callback_data="act:type:swim"),
            InlineKeyboardButton(text="🏋 Тренировка", callback_data="act:type:workout"),
        ],
        [
            InlineKeyboardButton(text="❌ Отмена", callback_data="act:cancel")
        ]
    ])



# СТАРТ ADD ACTIVITY
@router.message(F.text == "/add_activity")
async def add_activity_command(message: Message, state: FSMContext):

    await state.clear()

    # сохраняем id меню чтоб потом не удалить
    await state.update_data(menu_id=message.message_id, msgs=[message.message_id])

    await state.set_state(AddActivity.choosing_type)

    msg = await message.answer(
        "🏃 <b>Выбери тип активности:</b>",
        reply_markup=activity_type_keyboard()
    )
    await remember_message(state, msg)



# ВЫБОР ТИПА АКТИВНОСТИ
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
        )
    )
    await remember_message(state, msg)



# ВВОД ДИСТАНЦИИ
@router.message(AddActivity.entering_distance)
async def input_distance(message: Message, state: FSMContext):

    # неверный ввод → просто удаляем сообщение пользователя
    txt = message.text.strip().replace(",", ".")
    try:
        value = float(txt)
        if value <= 0:
            raise ValueError
    except:
        await message.delete()
        return

    # валидный ввод
    await remember_message(state, message)
    await state.update_data(distance=value)
    await state.set_state(AddActivity.entering_duration)

    msg = await message.answer(
        f"Дистанция: <b>{value} км</b>\nВведите время (мин):",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="❌ Отмена", callback_data="act:cancel")]]
        )
    )
    await remember_message(state, msg)



# ВВОД ВРЕМЕНИ
@router.message(AddActivity.entering_duration)
async def input_duration(message: Message, state: FSMContext):

    txt = message.text.strip()

    # только положительные целые
    if not txt.isdigit() or int(txt) <= 0:
        await message.delete()
        return

    await remember_message(state, message)

    duration = int(txt)
    data = await state.get_data()

    points = calculate_points(
        data["activity_type"],
        data["distance"],
        duration
    )

    msg = await message.answer(
        f"🏁 <b>Тренировка добавлена!</b>\n\n"
        f"Тип: {data['activity_type']}\n"
        f"Дистанция: {data['distance']} км\n"
        f"Время: {duration} мин\n"
        f"Очки: <b>{points}</b>",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="➕ Добавить ещё", callback_data="act:again")],
                [InlineKeyboardButton(text="⬅ В меню", callback_data="act:menu")]
            ]
        )
    )
    await remember_message(state, msg)



# ДОБАВИТЬ ЕЩЁ
@router.callback_query(F.data == "act:again")
async def again(callback: CallbackQuery, state: FSMContext):

    await clear_fsm_messages(state, callback)
    await add_activity_command(callback.message, state)



# ОТМЕНА
@router.callback_query(F.data == "act:cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):

    await clear_fsm_messages(state, callback)
    # меню остаётся



# В МЕНЮ
@router.callback_query(F.data == "act:menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):

    await clear_fsm_messages(state, callback)
    # меню остаётся как есть