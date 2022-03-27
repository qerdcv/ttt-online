import json
import logging
import typing as t
from dataclasses import dataclass, astuple

from aiohttp import web
from asyncpg.pool import Pool

from config import BASE_DIR
from src.encrypt import encrypt_password, decrypt_password
from src.models.game import Game
from src.models.user import User as ValidUser
from src.middlewares import User


log = logging.getLogger(__name__)


@dataclass
class UserInfo:
    id: str
    username: str
    password: str

    def is_password_same(self, password):
        return decrypt_password(self.password) == password


def get_query(query_name: str) -> t.Optional[str]:
    try:
        with open(BASE_DIR / f'queries/{query_name}.sql', 'r') as file:
            return file.read()
    except FileNotFoundError:
        log.error(f'Query {query_name} not found')


async def create_db(app: web.Application):
    log.info('create_db')
    pool: Pool = app['pool']
    async with pool.acquire() as conn:
        await conn.execute(get_query('init'))


async def create_user(pool: Pool, user: ValidUser):
    user.password = encrypt_password(user.password)
    async with pool.acquire() as conn:
        user.id = await conn.fetchval(
            get_query('create_user'),
            user.username, user.password
        )


async def create_game(pool: Pool, user: User) -> Game:
    async with pool.acquire() as conn:
        game = await conn.fetchrow(
            get_query('create_game'),
            user.id
        )
    game = Game(*game)
    game.field = json.loads(game.field)
    return game


async def get_user(pool: Pool, username: str) -> t.Optional[UserInfo]:
    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            get_query('get_user'),
            username
        )
    if user is not None:
        return UserInfo(*user)
    return None


async def get_game(pool: Pool, id: int) -> t.Optional[Game]:
    async with pool.acquire() as conn:
        game = await conn.fetchrow(
            get_query('get_game'),
            id
        )
    if game is not None:
        game = Game(*game)
        game.field = json.loads(game.field)
    return game


async def update_game(pool: Pool, game: Game):
    async with pool.acquire() as conn:
        await conn.execute(
            get_query('update_game'),
            game.id,
            game.owner_id,
            game.opponent_id,
            game.current_player_id,
            game.step_count,
            game.winner_id,
            json.dumps(game.field),
            game.current_state
        )
