from typing import Union

from app.models.cleaning import CleaningCreate, CleaningInDB

from .base import BaseRepository

CREATE_CLEANING_QUERY = """
    INSERT INTO cleanings (name, description, price, cleaning_type)
    VALUES (:name, :description, :price, :cleaning_type)
    RETURNING id, name, description, price, cleaning_type;
"""


RETRIEVE_CLEANING_BY_ID_QUERY = """
    SELECT id, name, description, price, cleaning_type
    FROM cleanings
    WHERE id = :id;
"""


class CleaningRepository(BaseRepository):
    async def create_cleaning(self, *, obj: CleaningCreate) -> CleaningInDB:
        query_values = obj.dict()
        cleaning = await self.db.fetch_one(
            query=CREATE_CLEANING_QUERY,
            values=query_values,
        )

        return CleaningInDB(**cleaning)

    async def retrieve_cleaning(self, *, id: int) -> Union[CleaningInDB, None]:
        cleaning = await self.db.fetch_one(
            query=RETRIEVE_CLEANING_BY_ID_QUERY,
            values={"id": id},
        )

        if not cleaning:
            return None

        return CleaningInDB(**cleaning)
