from datetime import datetime, timedelta

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_AUDIENCE
from app.models.base import CoreModel
from pydantic import EmailStr


class JWTMeta(CoreModel):
    iss: str = "phresh.io"
    aud: str = JWT_AUDIENCE
    iat: float = datetime.timestamp(datetime.utcnow())
    exp: float = datetime.timestamp(datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


class JWTCredentials(CoreModel):
    sub: EmailStr
    username: str


class JWTPayload(JWTMeta, JWTCredentials):
    pass


class AccessToken(CoreModel):
    access_token: str
    token_type: str
