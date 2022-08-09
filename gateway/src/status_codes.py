from grpc import StatusCode


grpc_to_http = {
    StatusCode.OK: 200,
    StatusCode.INVALID_ARGUMENT: 400,
    StatusCode.NOT_FOUND: 404,
    StatusCode.ALREADY_EXISTS: 409
}
