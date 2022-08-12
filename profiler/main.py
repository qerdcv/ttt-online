import asyncio
import logging
import os

import grpc

from gen import profiler_pb2_grpc
from src.handlers import RouteServicer

log = logging.getLogger(__name__)


async def main():
    server = grpc.aio.server()
    profiler_pb2_grpc.add_ProfilerServicer_to_server(
        RouteServicer(), server)
    port = int(os.environ['PROFILER_PORT'])
    server.add_insecure_port(f'localhost:{port}')
    log.info(f'starting grpc server on port {port}...')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
