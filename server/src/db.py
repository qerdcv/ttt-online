import logging

import asyncpg
from aiohttp import web
from asyncpg.pool import Pool

from config import BASE_DIR


log = logging.getLogger(__name__)


def get_query(query_name: str) -> str:
    try:
        with open(BASE_DIR / f'queries/{query_name}.sql', 'r') as file:
            return file.read()
    except FileNotFoundError:
        log.error(f'Query {query_name} not found')
        return ''


async def create_db(app: web.Application):
    log.info('create_db')
    pool: Pool = app['pool']
    async with pool.acquire() as con:
        await con.execute(get_query('init'))


async def create_room(pool: Pool, data: dict) -> int:
    async with pool.acquire() as con:
        room_id = await con.fetchval(
            get_query('create_room'),
            data['room_name'], data['is_private']
        )
    if 'password' in data.keys():
        await update_password(pool, room_id, data['password'])
    return room_id


async def get_room(pool: Pool, data: dict):
    async with pool.acquire() as con:
        room = await con.fetchrow(
            get_query('get_room'),
            data["room_name"]
        )
    return room


async def get_total_page(pool: Pool):
    async with pool.acquire() as con:
        total_page = await con.fetchval(get_query('get_total_page'))
    return total_page


async def get_room_list(pool: Pool, page: int, limit: int) -> (list, int):
    async with pool.acquire() as con:
        rows = await con.fetch(
            get_query('get_room_list'),
            (page - 1) * limit, limit
        )
    result = [dict(row) for row in rows]
    total_page = await get_total_page(pool)
    return result, total_page


async def update_password(pool: Pool, room_id: int, pas: str):
    async with pool.acquire() as con:
        await con.execute(
            get_query('update_password'),
            pas, room_id
        )
