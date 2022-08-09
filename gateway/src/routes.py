from aiohttp import web
from src import handlers


routes = [
    web.post(path='/api/v2/registration', handler=handlers.registration),
    web.post(path='/api/v2/login', handler=handlers.login),
    web.get(path='/api/v2/logout', handler=handlers.logout),
]
