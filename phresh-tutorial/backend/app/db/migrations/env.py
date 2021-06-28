import sys
import pathlib
import logging
from logging.config import fileConfig
import alembic
from sqlalchemy import (
    pool,
    engine_from_config,
)
from app.core.config import DATABAS_URL

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

config = alembic.context.config

fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", str(DATABAS_URL))

    if not connectable:
        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

    with connectable.connect() as connection:
        alembic.context.configure(
            connection=connection,
            target_metada=None,
        )

        with alembic.context.begin_transaction():
            alembic.context.run_migrations()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    """

    alembic.context.configure(url=str(DATABAS_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
