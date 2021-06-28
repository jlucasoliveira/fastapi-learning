from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config()


PROJECT_NAME: str = "phresh-tutorial"
VERSION: str = "0.0.1"
API_PREFIX: str = "api/"

SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)

DATABAS_URL = config("DATABASE_URL", cast=DatabaseURL)
