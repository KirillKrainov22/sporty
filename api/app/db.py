from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Базовый класс моделей
Base = declarative_base()

# Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,  # поставить True, если нужно видеть SQL в логах
    future=True,
)

# Фабрика сессий (асинхронная)
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Получение сессии (используется в роутерах)
async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
