import json
from dataclasses import asdict

from aiohttp import web
from aiohttp_sse import sse_response

from src import db
from src.models.lobby import Lobby
from src.config import Config


async def stream(request: web.Request) -> web.Response:
    game_id = int(request.match_info['_id'])
    if not await db.get_game(request.app['pool'], game_id):
        return web.json_response({'message': 'game not found'}, status=404)

    lobby = Lobby()
    queue = lobby.join(game_id)
    headers = {}

    if Config.is_dev:
        headers.update({
            'Access-Control-Allow-Origin': '*'
        })

    async with sse_response(request, headers=headers) as response:
        try:
            while not response.task.done():
                game = await queue.get()
                await response.send(json.dumps(asdict(game)))
                queue.task_done()
        finally:
            lobby.leave(game_id, queue)
    return response
