from aiohttp import web
from src import handlers


routes = [
    web.post(path='/api/v2/auth/reg', handler=handlers.registration),
    web.post(path='/api/v2/auth/login', handler=handlers.login),
    web.get(path='/api/v2/auth/logout', handler=handlers.logout),
]
