from aiohttp import web
from src import handlers

routes = [
    web.get(path='/ping', handler=handlers.ping),
    web.post(path='/api/room', handler=handlers.create_room),
    web.get(path='/api/room', handler=handlers.get_list_rooms),
    web.get(path='/api/room/{_id}', handler=handlers.get_room)
]
