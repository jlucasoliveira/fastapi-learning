from typing import List, Optional, Union

import pytest
from app.models.cleaning import CleaningCreate, CleaningInDB, CleaningType
from httpx import AsyncClient

from fastapi import FastAPI, status

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


class TestCreateCleaning:
    async def test_valid_input_create_cleaning(
        self, app: FastAPI, client: AsyncClient, new_cleaning: CleaningCreate
    ) -> None:
        res = await client.post(app.url_path_for("cleanings:create-cleaning"), json=new_cleaning.dict())
        assert res.status_code == status.HTTP_201_CREATED

        created_cleaning = CleaningCreate(**res.json())
        assert created_cleaning == new_cleaning

    @pytest.mark.parametrize(
        "invalid_input, status_code",
        (
            (None, 422),
            ({}, 422),
            ({"name": "test_name"}, 422),
            ({"price": 10.0}, 422),
            ({"name": "test_name", "description": "test"}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
        self, app: FastAPI, client: AsyncClient, invalid_input: Optional[dict], status_code: int
    ) -> None:
        res = await client.post(app.url_path_for("cleanings:create-cleaning"), json=invalid_input)
        assert res.status_code == status_code


class TestGetCleaning:
    async def test_get_cleaning_by_id(self, app: FastAPI, client: AsyncClient, test_cleaning: CleaningInDB) -> None:
        res = await client.get(app.url_path_for("cleanings:retrieve-cleaning-by-id", id=test_cleaning.id))
        assert res.status_code == status.HTTP_200_OK

        cleaning = CleaningInDB(**res.json())
        assert cleaning == test_cleaning

    @pytest.mark.parametrize(
        "id, status_code",
        (
            (None, 422),
            (99, 404),
            (-99, 404),
        ),
    )
    async def test_get_cleaning_raises_error(
        self, app: FastAPI, client: AsyncClient, id: Optional[int], status_code: int
    ) -> None:
        res = await client.get(app.url_path_for("cleanings:retrieve-cleaning-by-id", id=id))
        assert res.status_code == status_code

    async def test_get_all_cleanings_returns_valid_response(
        self, app: FastAPI, client: AsyncClient, test_cleaning: CleaningInDB
    ) -> None:
        res = await client.get(app.url_path_for("cleanings:list-cleanings"))
        assert res.status_code == status.HTTP_200_OK
        assert isinstance(res.json(), list)
        assert len(res.json()) > 0
        cleanings = [CleaningInDB(**item) for item in res.json()]
        assert test_cleaning in cleanings


class TestUpdateCleaning:
    @pytest.mark.parametrize(
        "attrs_to_change, values",
        (
            (["name"], ["new mock name to cleaning"]),
            (["description"], ["new mock description"]),
            (["price"], [92.3]),
            (["cleaning_type"], [CleaningType.full_clean]),
            (["name", "description"], ["extra new mock cleaning name", "oh yah! new description too"]),
            (["price", "cleaning_type"], [19.72, CleaningType.dust_up]),
        ),
    )
    async def test_update_cleaning_with_valid_input(
        self,
        app: FastAPI,
        client: AsyncClient,
        test_cleaning: CleaningInDB,
        attrs_to_change: List[str],
        values: List[Union[str, float]],
    ) -> None:
        to_update_cleaning = {attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))}
        res = await client.put(
            app.url_path_for("cleanings:update-cleaning", id=test_cleaning.id),
            json=to_update_cleaning,
        )
        assert res.status_code == status.HTTP_200_OK
        cleaning = CleaningInDB(**res.json())
        assert cleaning.id == test_cleaning.id

        # Testa se os atributos foram alteredos e se foram alterados do campo certo
        for i in range(len(attrs_to_change)):
            assert getattr(cleaning, attrs_to_change[i]) != getattr(test_cleaning, attrs_to_change[i])
            assert getattr(cleaning, attrs_to_change[i]) == values[i]

        # Testa se apenas os atributos enviados foram mudados
        for attr, value in cleaning.dict().items():
            if attr not in attrs_to_change:
                assert getattr(test_cleaning, attr) == value

    @pytest.mark.parametrize(
        "id, payload, status_code",
        (
            (-1, {"name": "test"}, 422),
            (0, {"name": "test2"}, 422),
            (500, {"name": "test3"}, 404),
            (1, None, 422),
            (1, {"cleaning_type": "invalid cleaning type"}, 422),
            (1, {"cleaning_type": None}, 400),
        ),
    )
    async def test_update_cleaning_raises_errors_with_invalid_input(
        self, app: FastAPI, client: AsyncClient, id: int, payload: Optional[dict], status_code: int
    ) -> None:
        res = await client.put(app.url_path_for("cleanings:update-cleaning", id=id), json=payload)
        assert res.status_code == status_code
