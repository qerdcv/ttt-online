from aiohttp import web
from src import handlers


routes = [
    web.get(path='/ping', handler=handlers.ping),
    web.post(path='/api/registration', handler=handlers.registration),
    web.post(path='/api/login', handler=handlers.login),
    web.get(path='/api/logout', handler=handlers.logout),
    web.get(path='/api/get_games', handler=handlers.get_games),
    web.get(path=r'/api/get_game/{num:\d+}', handler=handlers.get_game),
    web.post(path='/api/create_game', handler=handlers.create_game),
    web.post(path='/api/login_game', handler=handlers.login_game)
]
