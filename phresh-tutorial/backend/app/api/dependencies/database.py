from typing import Callable, Type

from app.db.repositories.base import BaseRepository
from databases import Database
from fastapi import Depends
from fastapi.requests import Request


def get_database(request: Request) -> Database:
    return request.app.state._db


def get_repository(RepoType: Type[BaseRepository]) -> Callable:
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return RepoType(db)

    return get_repo
