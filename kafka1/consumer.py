import sys
import json
import traceback
from kafka.structs import TopicPartition
from loguru import logger
from kafka import KafkaConsumer


class ConsumerOfKafka:

    _MESSAGE_NAME = 'tb_order'

    def __init__(self, host, client_id):
        self.host = host
        self.client_id = client_id

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
                print(msg)
        except KeyboardInterrupt:
            pass
        except Exception:
            type_, value, traceback_ = sys.exc_info()
            logger.error(f'send msg ext has an error, please check: {type_}, {value}, {traceback.format_tb(traceback_)}')
        finally:
            if self.consumer_client:
                self.close()

    def consumer_seek(self, partition=1, offset=0):
        try:
            consumer = self.consumer_client
            consumer.seek(TopicPartition(self._MESSAGE_NAME, partition=partition), offset=offset)
            for msg in consumer:
                print(msg)
        except Exception:
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
        except Exception:
            type_, value, traceback_ = sys.exc_info()
            logger.error(f'send msg ext has an error, please check: {type_}, {value}, {traceback.format_tb(traceback_)}')
        finally:
            self.close()

