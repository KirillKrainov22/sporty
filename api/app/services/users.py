from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from app.schemas.user import UserCreate
from datetime import datetime

async def register_user(db: AsyncSession, data: UserCreate) -> User:
    # Проверяем, есть ли такой пользователь
    result = await db.execute(
        select(User).where(User.telegram_id == data.telegram_id)
    )
    existing = result.scalars().first()

    if existing:
        return existing  # возвращаем его же (бот может несколько раз вызывать /start)

    new_user = User(
        telegram_id=data.telegram_id,
        username=data.username,
        created_at=datetime.utcnow(),
        points=0,
        level=1
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def get_user(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()
