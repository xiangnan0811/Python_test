import datetime
import json
import time
import uuid

from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(
    bootstrap_servers='192.168.2.240:9092',
)
topic = "spider"


def test():
    print("begin")
    try:
        n = 0
        while True:
            dic = {}
            dic['id'] = n
            dic['uuid'] = str(uuid.uuid4().hex)
            dic['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            producer.send(topic, json.dumps(dic).encode('utf-8'))
            print(f"send: {json.dumps(dic)}")
            time.sleep(0.5)
    except KafkaError as e:
        print(e)
    finally:
        producer.close()
        print("end")


if __name__ == '__main__':
    test()
