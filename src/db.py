import json
import logging
import typing as t

from aiohttp import web
from asyncpg.pool import Pool
from config import BASE_DIR
from src.encrypt import encrypt
from src.models.game import Game
from src.models.user import User


log = logging.getLogger(__name__)


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


async def create_user(pool: Pool, user: User):
    async with pool.acquire() as conn:
        await conn.execute(
            get_query('create_user'),
            user.username, encrypt(user.password)
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


async def get_user(pool: Pool, user: User) -> t.Optional[User]:
    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            get_query('get_user'),
            user.username
        )
    if user is not None:
        return User(dict(user))


async def get_game(pool: Pool, _id: int) -> t.Optional[Game]:
    async with pool.acquire() as conn:
        game = await conn.fetchrow(
            get_query('get_game'),
            _id
        )
    if game is not None:
        game = Game(*game)
        game.field = json.loads(game.field)
    return game


async def get_game_list(pool: Pool, page: int, limit: int) -> t.List[Game]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            get_query('get_game_list'),
            (page - 1) * limit, limit
        )
    games = [Game(*row) for row in rows]
    for game in games:
        game.field = json.loads(game.field)
    return games


async def get_total_games(pool: Pool) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval(get_query('get_total_games'))


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


async def cleanup(pool: Pool):
    async with pool.acquire() as conn:
        await conn.execute(get_query('cleanup'))
