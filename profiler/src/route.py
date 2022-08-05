import json

import grpc
from google.protobuf.json_format import MessageToDict
from schematics.exceptions import DataError
from asyncpg.exceptions import UniqueViolationError

from gen import route_pb2_grpc, route_pb2
from src import encrypt, db
from src.models.user import User


class RouteServicer(route_pb2_grpc.ProfilerServicer):
    user_crud: db.UserCRUD = db.UserCRUD()

    async def LoginUser(self, request: route_pb2.LoginUserRequest, context) -> route_pb2.Response:
        user = User(MessageToDict(request))
        try:
            user.validate()
        except DataError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(json.dumps(e.to_primitive()))
            return route_pb2.Response()
        stored_user = await self.user_crud.get(user)
        if stored_user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('user don\'t exists')
            return route_pb2.Response()
        if not encrypt.is_same_messages(stored_user.password, user.password):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('wrong password')
            return route_pb2.Response()
        context.set_code(grpc.StatusCode.OK)
        return route_pb2.Response(
            uid=str(stored_user.uid),
            username=stored_user.username
        )

    async def CreateUser(self, request, context) -> route_pb2.Response:
        user = User(MessageToDict(request))
        try:
            user.validate()
            await self.user_crud.create(user)
        except DataError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(json.dumps(e.to_primitive()))
            return route_pb2.Response()
        except UniqueViolationError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('user with that name already exists')
            return route_pb2.Response()
        context.set_code(grpc.StatusCode.OK)
        return route_pb2.Response()
