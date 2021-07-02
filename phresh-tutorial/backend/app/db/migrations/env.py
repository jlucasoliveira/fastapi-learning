import sys
import pathlib
import logging
from logging.config import fileConfig
import alembic
from psycopg2 import DatabaseError
from sqlalchemy import (
    pool,
    create_engine,
    engine_from_config,
)
from app.core.config import DATABASE_URL, TESTING

sys.path.append(str(pathlib.Path(__file__).resolve().parents[3]))

config = alembic.context.config

fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    """

    DB_NAME = DATABASE_URL.database
    _DATABASE_URL = f"{DATABASE_URL}_test" if TESTING else str(DATABASE_URL)

    if TESTING:
        default_engine = create_engine(str(DATABASE_URL), isolation_level="AUTOCOMMIT")
        with default_engine.connect() as default_conn:
            default_conn.execute(f"DROP DATABASE IF EXISTS {DB_NAME}_test")
            default_conn.execute(f"CREATE DATABASE {DB_NAME}_test")

    connectable = config.attributes.get("connection", None)
    config.set_main_option("sqlalchemy.url", str(_DATABASE_URL))

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

    if TESTING:
        raise DatabaseError("Running testing migrations offline currently not permitted.")

    alembic.context.configure(url=str(DATABASE_URL))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


if alembic.context.is_offline_mode():
    logger.info("Running migrations offline")
    run_migrations_offline()
else:
    logger.info("Running migrations online")
    run_migrations_online()
