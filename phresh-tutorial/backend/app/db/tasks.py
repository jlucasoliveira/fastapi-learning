from databases import Database
from fastapi import FastAPI

from ..core.config import DATABASE_URL
from ..utils import handle_exception


async def connect_to_db(app: FastAPI) -> None:
    database = Database(DATABASE_URL, min_size=2, max_size=10)

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
