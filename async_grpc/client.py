from __future__ import print_function

import logging

import grpc
from proto import async_pb2, async_pb2_grpc


def run():
    with grpc.insecure_channel(
            'localhost:50051',
            options=[('grpc.lb_policy_name', 'pick_first'),
                     ('grpc.enable_retries', 0),
                     ('grpc.keepalive_timeout_ms', 10000)]
    ) as channel:
        stub = async_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(async_pb2.HelloRequest(name='you'), timeout=10)
    print(f"Greeter client received: {response.message}")


if __name__ == '__main__':
    logging.basicConfig()
    run()
