import math

from aiohttp import web
from schematics.exceptions import DataError
from asyncpg.exceptions import UniqueViolationError

from src import db
from src.models.room import Room


async def ping(request: web.Request) -> web.Response:
    return web.json_response({'msg': 'pong'})


async def create_room(request: web.Request) -> web.Response:
    data = await request.json()
    room = Room(data)
    try:
        room.validate()
    except DataError as e:
        return web.json_response(e.to_primitive(), status=400)
    pool = request.app['pool']
    try:
        room_id = await db.create_room(pool, room)
    except UniqueViolationError:
        return web.json_response({'msg': 'room with that name already exists'}, status=409)
    return web.json_response({'id': room_id}, status=201)


async def get_list_rooms(request: web.Request) -> web.Response:
    pool = request.app['pool']
    page = int(request.query.get('page', '1'))
    limit = int(request.query.get('limit', '10'))
    rooms = await db.get_room_list(pool, page, limit)
    total_rooms = await db.get_total_rooms(pool)
    return web.json_response({
        "rooms": rooms,
        "paginator": {
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total_rooms / limit),
        }
    }, status=200)
