import os

import grpc
from aiohttp import web

from src.routes import routes
from src.middlewares import auth
from gen.profiler_pb2_grpc import ProfilerStub


def create_app() -> web.Application:
    app = web.Application(middlewares=[auth])
    app.add_routes(routes)
    app['profiler'] = ProfilerStub(grpc.aio.insecure_channel(os.environ['PROFILER_URL']))
    return app
