import asyncpg
from aiohttp import web

from src.config import Config
from src.routes import routes
from src.middlewares import auth


async def init_pool(app):
    db_config = Config.db
    app['pool'] = await asyncpg.create_pool(
        user=db_config.username,
        password=db_config.password,
        database=db_config.database,
        host=db_config.host,
        port=db_config.port,
    )


def create_app() -> web.Application:
    app = web.Application(middlewares=[auth])
    app.add_routes(routes)
    app.on_startup.extend([init_pool])
    return app
