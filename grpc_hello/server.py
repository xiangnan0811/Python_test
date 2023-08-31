from concurrent import futures

import grpc

from hello_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from hello_pb2 import HelloRequest, HelloReply


class Greeter(GreeterServicer):
    def SayHello(self, request, context):
        print(f"receive request: {request.name}")
        return HelloReply(message=f"Hello {request.name}")


if __name__ == '__main__':
    # 1. 实例化 server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # 2. 注册 Greeter
    add_GreeterServicer_to_server(Greeter(), server)
    # 3. 绑定端口
    server.add_insecure_port('[::]:50051')
    # 4. 启动服务
    server.start()
    server.wait_for_termination()

