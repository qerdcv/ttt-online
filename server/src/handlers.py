from aiohttp import web


async def ping(request: web.Request) -> web.Response:
    return web.json_response({'msg': 'pong'})
