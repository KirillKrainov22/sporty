from aiogram import Router, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()

#   Заглушечные данные
FAKE_FRIENDS = ["kirill", "maxim", "anton"]

FAKE_MY_CHALLENGES = [
    {"id": 1, "to": "maxim", "text": "Кто наберёт больше очков за неделю?"},
]

FAKE_INCOMING_CHALLENGES = [
    {"id": 2, "from": "kirill", "text": "Кто пробежит больше км за месяц?"},
]



#   Базовые экраны
async def challenge_screen():
    text = (
        "⚔️ <b>Вызовы</b>\n\n"
        "Здесь можно посмотреть свои вызовы, входящие и создать новый."
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📤 Мои вызовы", callback_data="ch:my")],
        [InlineKeyboardButton(text="📥 Входящие вызовы", callback_data="ch:incoming")],
        [InlineKeyboardButton(text="➕ Создать вызов", callback_data="ch:create")],
        [InlineKeyboardButton(text="⬅ Меню", callback_data="ch:menu")],
    ])
    return text, kb
    ## функция прост возвр данные для UI


async def my_challenges_screen():
    if not FAKE_MY_CHALLENGES:
        text = "📤 <b>Мои вызовы</b>\n\nПока нет активных вызовов."
    else:
        # если есть то формируем список
        lines = ["📤 <b>Мои вызовы</b>\n"]
        for ch in FAKE_MY_CHALLENGES:
            lines.append(f"• @{ch['to']}: {ch['text']}")
        text = "\n".join(lines)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅ Назад", callback_data="ch:back")],
    ])
    return text, kb

# экран входящих вызовов
async def incoming_challenges_screen():
    if not FAKE_INCOMING_CHALLENGES:
        text = "📥 <b>Входящие вызовы</b>\n\nНовых вызовов нет."
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅ Назад", callback_data="ch:back")],
        ])
        return text, kb

    lines = ["📥 <b>Входящие вызовы</b>\n"]
    kb_rows = []
    ## проходим по всем и создаем 2 кнопки для каждого (принять и отклонить)
    for ch in FAKE_INCOMING_CHALLENGES:
        lines.append(f"• @{ch['from']}: {ch['text']}")
        kb_rows.append([
            InlineKeyboardButton(text="✔ Принять", callback_data=f"ch:accept:{ch['id']}"),
            InlineKeyboardButton(text="✖ Отклонить", callback_data=f"ch:decline:{ch['id']}"),
        ])

    kb_rows.append([InlineKeyboardButton(text="⬅ Назад", callback_data="ch:back")])

    text = "\n".join(lines)
    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    return text, kb

## создание вызова и выбор друга
async def choose_friend_screen():
    text = "👤 <b>Создание вызова</b>\n\nВыбери друга, которому хочешь бросить вызов:"
    rows = []
    for friend in FAKE_FRIENDS:
        rows.append([
            InlineKeyboardButton(
                text=f"@{friend}",
                callback_data=f"ch:friend:{friend}"
            )
        ])
    rows.append([InlineKeyboardButton(text="⬅ Назад", callback_data="ch:back")])
    kb = InlineKeyboardMarkup(inline_keyboard=rows)
    return text, kb


async def confirm_challenge_screen(friend: str):
    text = (
        f"⚔️ <b>Создать вызов для @{friend}</b>\n\n"
        "Пока это заглушка: реальная логика (тип, цель, сроки) появится после подключения API.\n\n"
        "Отправить тестовый вызов?"
    )
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Отправить вызов", callback_data=f"ch:send:{friend}")],
        [InlineKeyboardButton(text="⬅ Назад", callback_data="ch:create")],
    ])
    return text, kb


# Обработчики колбэков (они выводят экраныыыыы)

@router.callback_query(F.data == "ch:my")
async def show_my_challenges(callback: CallbackQuery):
    text, kb = await my_challenges_screen()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
    ## тут от my_challenges_screen прилетают данные и бот отвечает (callback.answer())


@router.callback_query(F.data == "ch:incoming")
async def show_incoming_challenges(callback: CallbackQuery):
    text, kb = await incoming_challenges_screen()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "ch:create")
async def create_challenge_start(callback: CallbackQuery):
    text, kb = await choose_friend_screen()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("ch:friend:"))
async def choose_friend(callback: CallbackQuery):
    friend = callback.data.split(":")[2]
    text, kb = await confirm_challenge_screen(friend)
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("ch:send:"))
async def send_challenge(callback: CallbackQuery):
    friend = callback.data.split(":")[2]

    # здесь можно будет дергать API; сейчас — просто добавляем в FAKE_MY_CHALLENGES
    FAKE_MY_CHALLENGES.append({
        "id": max([c["id"] for c in FAKE_MY_CHALLENGES] + [0]) + 1,
        "to": friend,
        "text": "Тестовый вызов (заглушка)",
    })

    text, kb = await my_challenges_screen()
    await callback.message.edit_text(
        "✅ Вызов отправлен!\n\n" + text,
        reply_markup=kb,
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("ch:accept:"))
async def accept_challenge(callback: CallbackQuery):
    ch_id = int(callback.data.split(":")[2])
    # имитация: убираем из входящих
    for ch in list(FAKE_INCOMING_CHALLENGES):
        if ch["id"] == ch_id:
            FAKE_INCOMING_CHALLENGES.remove(ch)
            break

    text, kb = await incoming_challenges_screen()
    await callback.message.edit_text(
        "✔ Вызов принят!\n\n" + text,
        reply_markup=kb,
    )
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("ch:decline:"))
async def decline_challenge(callback: CallbackQuery):
    ch_id = int(callback.data.split(":")[2])
    # имитация: убираем из входящих
    for ch in list(FAKE_INCOMING_CHALLENGES):
        if ch["id"] == ch_id:
            FAKE_INCOMING_CHALLENGES.remove(ch)
            break

    text, kb = await incoming_challenges_screen()
    await callback.message.edit_text(
        "✖ Вызов отклонён.\n\n" + text,
        reply_markup=kb,
    )
    await callback.answer()


@router.callback_query(F.data == "ch:back")
async def back_to_challenge_menu(callback: CallbackQuery):
    text, kb = await challenge_screen()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "ch:menu")
async def back_to_main_menu(callback: CallbackQuery):
    # возвращаемся в главное меню бота
    from src.handlers.navigation import main_menu_ui

    text, kb = main_menu_ui()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
