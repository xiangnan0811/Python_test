import sys
import json
import traceback
import redis
from kafka.structs import TopicPartition
from loguru import logger
from kafka import KafkaConsumer


class ConsumerOfKafka:

    _MESSAGE_NAME = 'tb_order'

    def __init__(self, host, client_id):
        self.host = host
        self.client_id = client_id
        self.conn = RedisClient()

    @property
    def consumer_client(self, group_id=None):
        return KafkaConsumer(
            self._MESSAGE_NAME,
            bootstrap_servers=self.host,
            client_id=self.client_id,
            auto_offset_reset='earliest',
            group_id=group_id,
            value_deserializer=lambda m: json.loads(m.decode()) 
        )

    def close(self):
        return self.consumer_client.close()

    def consumer(self):
        try:
            consumer = self.consumer_client
            for msg in consumer:
                order = msg.value
                client = order.get('client', None)
                user_id = order.get('user_id', None)
                if client and user_id:
                    self.check_user_client(user_id=user_id, order_client=client)
        except Exception as e:
            type_, value, traceback_ = sys.exc_info()
            logger.error(f'send msg ext has an error, please check: {type_}, {value}, {traceback.format_tb(traceback_)}')
        finally:
            if self.consumer_client:
                self.close()

    def check_user_client(self, user_id, order_client):
        user_client = self.conn.search_user_client(user_id)
        if not user_client:
            print(f'用户 -> {user_id} 不存在 或 用户未导入Redis')
            return False
        if user_client != order_client:
            print(f'用户 -> {user_id} 订单虚拟机 -> {order_client} 与用户虚拟机 -> {user_client} 不一致')
            return False
        return True

    def consumer_seek(self, partition=1, offset=0):
        try:
            consumer = self.consumer_client
            consumer.seek(TopicPartition(self._MESSAGE_NAME, partition=partition), offset=offset)
            for msg in consumer:
                print(msg)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            type_, value, traceback_ = sys.exc_info()
            logger.error(f'send msg ext has an error, please check: {type_}, {value}, {traceback.format_tb(traceback_)}')
        finally:
            self.close()

    def consumer_assign(self, partition=1):
        try:
            consumer = self.consumer_client
            consumer.assign([TopicPartition(self._MESSAGE_NAME, partition=partition)])
            for msg in consumer:
                print(msg)
        except Exception as e:
            type_, value, traceback_ = sys.exc_info()
            logger.error(f'send msg ext has an error, please check: {type_}, {value}, {traceback.format_tb(traceback_)}')
        finally:
            self.close()


class RedisClient:
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



if __name__ == '__main__':
    kafka_consumer = ConsumerOfKafka(host='192.168.2.240:9092', client_id='test')
    kafka_consumer.consumer()
