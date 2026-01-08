import threading, requests, time, random

"""
- A thread is allowed to be sequential.
- Concurrency comes from having multiple threads, not from making one thread complex.
"""
class YahooFinancePriceScheduler(threading.Thread):
    def __init__(self, input_queue, **kwargs):
        super().__init__(**kwargs)
        self._input_queue = input_queue
        self.start()

    def run(self):
        while True:
            # get() waits till it gets a value
            # Thread waits
            val = self._input_queue.get()
            if val == 'DONE':
                break
                
            yahooFinancePriceWorker = YahooFinancePriceWorker(symbol=val)
            price = yahooFinancePriceWorker.get_price()

            print(price)

            # Rate Limiting, slow down requests
            time.sleep(random.random())


class YahooFinancePriceWorker():
    """Company object initialised by its symbol"""
    def __init__(self, symbol, **kwargs):
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


