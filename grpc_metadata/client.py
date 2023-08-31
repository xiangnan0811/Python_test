import grpc

from proto import hello_pb2, hello_pb2_grpc


if __name__ == '__main__':
    with grpc.insecure_channel("localhost:8080") as channel:
        stub = hello_pb2_grpc.GreeterStub(channel)
        response, call = stub.SayHello.with_call(
            hello_pb2.HelloRequest(name="world"),
            metadata=(
                ("token", "123"),
                ("user-agent", "xxxx-python-grpc-client"),
            )
        )
    print(response.message)
    for key, value in call.trailing_metadata():
        print(f"Greeter client received trailing metadata: {key}={value}")
