from aiohttp import web
from aiohttp.web import middleware
from jwt.exceptions import DecodeError

from src.encrypt import decode_jwt
from src.config import Config


@middleware
async def auth(request: web.Request, handler) -> web.Response:
    request.user = None
    try:
        request.user = decode_jwt(request.cookies.get(Config.cookie_name))
    except DecodeError:
        pass
    return await handler(request)
