import threading, requests, time, random
from queue import Empty

from datetime import datetime, timezone

"""
- A thread is allowed to be sequential.
- Concurrency comes from having multiple threads, not from making one thread complex.
"""
class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, output_queue, **kwargs):
        super().__init__(**kwargs)
        self._input_queue = input_queue

        temp_queue = output_queue   # List or Tuple
        if type(temp_queue) != list:
            temp_queue = [temp_queue]     # List

        self._output_queues = temp_queue
        self.start()


    def run(self):
        while True:
            # get() waits till it gets a value
            # Thread waits
            try:
                val = self._input_queue.get(timeout=10)
            except Empty:   # Empty exception
                print('Yahoo scheduler queue is empty, Stopping...')
                break
            
            if val == 'DONE':
                for output_queue in self._output_queues:
                    output_queue.put('DONE')
                break
                
            yahooFinancePriceWorker = YahooFinancePriceWorker(symbol=val)
            price = yahooFinancePriceWorker.get_price()

            for output_queue in self._output_queues:
                output_values = (val, price, datetime.now(timezone.utc))
                output_queue.put(output_values)
            time.sleep(random.random())


class YahooFinancePriceWorker():
    """Company object initialised by its symbol"""
    def __init__(self, symbol):
        self._symbol = symbol
        base_url = 'https://query2.finance.yahoo.com/v8/finance/chart/'
        self._url = f'{base_url}{self._symbol}'


    def get_price(self):
        """Return stock price associated with the symbol"""
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self._url,headers=headers)
        if response.status_code != 200:
            print("Couldnt get price")
            return

        json_data = response.json()
        price = round(json_data['chart']['result'][0]['meta']['regularMarketPrice'], 2)
        return price


if __name__=='__main__':
    p = YahooFinancePriceWorker('MMM')
    print(p.get_price())
    print(p.__doc__)
    print(p.get_price.__doc__)


