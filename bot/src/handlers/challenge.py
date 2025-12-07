from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

router = Router()


#заглушки (вместо API)


# список друзей — в будущем будет приходить из API
FAKE_FRIENDS = ["kirill", "maxim", "dima"]

# активные вызовы пользователя (created)
FAKE_ACTIVE_CHALLENGES = []

# входящие вызовы пользователя (incoming)
FAKE_INCOMING_CHALLENGES = []



# FSM для создания вызова
class ChallengeState(StatesGroup):
    choosing_friend = State()
    choosing_type = State()



# /challenge меню
@router.message(Command("challenge"))
async def challenge_menu(message: types.Message):

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать вызов", callback_data="challenge_create")],
        [InlineKeyboardButton(text="Мои вызовы", callback_data="challenge_my")],
        [InlineKeyboardButton(text="Входящие вызовы", callback_data="challenge_incoming")],
    ])

    await message.answer("Выбери действие:", reply_markup=keyboard)



# Создать вызов → Выбор друга
@router.callback_query(lambda c: c.data == "challenge_create")
async def start_challenge(callback: CallbackQuery, state: FSMContext):

    # Генерируем список друзей
    keyboard = []
    for friend in FAKE_FRIENDS:
        keyboard.append([
            InlineKeyboardButton(
                text=friend,
                callback_data=f"challenge_friend:{friend}"
            )
        ])

    await callback.message.answer("Выбери друга:", reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    await state.set_state(ChallengeState.choosing_friend)
    await callback.answer()


#Пользователь выбрал друга → выбор типа вызова
@router.callback_query(lambda c: c.data.startswith("challenge_friend:"))
async def choose_challenge_type(callback: CallbackQuery, state: FSMContext):

    friend = callback.data.split(":")[1]

    # сохраняем выбранного друга во временное состояние FSM
    await state.update_data(friend=friend)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Бег", callback_data="challenge_type:run")],
        [InlineKeyboardButton(text="Шаги", callback_data="challenge_type:steps")],
        [InlineKeyboardButton(text="Время", callback_data="challenge_type:time")],
    ])

    await callback.message.answer(f"Выбран: {friend}\nТеперь выбери тип вызова:", reply_markup=keyboard)
    await state.set_state(ChallengeState.choosing_type)
    await callback.answer()



# Пользователь выбрал тип → создаём вызов
@router.callback_query(lambda c: c.data.startswith("challenge_type:"))
async def create_challenge(callback: CallbackQuery, state: FSMContext):

    data = await state.get_data()
    friend = data["friend"]

    challenge_type = callback.data.split(":")[1]

    # Создаём объект вызова в заглушке
    challenge = {
        "friend": friend,
        "type": challenge_type,
        "status": "pending"
    }

    # Добавляем "как будто" в БД
    FAKE_ACTIVE_CHALLENGES.append(challenge)
    FAKE_INCOMING_CHALLENGES.append(challenge)  # симуляция входящего вызова у друга

    await state.clear()
    await callback.message.answer(f"Вызов отправлен пользователю {friend}.")
    await callback.answer()


# Мои вызовы (созданные)
@router.callback_query(lambda c: c.data == "challenge_my")
async def show_my_challenges(callback: CallbackQuery):

    if not FAKE_ACTIVE_CHALLENGES:
        await callback.message.answer("У тебя нет активных вызовов.")
        await callback.answer()
        return

    text = "<b>Твои вызовы:</b>\n\n"
    for ch in FAKE_ACTIVE_CHALLENGES:
        text += f"• {ch['friend']} — {ch['type']} — статус: {ch['status']}\n"

    await callback.message.answer(text)
    await callback.answer()


#  Входящие вызовы (incoming)
@router.callback_query(lambda c: c.data == "challenge_incoming")
async def show_incoming(callback: CallbackQuery):

    if not FAKE_INCOMING_CHALLENGES:
        await callback.message.answer("Нет входящих вызовов.")
        await callback.answer()
        return

    text = "<b>Входящие вызовы:</b>\n\n"

    keyboard = []
    for idx, ch in enumerate(FAKE_INCOMING_CHALLENGES):
        text += f"• {ch['friend']} — {ch['type']}\n"
        keyboard.append([
            InlineKeyboardButton(text="Принять", callback_data=f"challenge_accept:{idx}"),
            InlineKeyboardButton(text="Отклонить", callback_data=f"challenge_decline:{idx}")
        ])

    await callback.message.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard))
    await callback.answer()



#   Принять вызов
@router.callback_query(lambda c: c.data.startswith("challenge_accept:"))
async def accept_challenge(callback: CallbackQuery):

    idx = int(callback.data.split(":")[1])
    ch = FAKE_INCOMING_CHALLENGES.pop(idx)
    ch["status"] = "accepted"
    FAKE_ACTIVE_CHALLENGES.append(ch)

    await callback.message.answer("Вызов принят.")
    await callback.answer()



#Отклонить вызов
@router.callback_query(lambda c: c.data.startswith("challenge_decline:"))
async def decline_challenge(callback: CallbackQuery):

    idx = int(callback.data.split(":")[1])
    FAKE_INCOMING_CHALLENGES[idx]["status"] = "declined"

    await callback.message.answer("Вызов отклонён.")
    await callback.answer()


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def challenge_screen():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать вызов", callback_data="challenge_create")],
        [InlineKeyboardButton(text="Мои вызовы", callback_data="challenge_my")],
        [InlineKeyboardButton(text="Входящие вызовы", callback_data="challenge_incoming")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="go:menu")],
    ])

    return "Меню вызовов:", kb
