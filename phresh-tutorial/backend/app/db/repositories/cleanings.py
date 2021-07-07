from typing import List, Optional

from app.db.repositories.base import BaseRepository
from app.models.cleaning import CleaningCreate, CleaningInDB, CleaningUpdate
from app.utils import handle_exception

from fastapi import HTTPException, status

CREATE_CLEANING_QUERY = """
    INSERT INTO cleanings (name, description, price, cleaning_type)
    VALUES (:name, :description, :price, :cleaning_type)
    RETURNING id, name, description, price, cleaning_type;
"""


LIST_ALL_CLEANINGS_QUERY = """
    SELECT id, name, description, price, cleaning_type
    FROM cleanings
"""


RETRIEVE_CLEANING_BY_ID_QUERY = """
    SELECT id, name, description, price, cleaning_type
    FROM cleanings
    WHERE id = :id;
"""


UPDATE_CLEANING_BY_ID_QUERY = """
    UPDATE cleanings
    SET name = :name,
        description = :description,
        price = :price,
        cleaning_type = :cleaning_type
    WHERE id = :id
    RETURNING id, name, description, price, cleaning_type;
"""


class CleaningRepository(BaseRepository):
    async def create_cleaning(self, *, obj: CleaningCreate) -> CleaningInDB:
        query_values = obj.dict()
        cleaning = await self.db.fetch_one(
            query=CREATE_CLEANING_QUERY,
            values=query_values,
        )

        return CleaningInDB(**cleaning)

    async def list_cleanings(self) -> List[CleaningInDB]:
        cleanings = await self.db.fetch_all(
            query=LIST_ALL_CLEANINGS_QUERY,
        )
        return [CleaningInDB(**cleaning) for cleaning in cleanings]

    async def retrieve_cleaning_by_id(self, *, id: int) -> Optional[CleaningInDB]:
        cleaning = await self.db.fetch_one(
            query=RETRIEVE_CLEANING_BY_ID_QUERY,
            values={"id": id},
        )

        if not cleaning:
            return None

        return CleaningInDB(**cleaning)

    async def update_cleaning(self, *, id: int, obj: CleaningUpdate) -> Optional[CleaningInDB]:
        cleaning_to_update = await self.retrieve_cleaning_by_id(id=id)

        if not cleaning_to_update:
            return None

        cleaning_updated_params = cleaning_to_update.copy(update=obj.dict(exclude_unset=True))

        try:
            updated_cleaning = await self.db.fetch_one(
                query=UPDATE_CLEANING_BY_ID_QUERY,
                values=cleaning_updated_params.dict(),
            )
            return CleaningInDB(**updated_cleaning)
        except Exception as e:
            handle_exception("UPDATE CLEANING", e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid update params.",
            )
