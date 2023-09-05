from orm.peewee_test.model_define import main as model_define_main
from grpc_hello.server import main as grpc_hello_server_main
from orm.peewee_test.joins import main as joins_main


if __name__ == '__main__':
    # peewee 库的模型定义 demo
    # model_define_main()

    # peewee 库的 joins demo
    joins_main()

    # grpc hello demo
    # grpc_hello_server_main()
