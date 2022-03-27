from dataclasses import dataclass

from aiohttp import web
from aiohttp.web import middleware
from jwt.exceptions import DecodeError

from src.encrypt import decode_jwt


@dataclass
class User:
    id: int
    username: str


@middleware
async def authorized(request: web.Request, handler) -> web.Response:
    token = request.cookies.get('token')
    request.user = None
    if token is not None:
        try:
            token = decode_jwt(token)
        except DecodeError:
            response = await handler(request)
            return response
        request.user = User(*token.values())
    response = await handler(request)
    return response


def auth_required(handler):
    async def wrapped(request: web.Request) -> web.Response:
        if request.user is None:
            return web.json_response({'message': 'unauthorized'}, status=401)
        return await handler(request)
    return wrapped
