from typing import Optional

from app.models.token import AccessToken
from pydantic import EmailStr, constr

from .base import CoreModel, DateTimeModelMixin, IDModelMixin


class UserBase(CoreModel):
    email: Optional[EmailStr]
    username: Optional[str]
    email_verified: bool = False
    is_active: bool = True
    is_superuser: bool = False


class UserCreate(CoreModel):
    email: EmailStr
    password: constr(min_length=10, max_length=280)
    username: constr(min_length=5, regex=r"^[a-zA=Z_-]+$")  # noqa


class UserUpdate(CoreModel):
    email: Optional[EmailStr]
    username: Optional[constr(min_length=5, regex=r"^[a-zA=Z_-]+$")]  # noqa


class UserPasswordUpdate(CoreModel):
    password: constr(min_length=10, max_length=280)
    salt: str


class UserInDB(IDModelMixin, DateTimeModelMixin, UserBase):
    password: constr(min_length=10, max_length=280)
    salt: str


class UserPublic(IDModelMixin, DateTimeModelMixin, UserBase):
    access_token: Optional[AccessToken]
