from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config()

ONE_WEEK_IN_SECONDS = 7 * 24 * 60


PROJECT_NAME: str = "phresh-tutorial"
VERSION: str = "0.0.1"
API_PREFIX: str = "/api"

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES",
    cast=int,
    default=ONE_WEEK_IN_SECONDS,
)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="phresh:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")

DATABASE_URL = config("DATABASE_URL", cast=DatabaseURL)

TESTING: str = config("TESTING", cast=bool, default=False)
