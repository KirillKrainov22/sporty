from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User


async def get_or_create_user(
    session: AsyncSession,
    telegram_id: int,
    username: str | None = None,
):
    """
    Достаёт пользователя по telegram_id.
    Если не найден — создаёт нового, сохраняет в БД и возвращает.
    """

    # 1. Пытаемся найти пользователя
    result = await session.execute(
        select(User).where(User.telegram_id == telegram_id)
    )
    user = result.scalar_one_or_none()

    if user is not None:
        return user

    # 2. Если не нашли — создаём
    user = User(
        telegram_id=telegram_id,
        username=username,
        # если в модели created_at стоит server_default=func.now(),
        # можно НЕ передавать created_at — БД сама поставит значение.
        # если будет ругаться на лишний аргумент, просто убери его.
        # created_at=datetime.utcnow(),
        points=0,
        level=1,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user
