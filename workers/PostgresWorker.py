import threading
import os
from dotenv import load_dotenv

from queue import Empty

from sqlalchemy import create_engine
from sqlalchemy.sql import text

class PostgresMasterScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            try:
                # Wait till it gets value
                val = self._input_queue.get(timeout=10)
            except Empty:
                print('Timeout reached in postgres scheduler, Stopping...')
                break

            # Signal to stop the thread
            if val == 'DONE':
                break
            
            symbol, price, extracted_time = val     # List or Tuple
            postgresWorker = PostgresWorker(symbol, price, extracted_time)
            postgresWorker.insert_into_db()

class PostgresWorker():
    def __init__(self, symbol, price, extracted_time):
        self._symbol = symbol
        self._price = price
        self._extracted_time = extracted_time

        load_dotenv()
        self._PG_USER = os.environ.get('PG_USER') or ''
        self._PG_PW = os.environ.get('PG_PW') or ''
        self._PG_HOST = os.environ.get('PG_HOST') or 'localhost'
        self._PG_DB = os.environ.get('PG_DB') or 'postgres'

        # Create database engine
        self._engine = create_engine(f'postgresql://{self._PG_USER}:{self._PG_PW}@{self._PG_HOST}/{self._PG_DB}')


    def create_insert_query(self):
        SQL = """INSERT INTO prices (symbol, price, extracted_time) VALUES (:symbol, :price, :extracted_time)"""   # 2022-02-02 15:00:00
        return SQL
    

    def insert_into_db(self):
        insert_query = self.create_insert_query()

        # Open connection 
        # with self._engine.connect() as conn:
        with self._engine.begin() as conn:
            conn.execute(text(insert_query),
                         {'symbol': self._symbol,
                          'price': self._price,
                          'extracted_time': str(self._extracted_time)})
