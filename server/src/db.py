import logging

import asyncpg
from aiohttp import web
from asyncpg.pool import Pool
from dataclasses import dataclass

from config import BASE_DIR


log = logging.getLogger(__name__)


@dataclass
class Room:
    room_name: str
    is_private: bool
    password: str = ''


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
    async with pool.acquire() as conn:
        await conn.execute(get_query('init'))


async def create_room(pool: Pool, data: dict) -> int:
    room = Room(room_name=data['room_name'], is_private=data['is_private'])
    if 'password' in data.keys():
        room.password = data['password']
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
        total_page = await con.fetchval(get_query('get_total_rooms'))
    return total_page


async def is_room_exist(pool: Pool, data: dict) -> bool:
    async with pool.acquire() as conn:
        room = await conn.fetchrow(
            get_query('get_room'),
            data["room_name"]
        )
    if room is not None:
        return True
    return False
