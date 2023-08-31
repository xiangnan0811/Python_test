import asyncio
import logging

import grpc
from proto import async_pb2, async_pb2_grpc

_cleanup_coroutines = []


class Greeter(async_pb2_grpc.GreeterServicer):

    async def SayHello(
            self, request: async_pb2.HelloRequest,
            context: grpc.aio.ServicerContext) -> async_pb2.HelloReply:
        logging.info('Received request, sleeping for 4 seconds...')
        await asyncio.sleep(4)
        logging.info('Sleep completed, responding')
        return async_pb2.HelloReply(message='Hello, %s!' % request.name)


async def serve() -> None:
    server = grpc.aio.server()
    async_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logging.info("Starting server on %s", listen_addr)
    await server.start()

    async def server_graceful_shutdown():
        logging.info("Starting graceful shutdown...")
        # Shuts down the server with 5 seconds of grace period. During the
        # grace period, the server won't accept new connections and allow
        # existing RPCs to continue within the grace period.
        await server.stop(5)

    _cleanup_coroutines.append(server_graceful_shutdown())
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(serve())
    except KeyboardInterrupt:
        logging.info("Shutting down server...")
    finally:
        loop.run_until_complete(*_cleanup_coroutines)
        loop.close()
        logging.info("Server shut down")
