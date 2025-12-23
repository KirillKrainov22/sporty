from aiogram import Router, F
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.fsm.context import FSMContext
import httpx

from src.services.api_client import api_client

router = Router()


async def challenge_screen():
    text = (
        "⚔️ <b>Вызовы</b>\n\n"
        "Создайте вызов другу (нужен его user_id) или получите информацию о вызове по id."
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="➕ Создать вызов", callback_data="ch:create")],
            [InlineKeyboardButton(text="🔎 Получить вызов", callback_data="ch:get")],
            [InlineKeyboardButton(text="⬅ Меню", callback_data="ch:menu")],
        ]
    )
    return text, kb


async def choose_friend_screen():
    text = "Введите user_id друга для вызова (отправьте числом)"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="ch:back")]]
    )
    return text, kb


async def confirm_challenge_screen(friend_id: int):
    text = (
        f"⚔️ <b>Создать вызов для user_id {friend_id}</b>\n\n"
        "Тип соревнования можно выбрать ниже."
    )
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="По очкам", callback_data=f"ch:send:{friend_id}:points"),
                InlineKeyboardButton(text="По расстоянию", callback_data=f"ch:send:{friend_id}:distance"),
            ],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="ch:back")],
        ]
    )
    return text, kb


async def get_challenge_screen():
    text = "Отправьте id вызова, чтобы посмотреть его состояние"
    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="ch:back")]]
    )
    return text, kb


@router.callback_query(F.data == "go:challenge")
async def open_challenges(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if not data.get("user_id"):
        await callback.answer("Сначала нажми /start", show_alert=True)
        return

    await state.update_data(last_challenge_action=None)
    text, kb = await challenge_screen()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "ch:create")
async def create_challenge_start(callback: CallbackQuery, state: FSMContext):
    await state.update_data(last_challenge_action="create")
    text, kb = await choose_friend_screen()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("ch:send:"))
async def send_challenge(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split(":")
    friend_id = int(parts[2])
    ch_type = parts[3]

    data = await state.get_data()
    creator_id = data.get("user_id")
    if not creator_id:
        await callback.answer("Сначала нажми /start", show_alert=True)
        return

    try:
        challenge = await api_client.create_challenge(
            creator_id=creator_id, target_id=friend_id, type_=ch_type
        )
        text = (
            "✅ Вызов создан!\n\n"
            f"ID: {challenge.get('id')}\n"
            f"Цель: {ch_type}\n"
            f"Против user_id {friend_id}"
        )
    except httpx.HTTPStatusError:
        text = "Не удалось создать вызов. Проверьте ID друга и статус пользователей."

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅ Назад", callback_data="ch:back")]]
    )
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "ch:get")
async def request_challenge(callback: CallbackQuery, state: FSMContext):
    await state.update_data(last_challenge_action="get")
    text, kb = await get_challenge_screen()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.message(F.text.regexp(r"^\d+$"))
async def handle_numbers(message: Message, state: FSMContext):
    # this handler is used for numeric inputs on challenge screens
    data = await state.get_data()
    last_callback = data.get("last_challenge_action")

    if last_callback == "get":
        challenge_id = int(message.text)
        try:
            challenge = await api_client.get_challenge(challenge_id)
            text = (
                f"⚔️ Вызов {challenge.get('id')}\n"
                f"Создатель: {challenge.get('creator_id')}\n"
                f"Цель: {challenge.get('target_id')}\n"
                f"Тип: {challenge.get('type')}\n"
                f"Победитель: {challenge.get('winner_id')}"
            )
        except httpx.HTTPStatusError:
            text = "Не удалось получить вызов. Проверьте id."
        await message.answer(text)
    elif last_callback == "create":
        friend_id = int(message.text)
        text, kb = await confirm_challenge_screen(friend_id)
        await message.answer(text, reply_markup=kb)
    else:
        return


@router.callback_query(F.data == "ch:back")
async def back_to_challenge_menu(callback: CallbackQuery, state: FSMContext):
    await state.update_data(last_challenge_action=None)
    text, kb = await challenge_screen()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()


@router.callback_query(F.data == "ch:menu")
async def back_to_main_menu(callback: CallbackQuery):
    from src.handlers.navigation import main_menu_ui

    text, kb = main_menu_ui()
    await callback.message.edit_text(text, reply_markup=kb)
    await callback.answer()
