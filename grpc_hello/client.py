import grpc

import hello_pb2, hello_pb2_grpc


if __name__ == '__main__':
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        res: hello_pb2.HelloReply = stub.SayHello(hello_pb2.HelloRequest(name="world"))
        print(res.message)
