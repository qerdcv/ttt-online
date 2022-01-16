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
    if await db.room_is_occupied(data):
        return web.json_response({'msg': 'room with that name already exists'}, status=409)
    await db.create_room(data)
    return web.json_response({'msg': 'OK'}, status=201)


async def get_list_rooms(request: web.Request) -> web.Response:
    page = int(request.query.get('page', '1'))
    limit = int(request.query.get('limit', '10'))
    rooms, total_count = await db.get_rooms(page, limit)
    return web.json_response({
        "rooms": rooms,
        "paginator": {
            "page": page,
            "limit": limit,
            "total_pages": math.ceil(total_count / limit),
        }
    }, status=200, dumps=parse_json)


async def get_room(request: web.Request) -> web.Response:
    _id = request.match_info['_id']
    game = await db.get_room(_id)
    if game is None:
        return web.json_response({'msg': 'Room search error'}, status=404)
    return web.json_response({'game': game}, status=200)
