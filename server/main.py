import os

import asyncpg
from aiohttp import web

from src.routes import routes
from src.db import create_db


async def init_pool(app):
    app['pool'] = await asyncpg.create_pool(
        os.environ['DB_URI'],
        host=os.environ['DB_HOST']
    )


def create_app() -> web.Application:
    app = web.Application()
    app.add_routes(routes)
    app.on_startup.append(init_pool)
    app.on_startup.append(create_db)
    return app


def main():
    app = create_app()
    web.run_app(host='0.0.0.0', port=8000, app=app)


if __name__ == '__main__':
    main()
