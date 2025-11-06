from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
import os
import sys

# Добавляем корневую директорию проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import Base
from app.core.config import settings
from app.incidents.model import Incident  # noqa

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    return settings.database_url


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio
    try:
        asyncio.run(run_migrations_online())
    except Exception as e:
        error_msg = str(e)
        if "getaddrinfo" in error_msg or "connect" in error_msg.lower() or "connection" in error_msg.lower():
            print("\n" + "="*70)
            print("ОШИБКА: Не удалось подключиться к базе данных!")
            print("="*70)
            print(f"\nURL подключения: {get_url()}")
            print("\nВозможные решения:")
            print("1. Убедитесь, что PostgreSQL запущен локально")
            print("2. Проверьте настройки подключения в .env файле или app/core/config.py")
            print("3. Для создания миграции без подключения используйте:")
            print("   alembic revision -m 'Initial'")
            print("   (но autogenerate не будет работать без БД)")
            print("\n" + "="*70)
        raise

