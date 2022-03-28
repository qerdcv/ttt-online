from aiohttp import web
from aiohttp.web import middleware
from jwt.exceptions import DecodeError

from src.encrypt import decode_jwt
from src.models.user import User


@middleware
async def auth(request: web.Request, handler) -> web.Response:
    request.user = None
    try:
        request.user = User(decode_jwt(request.cookies.get('token')))
    except DecodeError:
        pass
    return await handler(request)
