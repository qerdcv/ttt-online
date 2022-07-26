from aiohttp import web
from src import handlers
from src import sse


routes = [
    web.get(path='/ping', handler=handlers.ping),
    web.post(path='/api/registration', handler=handlers.registration),
    web.post(path='/api/login', handler=handlers.login),
    web.get(path='/api/logout', handler=handlers.logout),
    web.get(path='/api/games', handler=handlers.get_games),
    web.get(path='/api/games/{_id:\\d+}', handler=handlers.get_game),
    web.post(path='/api/games', handler=handlers.create_game),
    web.patch(path='/api/games/{_id:\\d+}/login', handler=handlers.login_game),
    web.get(path='/api/games/{_id:\\d+}/sse', handler=sse.stream),
    web.patch(path='/api/games/{_id:\\d+}', handler=handlers.make_step)
]
