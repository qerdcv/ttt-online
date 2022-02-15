import logging

import schematics
from aiohttp import web
from asyncpg.pool import Pool
from typing import Optional

from config import BASE_DIR


log = logging.getLogger(__name__)


def get_query(query_name: str) -> Optional[str]:
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


async def create_room(pool: Pool, room: schematics.Model) -> int:
    async with pool.acquire() as conn:
        room_id = await conn.fetchval(
            get_query('create_room'),
            room.room_name, room.is_private, room.password
        )
    return room_id


async def get_room_list(pool: Pool, page: int, limit: int) -> list:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            get_query('get_room_list'),
            (page - 1) * limit, limit
        )
    result = [dict(row) for row in rows]
    return result


async def get_total_rooms(pool: Pool) -> int:
    async with pool.acquire() as con:
        total_rooms = await con.fetchval(get_query('get_total_rooms'))
    return total_rooms
