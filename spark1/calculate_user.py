import json
import redis
from pyspark.sql import SparkSession


class CalculateUser:

    def start(self):
        spark = SparkSession \
                .builder \
                .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2') \
                .getOrCreate()
        df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "192.168.2.240:9092") \
            .option("subscribe", "user_info") \
            .load()
        df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
        # query1 = df.writeStream.format("console").queryName('value').start()
        query1 = df.writeStream.foreach(self.calculate).start()

        df.printSchema()
        query1.awaitTermination()

    def calculate(self, row):
        """计算用户属性"""
        user = json.load(row.decode('utf-8'))
        print(user)


if __name__ == '__main__':
    client = CalculateUser()
    client.start()
