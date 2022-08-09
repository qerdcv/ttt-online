import json

from aiohttp import web
from grpc.aio import AioRpcError

from gen import profiler_pb2, profiler_pb2_grpc
from src.encrypt import encrypt_jwt
from src.models.user import User
from src.status_codes import grpc_to_http


async def registration(request: web.Request) -> web.Response:
    data = await request.json()
    user = User(**data)
    profiler: profiler_pb2_grpc.ProfilerStub = request.app['profiler']
    try:
        await profiler.CreateUser(
            profiler_pb2.CreateUserRequest(
                username=user.username,
                password=user.password
            )
        )
    except AioRpcError as e:
        return web.json_response(
            json.loads(e.details()),
            status=grpc_to_http[e.code()]
        )
    return web.json_response({'message': 'OK'}, status=201)


async def login(request: web.Request) -> web.Response:
    data = await request.json()
    remember = data.pop('remember', False)
    user = User(**data)
    profiler: profiler_pb2_grpc.ProfilerStub = request.app['profiler']
    try:
        stored_user: profiler_pb2.LoginUserResponse = await profiler.LoginUser(
            profiler_pb2.LoginUserRequest(
                username=user.username,
                password=user.password
            )
        )
    except AioRpcError as e:
        return web.json_response(
            json.loads(e.details()),
            status=grpc_to_http[e.code()]
        )
    response = web.json_response(
        {
            'uid': stored_user.uid,
            'username': stored_user.username
        },
        status=200
    )
    response.set_cookie(
        name='token',
        value=encrypt_jwt(uid=stored_user.uid, username=stored_user.username),
        httponly=True,
        max_age=None if remember else 3600 * 24 * 7
    )
    return response


async def logout(request: web.Request) -> web.Response:
    response = web.json_response({'message': 'OK'})
    response.del_cookie(name='token')
    return response
