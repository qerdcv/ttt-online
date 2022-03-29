from aiohttp import web


def auth_required(handler):
    async def wrapped(request: web.Request) -> web.Response:
        if request.user is None:
            return web.json_response({'message': 'unauthorized'}, status=401)
        return await handler(request)
    return wrapped
