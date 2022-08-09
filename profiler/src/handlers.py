import json

import grpc
from google.protobuf.json_format import MessageToDict
from schematics.exceptions import DataError
from asyncpg.exceptions import UniqueViolationError

from gen import profiler_pb2_grpc, profiler_pb2
from src.service import Profiler
from src.models.user import User
from src.errors import user


class RouteServicer(profiler_pb2_grpc.ProfilerServicer):
    profiler = Profiler()

    async def LoginUser(self, request: profiler_pb2.LoginUserRequest, context) -> profiler_pb2.LoginUserResponse:
        try:
            stored_user = await self.profiler.login(
                User(MessageToDict(request))
            )
        except DataError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(json.dumps(e.to_primitive()))
            return profiler_pb2.LoginUserResponse()
        except user.NotFound as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(json.dumps(e.to_dict()))
            return profiler_pb2.LoginUserResponse()
        except user.WrongPassword as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(json.dumps(e.to_dict()))
            return profiler_pb2.LoginUserResponse()
        context.set_code(grpc.StatusCode.OK)
        return profiler_pb2.LoginUserResponse(
            uid=str(stored_user.uid),
            username=stored_user.username
        )

    async def CreateUser(self, request, context) -> profiler_pb2.CreateUserResponse:
        try:
            await self.profiler.create(
                User(MessageToDict(request))
            )
        except DataError as e:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(json.dumps(e.to_primitive()))
            return profiler_pb2.CreateUserResponse()
        except UniqueViolationError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(json.dumps({'message': 'user with that name already exists'}))
            return profiler_pb2.CreateUserResponse()
        context.set_code(grpc.StatusCode.OK)
        return profiler_pb2.CreateUserResponse()
