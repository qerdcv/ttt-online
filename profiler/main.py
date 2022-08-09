import asyncio
import logging

import grpc

from gen import profiler_pb2_grpc
from src.handlers import RouteServicer

log = logging.getLogger(__name__)


async def main():
    server = grpc.aio.server()
    profiler_pb2_grpc.add_ProfilerServicer_to_server(
        RouteServicer(), server)
    server.add_insecure_port('[::]:50051')
    log.info("starting grpc server on port 50051...")
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
