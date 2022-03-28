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
    try:
        await db.create_user(request.app['pool'], user)
    except UniqueViolationError:
        return web.json_response({'message': 'user with that name already exists'}, status=409)
    response = web.json_response({'message': 'OK'}, status=201)
    if remember:
        response.set_cookie(
            name='token',
            value=encrypt_jwt(id=user.id, user_name=user.username),
            httponly=True
        )
    else:
        response.set_cookie(
            name='token',
            value=encrypt_jwt(id=user.id, user_name=user.username),
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
    password = user.password
    user = await db.get_user(request.app['pool'], user.username)
    if user is None:
        return web.json_response({'message': "user don't exists"}, status=404)
    if user.is_password_same(password):
        response = web.json_response({'message': 'OK'}, status=200)
        if remember:
            response.set_cookie(
                name='token',
                value=encrypt_jwt(id=user.id, user_name=user.username),
                httponly=True
            )
        else:
            response.set_cookie(
                name='token',
                value=encrypt_jwt(id=user.id, user_name=user.username),
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
    data = await request.json()
    game = await db.get_game(request.app['pool'], data['id'])
    if game is None:
        return web.json_response({'message': 'game not found'}, status=404)
    game.set_opponent(request.user)
    await db.update_game(request.app['pool'], game)
    return web.json_response(asdict(game), status=200)


async def get_game(request: web.Request) -> web.Response:
    game = await db.get_game(request.app['pool'], int(request.match_info['num']))
    if game is None:
        return web.json_response({'message': 'game not found'}, status=404)
    return web.json_response(asdict(game), status=200)


async def get_games(request: web.Request) -> web.Response:
    paginator = Paginator()
    paginator.create_paginator(
        request.query.get('page'), request.query.get('limit')
    )
    rooms = await db.get_game_list(request.app['pool'], paginator.page, paginator.limit)
    total_rooms = await db.get_total_games(request.app['pool'])
    return web.json_response({
        "rooms": rooms,
        "paginator": {
            "page": paginator.page,
            "limit": paginator.limit,
            "total_pages": math.ceil(total_rooms / paginator.limit),
        }
    }, status=200)
