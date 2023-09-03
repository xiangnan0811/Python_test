import asyncio
from concurrent import futures
from datetime import datetime

import grpc

from hello_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from hello_pb2 import HelloRequest, HelloReply


class LogInterceptor(grpc.aio.ServerInterceptor):
    async def intercept_service(self, continuation, handler_call_details: grpc.HandlerCallDetails):
        print(f"Received request: {handler_call_details}")
        return await continuation(handler_call_details)


class Greeter(GreeterServicer):
    def SayHello(self, request: HelloRequest, context):
        # metadata
        for key, value in context.invocation_metadata():
            print(f"Received metadata: {key}={value}")
        context.set_trailing_metadata((
            ("token", "456"),
            ("retry", "false"),
        ))
        print(f"receive request: {request.name}, gender: {request.gender}, addtime: {datetime.fromtimestamp(request.addTime.seconds)}")
        reply = HelloReply(message=f"Hello, {request.name}")
        # context.set_code(grpc.StatusCode.NOT_FOUND)
        return reply


async def main():
    # 1. 实例化 server
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = grpc.aio.server(
        migration_thread_pool=futures.ThreadPoolExecutor(max_workers=10),
        interceptors=[LogInterceptor()],
    )
    # 2. 注册 Greeter
    add_GreeterServicer_to_server(Greeter(), server)
    # 3. 绑定端口
    server.add_insecure_port('[::]:50051')
    # 4. 启动服务
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    asyncio.run(main())
