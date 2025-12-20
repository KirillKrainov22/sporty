import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool


# добавляем в sys.path папку api, чтобы импортировать app.*
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from app.core.config import settings
from app.models import Base  # noqa

def make_sync_database_url(async_url: str) -> str:
    """Преобразуем asyncpg-URL к psycopg2 для Alembic."""
    if async_url.startswith("postgresql+asyncpg"):
        return async_url.replace("+asyncpg", "+psycopg2", 1)
    return async_url

# ---- НАСТРОЙКИ ПОДКЛЮЧЕНИЯ К БД ДЛЯ ALEMBIC ----
SYNC_DATABASE_URL = make_sync_database_url(settings.DATABASE_URL)
# Alembic Config
config = context.config

# подставляем URL (на всякий случай)
config.set_main_option("sqlalchemy.url", SYNC_DATABASE_URL)

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные наших моделей
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн-режиме (без реального подключения)."""
    context.configure(
        url=SYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме (с подключением к БД)."""
    connectable = create_engine(
        SYNC_DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
#для коммита