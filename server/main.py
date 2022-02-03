import os
import asyncio

import asyncpg
import nest_asyncio
from aiohttp import web

from src.routes import routes
from src.db import create_db


def create_app() -> web.Application:
    app = web.Application()
    loop = asyncio.get_event_loop()
    nest_asyncio.apply(loop)
    app['pool'] = loop.run_until_complete(asyncpg.create_pool(
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'],
        database=os.environ['DB_DATABASE'],
        host=os.environ['DB_HOST']
    ))
    app.add_routes(routes)
    app.on_startup.append(create_db)
    return app


def main():
    app = create_app()
    web.run_app(host='0.0.0.0', port=8000, app=app)


if __name__ == '__main__':
    main()
