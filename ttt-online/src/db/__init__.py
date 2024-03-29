import json
import logging
import typing as t

from asyncpg.pool import Pool
from src.config import Config
from src.encrypt import encrypt_password
from src.models.game import Game, Games
from src.models.user import User
from src.models.lobby import Lobby


log = logging.getLogger(__name__)


def get_query(query_name: str) -> t.Optional[str]:
    try:
        with open(Config.base_dir / f'src/db/queries/{query_name}.sql', 'r') as file:
            return file.read()
    except FileNotFoundError:
        log.error(f'Query {query_name} not found')


async def create_user(pool: Pool, user: User) -> User:
    async with pool.acquire() as conn:
        user.id = await conn.fetchval(
            get_query('create_user'),
            user.username, encrypt_password(user.password)
        )
    return user


async def create_game(pool: Pool, user: User) -> Game:
    async with pool.acquire() as conn:
        game = await conn.fetchrow(
            get_query('create_game'),
            user.id
        )
    return Game.from_record(game)


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
    if game:
        return Game.from_record(game)


async def get_game_list(pool: Pool, page: int, limit: int) -> Games:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            get_query('get_game_list'),
            (page - 1) * limit, limit
        )
    return Games.from_record(rows)


async def get_total_games(pool: Pool) -> int:
    async with pool.acquire() as conn:
        return await conn.fetchval(get_query('get_total_games'))


async def get_game_history(pool: Pool, game_id: int) -> Games:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            get_query('get_game_history'),
            game_id
        )
    return Games.from_record(rows)


async def update_game(pool: Pool, game: Game):
    async with pool.acquire() as conn:
        await conn.execute(
            get_query('update_game'),
            game.id,
            game.owner.id,
            game.opponent.id,
            game.current_player.id,
            game.step_count,
            game.winner.id,
            json.dumps(game.field),
            game.current_state
        )
    await Lobby().update(game.id, game)


async def cleanup(pool: Pool):
    async with pool.acquire() as conn:
        await conn.execute(get_query('cleanup'))
