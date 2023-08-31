import json
import redis
from pyspark.sql import SparkSession


class RedisClient:
    pool = None
    def __init__(self):
        self.get_redis_pool()
    
    def get_redis_pool(self):
        self.pool = redis.ConnectionPool(
            host='192.168.2.240',
            port=6379,
            password='',
            db=1,
            encoding="utf-8",
            decode_responses=True
        )
        return self.pool

    def search_user_client(self, user_id, name='lxs_user'):
        if not self.pool:
            self.pool = self.get_redis_pool()
        r = redis.StrictRedis(connection_pool=self.pool)
        return r.hget(name, user_id)


class CheckUser:

    @staticmethod
    def check_user_client(row):
        order = json.loads(row.value.decode())
        user_id = order.get('user_id', '')
        if not user_id:
            return False
        order_client = order.get('client', '')
        r = RedisClient()
        user_client = r.search_user_client(user_id)
        if not user_client:
            print(f'用户 -> {user_id} 不存在 或 用户未导入Redis')
            return False
        if user_client != order_client:
            print(f'用户 -> {user_id} 订单虚拟机 -> {order_client} 与用户虚拟机 -> {user_client} 不一致')
            return False
        return True


    def start(self):
        spark = SparkSession \
                .builder \
                .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2') \
                .getOrCreate()
        df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "192.168.2.240:9092") \
            .option("subscribe", "tb_order") \
            .load()
        df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        # query1 = df.writeStream.format("console").queryName('value').start()
        query1 = df.writeStream.foreach(self.check_user_client).start()

        df.printSchema()
        query1.awaitTermination()


if __name__ == '__main__':
    check = CheckUser()
    check.start()
