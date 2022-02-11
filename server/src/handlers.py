import math

from aiohttp import web
from schematics.exceptions import DataError

from src import db
from src.models import room as room_model
from src.utils import parse_json


async def ping(request: web.Request) -> web.Response:
    return web.json_response({'msg': 'pong'})


async def create_room(request: web.Request) -> web.Response:
    data = await request.json()
    room = room_model.Room(data)
    try:
        room.validate()
    except DataError as e:
        return web.json_response(e.to_primitive(), status=400)
    pool = request.app['pool']
    room_exist = await db.is_room_exist(pool, data)
    if room_exist:
        return web.json_response({'msg': 'room with that name already exists'}, status=409)
    room_id = await db.create_room(pool, data)
    return web.json_response({'id': room_id}, status=201, dumps=parse_json)


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
    }, status=200, dumps=parse_json)
