from typing import List

from app.api.dependencies.database import get_repository
from app.db.repositories.cleanings import CleaningRepository
from app.models.cleaning import CleaningCreate, CleaningPublic, CleaningUpdate

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

router = APIRouter()


@router.get("/", response_model=List[CleaningPublic], name="cleanings:list-cleanings")
async def get_all_cleanings(
    cleanings_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
) -> List[CleaningPublic]:
    cleanings = await cleanings_repo.list_cleanings()
    return cleanings


@router.get(
    "/{id}/",
    response_model=CleaningPublic,
    name="cleanings:retrieve-cleaning-by-id",
)
async def retrieve_cleaning_by_id(
    id: int,
    cleanings_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
) -> CleaningPublic:
    cleaning = await cleanings_repo.retrieve_cleaning_by_id(id=id)
    if not cleaning:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No cleaning found with that id.")
    return cleaning


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


@router.put(
    "/{id}/",
    response_model=CleaningPublic,
    name="cleanings:update-cleaning",
)
async def update_cleaning(
    id: int = Path(Ellipsis, ge=1, title="The ID of the cleaning to update."),
    cleaning: CleaningUpdate = Body(Ellipsis),
    cleanings_repo: CleaningRepository = Depends(get_repository(CleaningRepository)),
) -> CleaningPublic:
    updated_cleaning = await cleanings_repo.update_cleaning(id=id, obj=cleaning)

    if not updated_cleaning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No cleaning found with that id.",
        )

    return updated_cleaning
