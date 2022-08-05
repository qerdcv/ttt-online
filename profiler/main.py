import asyncio
import logging

import grpc

from gen import route_pb2_grpc
from src.route import RouteServicer


async def serve():
    server = grpc.aio.server()
    route_pb2_grpc.add_ProfilerServicer_to_server(
        RouteServicer(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    asyncio.run(serve())
