from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()

# FSM: состояния
class AddActivityStates(StatesGroup):
    choosing_type = State()
    entering_data = State()


# /add_activity
@router.message(Command("add_activity"))
async def add_activity_command(message: types.Message, state: FSMContext):
    kb = InlineKeyboardBuilder()
    kb.button(text="🏃 Бег", callback_data="type_run")
    kb.button(text="🚴 Велосипед", callback_data="type_bicycle")
    kb.button(text="🏊 Плавание", callback_data="type_swim")
    kb.button(text="💪 Тренировка", callback_data="type_workout")
    kb.adjust(2)

    await message.answer(
        "Выбери тип активности:",
        reply_markup=kb.as_markup()
    )

    await state.set_state(AddActivityStates.choosing_type)


# обработка выбора активности
@router.callback_query(F.data.startswith("type_"))
async def choose_type(callback: types.CallbackQuery, state: FSMContext):
    activity_type = callback.data.replace("type_", "")

    await state.update_data(activity_type=activity_type)
    await state.set_state(AddActivityStates.entering_data)

    await callback.message.answer(
        "Введи дистанцию (км) и время (мин). Пример:\n\n"
        "<b>5 28</b>"
    )
    await callback.answer()


# получаем ввод пользователя (дистанция + время)
@router.message(AddActivityStates.entering_data)
async def process_data(message: types.Message, state: FSMContext):
    try:
        distance_str, duration_str = message.text.split()
        distance = float(distance_str)
        duration = int(duration_str)
    except:
        await message.answer("❌ Формат некорректен.\nПример: <b>5 28</b>")
        return

    if distance <= 0 or duration <= 0:
        await message.answer("❌ Значения должны быть положительными.")
        return

    # достаём тип активности
    data = await state.get_data()
    activity_type = data["activity_type"]

    # МОК — заглушка отправки в API
    # потом заменим на реальный запрос requests.post(...)
    points = calculate_mock_points(activity_type, distance)

    await message.answer(
        f"🏆 Тренировка добавлена!\n\n"
        f"<b>{distance} км</b> за <b>{duration} мин</b>\n"
        f"→ <b>+{points} очков</b> 🎉"
    )

    await state.clear()


# простая функция — временная заглушка
def calculate_mock_points(activity_type: str, distance: float) -> int:
    base = {
        "run": 10,
        "bicycle": 5,
        "swim": 15,
        "workout": 8
    }
    return int(distance * base.get(activity_type, 5))
