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
    # TODO: Solve problem "RuntimeError: This event loop is already running" without nest_asyncio library
    nest_asyncio.apply(loop)
    app['pool'] = loop.run_until_complete(asyncpg.create_pool(
        os.environ['DB_URI']
    ))
    app.add_routes(routes)
    app.on_startup.append(create_db)
    return app


def main():
    app = create_app()
    web.run_app(host='0.0.0.0', port=8000, app=app)


if __name__ == '__main__':
    main()
