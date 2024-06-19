import logging
import os
from time import sleep

from clickhouse_connect import get_client
from clickhouse_connect.driver import exceptions
from clickhouse_connect.driver.client import Client
from clickhouse_connect.driver.query import QueryResult
from dotenv import load_dotenv

# Load configuration from .env file
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DBHelper:
    def __init__(self, host=None, port=None, username=None, password=None, database=None):
        self.host = host or os.getenv('CLICKHOUSE_HOST')
        self.port = port or os.getenv('CLICKHOUSE_PORT')
        self.username = username or os.getenv('CLICKHOUSE_USER')
        self.password = password or os.getenv('CLICKHOUSE_PASSWORD')
        self.database = database or os.getenv('CLICKHOUSE_DATABASE')
        self.client = None
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """
        Establish a connection to the ClickHouse database with retry mechanism.
        """
        for attempt in range(self.max_retries):
            try:
                self.client: Client = get_client(
                    host=self.host,
                    port=self.port,
                    username=self.username,
                    password=self.password,
                    database=self.database
                )
                logging.info("Connection to ClickHouse established successfully.")
                return
            except exceptions.Error as e:
                logging.error(f"Failed to connect to ClickHouse: {e}")
                if attempt < self.max_retries - 1:
                    logging.info(f"Retrying in {self.retry_delay} seconds...")
                    sleep(self.retry_delay)
                else:
                    logging.critical("Max retries reached. Could not connect to ClickHouse.")
                    raise

    def execute_query(self, query, params=None):
        """
        Execute a query and return the results.
        
        :param query: SQL query to be executed
        :param params: Optional dictionary of parameters to bind to the query
        :return: Query results
        """
        if self.client is None:
            logging.error("Not connected to ClickHouse.")
            return None

        try:
            results: QueryResult = self.client.query(query, parameters=params)
            logging.info("Query executed successfully.")
            return results
        except exceptions.Error as e:
            logging.error(f"Query execution failed: {e}")
            return None

    def close(self):
        """
        Close the connection to the ClickHouse database.
        """
        if self.client:
            self.client.close()
            self.client = None
            logging.info("Connection to ClickHouse closed.")

# Example usage
if __name__ == "__main__":
    with DBHelper(
        host="88.33.100.47",
        port=8123,
        username="default",
        password="123333",
        database="default"
    ) as db_helper:
        query = """
SELECT 
    f1.relation_field,
    f1.zxrq,
    f1.fydm,
    f1.dj,
    f1.sl,
    f1.je,
    f2.fydm AS fydm1,
    f2.dj AS dj1,
    f2.sl AS sl1,
    f2.je AS je1,
    f3.fydm AS fydm2,
    f3.dj AS dj2,
    f3.sl AS sl2,
    f3.je AS je2
FROM 
    (SELECT * FROM default.fast_fee WHERE jssj BETWEEN '2021-05-01' AND '2024-04-30' AND fydm = '25030700102') AS f1
JOIN 
    (SELECT * FROM default.fast_fee WHERE jssj BETWEEN '2021-05-01' AND '2024-04-30' AND fydm = '25030700201') AS f2 
ON 
    f1.relation_field = f2.relation_field AND f1.zxrq = f2.zxrq
JOIN 
    (SELECT * FROM default.fast_fee WHERE jssj BETWEEN '2021-05-01' AND '2024-04-30' AND fydm = '25030702801') AS f3 
ON 
    f1.relation_field = f3.relation_field AND f1.zxrq = f3.zxrq
limit 10"""
        results = db_helper.execute_query(query)
        
        if results:
            print(f"Column names: {results.column_names}")
            # results.named_results
            print('-' * 100)
            for item in results.named_results():
                print(item)
            print('-' * 100)
