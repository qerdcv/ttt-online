import math

from aiohttp import web
from schematics.exceptions import DataError

from src import db
from src.models import room
from src.utils import parse_json


async def ping(request: web.Request) -> web.Response:
    return web.json_response({'msg': 'pong'})


async def create_room(request: web.Request) -> web.Response:
    data = await request.json()
    some_room = room.Room(data)
    try:
        some_room.validate()
    except DataError as e:
        return web.json_response(e.to_primitive(), status=400)
    pool = request.app['pool']
    room_info = await db.get_room(pool, data)
    if room_info is not None:
        return web.json_response({'msg': 'room with that name already exists'}, status=409)
    room_id = await db.create_room(pool, data)
    return web.json_response({'room_id': room_id}, status=201, dumps=parse_json)


async def get_list_rooms(request: web.Request) -> web.Response:
    pool = request.app['pool']
    page = int(request.query.get('page', '1'))
    limit = int(request.query.get('limit', '10'))
    rooms, total_count = await db.get_room_list(pool, page, limit)
    return web.json_response({
        "rooms": rooms,
        "paginator": {
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total_count / limit),
        }
    }, status=200, dumps=parse_json)
