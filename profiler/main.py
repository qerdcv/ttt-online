import asyncio
import logging

import grpc

from gen import profiler_pb2_grpc
from src.handlers import RouteServicer
from src.config import Config

log = logging.getLogger(__name__)

log = logging.getLogger(__name__)


async def main():
    server = grpc.aio.server()
    profiler_pb2_grpc.add_ProfilerServicer_to_server(
        RouteServicer(), server)
    server.add_insecure_port(f'0.0.0.0:{Config.grpc_port}')
    log.info(f'starting grpc server on port {Config.grpc_port}...')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
