import signal
from concurrent import futures
from datetime import datetime
import sys
import argparse

import grpc

from .hello_pb2_grpc import GreeterServicer, add_GreeterServicer_to_server
from .hello_pb2 import HelloRequest, HelloReply
from log.logger import init_logger

logger = init_logger(log_file_name='grpc_hello_server')


def on_exit(signal, frame):
    logger.error(f"进程中断！, signal: {signal}")
    sys.exit(0)


class LogInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details: grpc.HandlerCallDetails):
        logger.debug(f"Received request: {handler_call_details}")
        return continuation(handler_call_details)


class Greeter(GreeterServicer):
    def SayHello(self, request: HelloRequest, context):
        # metadata
        for key, value in context.invocation_metadata():
            logger.debug(f"Received metadata: {key}={value}")
        context.set_trailing_metadata((
            ("token", "456"),
            ("retry", "false"),
        ))
        logger.debug(f"receive request: {request.name}, gender: {request.gender}, addtime: {datetime.fromtimestamp(request.addTime.seconds)}")
        reply = HelloReply(message=f"Hello, {request.name}")
        # context.set_code(grpc.StatusCode.NOT_FOUND)
        return reply


def parse_args():
        # 参数解析
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host",
        nargs="?",
        type=str,
        default="127.0.0.1",
        help="binding host"
    )
    parser.add_argument(
        "--port",
        nargs="?",
        type=int,
        default=50051,
        help="the listening port"
    )
    args = parser.parse_args()
    return args

def main():
    # 0. 解析参数
    args = parse_args()
    # 1. 实例化 server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # server = grpc.aio.server(
    #     migration_thread_pool=futures.ThreadPoolExecutor(max_workers=10),
    #     interceptors=[LogInterceptor()],
    # )
    # 2. 注册 Greeter
    add_GreeterServicer_to_server(Greeter(), server)
    # 3. 绑定端口
    server.add_insecure_port(f'{args.host}:{args.port}')
    # 4. 启动服务
    # 主进程退出信号监听 并优雅退出
    signal.signal(signal.SIGINT, on_exit)               # Control + C
    signal.signal(signal.SIGTERM, on_exit)              # kill
    logger.info(f"启动服务：{args.host}:{args.port}")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    main()
