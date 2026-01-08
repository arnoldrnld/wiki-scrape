"""This code can be an example of Producer-Consumer Architecture
- Used in web servers, job-queues, scrapers etc
"""

import time
from multiprocessing import Queue

from workers.WikiWorker import WikiWorker
from workers.YahooFinanceWorkers import YahooFinancePriceScheduler


def main():
    symbol_queue = Queue()
    calc_start_time = time.time()
    
    wikiWorker = WikiWorker()
    # Track threads
    yahoo_finance_price_scheduler_threads = []
    num_yahoo_finance_price_workers = 4

    # Multiple workers run same time
    # As Queue prevent race condition, no two threads work on same symbol
    for i in range(num_yahoo_finance_price_workers):
        # We initialise the thread, input_queue is empty
        # Thread start waiting for value in input_queue
        yahooFinancePriceScheduler = YahooFinancePriceScheduler(input_queue=symbol_queue)
        yahoo_finance_price_scheduler_threads.append(yahooFinancePriceScheduler)

    # symbol_queue gets value , thus input_queue will have value, both points to same queue object
    for symbol in wikiWorker.get_sp_500_companies():
        symbol_queue.put(symbol)

    # Add 'DONE' for number of threads
    # So each thread will stop gracefully
    for i in range(len(yahoo_finance_price_scheduler_threads)):
        symbol_queue.put('DONE')

    for thread in yahoo_finance_price_scheduler_threads:
        thread.join()

    print(f'Time taken: {round(time.time() - calc_start_time, 2)}')
        
    
if __name__=='__main__':
    main()    

"""Next Steps
ONE
- Integrate Postgres
- Use sqlalchemy
- Store credentials as environment variables
- Design it as PostgresWorkers running parallelly with PostgresSchedulers"""