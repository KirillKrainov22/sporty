from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import httpx

from src.services.api_client import api_client


USER_KEYS = ("user_id", "telegram_id", "username")


def _extract_event_user(event: CallbackQuery | Message | None) -> tuple[int | None, str | None]:
    if not event:
        return None, None

    user = event.from_user if isinstance(event, (CallbackQuery, Message)) else None
    if not user:
        return None, None

    return user.id, user.username


async def ensure_user_in_state(
    state: FSMContext, event: CallbackQuery | Message | None = None
):
    """Guarantee user data is available in FSM state.

    If the state is missing ``user_id`` or ``telegram_id``, the function will try to
    restore it from the incoming event and refresh the data from the API.
    """

    data = await state.get_data()
    if data.get("user_id") and data.get("telegram_id"):
        return data

    telegram_id, username = _extract_event_user(event)
    if not telegram_id:
        return None

    try:
        user = await api_client.get_user_by_telegram_id(telegram_id)
    except httpx.HTTPStatusError:
        return None

    await state.update_data(
        user_id=user.get("id"),
        telegram_id=telegram_id,
        username=username or user.get("username"),
    )
    return await state.get_data()


async def clear_state_preserve_user(state: FSMContext):
    """Clear FSM data but keep user identifiers in place."""

    data = await state.get_data()
    user_data = {key: data.get(key) for key in USER_KEYS if data.get(key) is not None}

    await state.clear()

    if user_data:
        await state.update_data(**user_data)

    return user_data