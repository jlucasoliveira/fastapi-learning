import os
import warnings

import alembic
import pytest
from alembic.config import Config
from app.db.repositories.cleanings import CleaningRepository
from app.models.cleaning import CleaningCreate, CleaningInDB, CleaningType
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from httpx import AsyncClient


@pytest.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "True"
    config = Config("alembic.ini")

    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture
def app(apply_migrations: None) -> FastAPI:
    from app.api.server import get_application

    return get_application()


@pytest.fixture
def db(app: FastAPI) -> Database:
    return app.state._db


@pytest.fixture
async def client(app: FastAPI) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://localhost:8000",
            headers={"Content-Type": "application/json"},
        ) as client:
            yield client


@pytest.fixture
async def test_cleaning(db: Database) -> CleaningInDB:
    cleaning_repo = CleaningRepository(db)
    new_cleaning = CleaningCreate(
        name="mocked cleaning name",
        description="mocked cleaning description",
        price=99.9,
        cleaning_type=CleaningType.spot_clean,
    )

    return await cleaning_repo.create_cleaning(obj=new_cleaning)
