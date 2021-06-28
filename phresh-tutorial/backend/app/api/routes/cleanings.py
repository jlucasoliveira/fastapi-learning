from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.cleanings import CleaningRepository
from app.models.cleaning import CleaningCreate, CleaningPublic
from fastapi import APIRouter, Body, Depends, status

router = APIRouter()


@router.get("/")
async def get_all_cleanings() -> List[dict]:
    cleanings = [
        {"id": 1, "name": "My House", "cleaning_type": "full_clean", "price_per_hour": 29.99},
        {"id": 2, "name": "Someone else's house", "cleaning_type": "spot_clean", "price_per_hour": 19.99},
    ]
    return cleanings


@router.post(
    "/",
    response_model=CleaningPublic,
    name="cleanings:create-cleaning",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_cleaning(
    new_cleaning: CleaningCreate = Body(Ellipsis),
    cleanings_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
) -> CleaningPublic:
    created_cleaning = await cleanings_repo.create_cleaning(obj=new_cleaning)
    return created_cleaning
