import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import app.models.group  # noqa: F401
import app.models.relationships  # noqa: F401
import app.models.role  # noqa: F401
import app.models.user  # noqa: F401
from app.models.base import Base

target_metadata = Base.metadata

config = context.config
fileConfig(config.config_file_name)


def get_url() -> str:
    url = os.getenv("USER_DB_URL") or "postgresql://user:password@postgres/user_db"
    print(f"Using database URL: {url}")
    return url.replace("+asyncpg", "")


def run_migrations_online() -> None:
    alembic_cfg = context.config
    alembic_cfg.set_main_option("sqlalchemy.url", get_url())

    connectable = engine_from_config(
        alembic_cfg.get_section(alembic_cfg.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    print(f"Online - URL: {get_url()}")

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()


def run_migrations_offline() -> None:
    # Run migrations in 'offline' mode.
    context.configure(
        url=get_url(),
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    print(f"Offline - URL: {get_url()}")

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
