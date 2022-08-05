import logging
import typing as t

import asyncpg

from src.config import Config
from src.encrypt import encrypt
from src.models.user import User

log = logging.getLogger(__name__)


class UserCRUD:
    obj = None

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = super().__new__(cls, *args, **kwargs)
        return cls.obj

    @staticmethod
    def get_query(query_name: str) -> t.Optional[str]:
        try:
            with open(Config.base_dir / f'src/db/queries/{query_name}.sql', 'r') as file:
                return file.read()
        except FileNotFoundError:
            log.error(f'Query {query_name} not found')

    @classmethod
    async def get(cls, user: User) -> User:
        conn = await asyncpg.connect(Config.db_uri)
        user = await conn.fetchrow(
            cls.get_query('get_user'),
            user.username
        )
        if user:
            return User(dict(user))

    @classmethod
    async def create(cls, user: User) -> User:
        conn = await asyncpg.connect(Config.db_uri)
        user.uid = await conn.fetchval(
            cls.get_query('create_user'),
            user.username, encrypt(user.password)
        )
        return user
