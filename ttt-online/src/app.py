import asyncpg
from aiohttp import web

from src.routes import routes
from src.middlewares import auth
from src.config import Config


async def init_pool(app):
    app['pool'] = await asyncpg.create_pool(
        Config.db.uri
    )


def create_app() -> web.Application:
    app = web.Application(middlewares=[auth])
    app.add_routes(routes)
    app.on_startup.extend([init_pool])
    return app
