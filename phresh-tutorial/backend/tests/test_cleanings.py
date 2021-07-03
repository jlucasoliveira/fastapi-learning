import pytest
from app.models.cleaning import CleaningCreate, CleaningType
from fastapi import FastAPI, status
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


@pytest.fixture
def new_cleaning() -> CleaningCreate:
    return CleaningCreate(
        name="test cleaning",
        description="test description",
        price=0.0,
        cleaning_type=CleaningType.spot_clean,
    )


class TestCleaningsRoutes:
    async def test_routes_exist(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("cleanings:create-cleaning"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND

    async def test_invalid_input_raises_error(self, app: FastAPI, client: AsyncClient) -> None:
        res = await client.post(app.url_path_for("cleanings:create-cleaning"), json={})
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCleaningCreate:
    async def test_valid_input_create_cleaning(
        self, app: FastAPI, client: AsyncClient, new_cleaning: CleaningCreate
    ) -> None:
        res = await client.post(app.url_path_for("cleanings:create-cleaning"), json=new_cleaning.dict())
        assert res.status_code == status.HTTP_201_CREATED

        created_cleaning = CleaningCreate(**res.json())
        assert created_cleaning == new_cleaning
