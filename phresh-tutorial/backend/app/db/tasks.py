from app.core.config import DATABASE_URL, TESTING
from app.utils import handle_exception
from databases import Database
from fastapi import FastAPI


async def connect_to_db(app: FastAPI) -> None:
    _DATABASE_URL = f"{DATABASE_URL}_test" if TESTING else DATABASE_URL
    database = Database(_DATABASE_URL, min_size=2, max_size=10)

    try:
        await database.connect()
        app.state._db = database
    except Exception as e:
        handle_exception("DB CONNECTION", e)


async def close_db_connection(app: FastAPI) -> None:
    try:
        await app.state._db.disconnect()
    except Exception as e:
        handle_exception("DB DISCONNECTION", e)
