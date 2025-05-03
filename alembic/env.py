from logging.config import fileConfig

from sqlalchemy import create_engine  # 👈 added this
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ----👇 ADD THIS: import your Base ----
from app.models import Base
target_metadata = Base.metadata
# --------------------------------------


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = "sqlite:///./test.db"  # 👈 hardcoded here too just in case you want offline mode
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(  # 👈 hardcoded here
        "sqlite:///./test.db",
        connect_args={"check_same_thread": False},
        poolclass=pool.NullPool
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
