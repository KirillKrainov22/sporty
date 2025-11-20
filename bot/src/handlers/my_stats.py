from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("my_stats"))

async def my_stats(message: types.Message):
    stats = get_mock_stats()

    text = (
        "📊 <b>Твоя статистика</b>\n\n"
        f"За сегодня: <b>{stats['today']} очков</b>\n"
        f"За неделю: <b>{stats['week']} очков</b>\n"
        f"За месяц: <b>{stats['month']} очков</b>\n\n"
        f"Всего тренировок: <b>{stats['total_workouts']}</b>\n"
        f"Средняя активность: <b>{stats['avg_daily']} км/день</b>"
    )

    await message.answer(text)


def get_mock_stats():
    # Здесь позже будет запрос в API:
    # response = requests.get(...)
    # return response.json()
    #

    return {
        "today": 150,
        "week": 420,
        "month": 1200,
        "total_workouts": 17,
        "avg_daily": 5.3
    }
