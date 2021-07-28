from app.api.dependencies.database import get_repository
from app.core.config import JWT_TOKEN_PREFIX
from app.db.repositories.users import UsersRepository
from app.models.token import AccessToken
from app.models.user import UserCreate, UserPublic
from app.services import auth_service

from fastapi import APIRouter, Body, Depends, status

router = APIRouter()


@router.post(
    "/",
    response_model=UserPublic,
    name="users:register-new-user",
    status_code=status.HTTP_201_CREATED,
)
async def register_new_user(
    new_user: UserCreate = Body(Ellipsis),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    created_user = await user_repo.register_new_user(new_user=new_user)

    access_token = AccessToken(
        access_token=auth_service.create_access_token_for_user(user=created_user),
        token_type=JWT_TOKEN_PREFIX,
    )
    return UserPublic(**created_user.dict(), access_token=access_token)
