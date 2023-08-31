from concurrent import futures

import grpc

from proto.hello_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from proto.hello_pb2 import HelloRequest, HelloReply


class Greeter(GreeterServicer):
    def SayHello(self, request, context):
        for key, value in context.invocation_metadata():
            print(f"Received metadata: {key}={value}")
        context.set_trailing_metadata((
            ("token", "456"),
            ("retry", "false"),
        ))
        return HelloReply(message=f"Hello {request.name}")


if __name__ == '__main__':
    # 1. 实例化 server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 2. 注册 Greeter
    add_GreeterServicer_to_server(Greeter(), server)
    # 3. 绑定端口
    server.add_insecure_port('[::]:8080')
    # 4. 启动服务
    server.start()
    server.wait_for_termination()

