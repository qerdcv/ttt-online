import math
from dataclasses import asdict

from aiohttp import web
from schematics.exceptions import DataError
from asyncpg.exceptions import UniqueViolationError

from src import db
from src.models.user import User
from src.models.paginator import Paginator
from src.encrypt import encrypt_jwt
from src.middlewares import auth_required


async def ping(request: web.Request) -> web.Response:
    return web.json_response({'message': 'pong'})


async def registration(request: web.Request) -> web.Response:
    data = await request.json()
    remember = data.pop('remember', False)
    user = User(data)
    try:
        user.validate()
    except DataError as e:
        return web.json_response(e.to_primitive(), status=400)
    pool = request.app['pool']
    try:
        user = await db.create_user(pool, user)
    except UniqueViolationError:
        return web.json_response({'message': 'user with that name already exists'}, status=409)
    response = web.json_response({'message': 'OK'}, status=201)
    encoded_jwt = encrypt_jwt(id=user.id, user_name=user.username)
    if remember:
        response.set_cookie(
            name='token',
            value=encoded_jwt,
            httponly=True
        )
    else:
        response.set_cookie(
            name='token',
            value=encoded_jwt,
            httponly=True,
            max_age=3600 * 24 * 7
        )
    return response


async def login(request: web.Request) -> web.Response:
    data = await request.json()
    remember = data.pop('remember', False)
    user = User(data)
    try:
        user.validate()
    except DataError as e:
        return web.json_response(e.to_primitive(), status=400)
    pool = request.app['pool']
    password = user.password
    user = await db.get_user(pool, user.username)
    if user is None:
        return web.json_response({'message': "user don't exists"}, status=404)
    if user.is_password_same(password):
        response = web.json_response({'message': 'OK'}, status=200)
        encoded_jwt = encrypt_jwt(id=user.id, user_name=user.username)
        if remember:
            response.set_cookie(
                name='token',
                value=encoded_jwt,
                httponly=True
            )
        else:
            response.set_cookie(
                name='token',
                value=encoded_jwt,
                httponly=True,
                max_age=3600 * 24 * 7
            )
        return response
    return web.json_response({'message': 'wrong password'}, status=400)


async def logout(request: web.Request) -> web.Response:
    response = web.json_response({'message': 'OK'})
    response.del_cookie(name='token')
    return response


@auth_required
async def create_game(request: web.Request) -> web.Response:
    game = await db.create_game(request.app['pool'], request.user)
    return web.json_response(asdict(game), status=201)


@auth_required
async def login_game(request: web.Request) -> web.Response:
    pass


async def get_game(request: web.Request) -> web.Response:
    pass


async def get_games(request: web.Request) -> web.Response:
    pass


async def get_list_rooms(request: web.Request) -> web.Response:
    pool = request.app['pool']
    paginator = Paginator()
    try:
        page = int(request.query.get('page'))
        limit = int(request.query.get('limit'))
        paginator.page, paginator.limit = page, limit
        paginator.validate()
    except (TypeError, ValueError):
        page, limit = paginator.page, paginator.limit
    except DataError:
        page, limit = paginator.page, 100
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
