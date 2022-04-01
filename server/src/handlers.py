from dataclasses import asdict

from aiohttp import web
from schematics.exceptions import DataError
from asyncpg.exceptions import UniqueViolationError

from src import db
from src.models.user import User
from src.models.paginator import Paginator
from src.models.game import State
from src.encrypt import encrypt_jwt, is_same_messages
from src.decorators import auth_required


async def ping(request: web.Request) -> web.Response:
    return web.json_response({'message': 'pong'})


async def registration(request: web.Request) -> web.Response:
    data = await request.json()
    user = User(data)
    try:
        user.validate()
        await db.create_user(request.app['pool'], user)
    except DataError as e:
        return web.json_response(e.to_primitive(), status=400)
    except UniqueViolationError:
        return web.json_response({'message': 'user with that name already exists'}, status=409)
    return web.json_response({'message': 'OK'}, status=201)


async def login(request: web.Request) -> web.Response:
    data = await request.json()
    remember = data.pop('remember', False)
    user = User(data)
    try:
        user.validate()
    except DataError as e:
        return web.json_response(e.to_primitive(), status=400)
    stored_user = await db.get_user(request.app['pool'], user)
    if stored_user is None:
        return web.json_response({'message': 'user don\'t exists'}, status=404)
    if not is_same_messages(stored_user.password, user.password):
        return web.json_response({'message': 'wrong password'}, status=400)
    response = web.json_response({'message': 'OK'}, status=200)
    response.set_cookie(
        name='token',
        value=encrypt_jwt(id=stored_user.id, username=stored_user.username),
        httponly=True,
        max_age=None if remember else 3600 * 24 * 7
    )
    return response


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
    game = await db.get_game(request.app['pool'], int(request.match_info['gID']))
    if game is None:
        return web.json_response({'message': 'game not found'}, status=404)
    if game.current_state != State.PENDING.value:
        return web.json_response({'message': 'invalid state'}, status=400)
    game.set_opponent(request.user)
    await db.update_game(request.app['pool'], game)
    return web.json_response(asdict(game), status=200)


async def get_game(request: web.Request) -> web.Response:
    game = await db.get_game(request.app['pool'], int(request.match_info['gID']))
    if game is None:
        return web.json_response({'message': 'game not found'}, status=404)
    return web.json_response(asdict(game), status=200)


async def get_games(request: web.Request) -> web.Response:
    count_games = await db.get_total_games(request.app['pool'])
    paginator = Paginator(
        count_games,
        request.query.get('page', '1'),
        request.query.get('limit', '10')
    )
    games = await db.get_game_list(request.app['pool'], paginator.page, paginator.limit)
    return web.json_response(
        {
            'games': [game.to_json() for game in games],
            'paginator': paginator.to_json()
        },
        status=200
    )
