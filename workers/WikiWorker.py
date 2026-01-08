import requests
from bs4 import BeautifulSoup


class WikiWorker():
    def __init__(self):
        self._url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'


    # we are not using any self instances, so we make it static method
    @staticmethod
    def _extract_company_symbols(page_html):
        soup = BeautifulSoup(page_html, 'html.parser')   #, 'lxml')
        table = soup.find(id='constituents')
        table_rows = table.find_all('tr')

        for table_row in table_rows[1:]:
            symbol = table_row.find('td').text.strip('\n')
            yield symbol

    def get_sp_500_companies(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(self._url, headers=headers)
        if response.status_code != 200:
            print("Couldnt get entries")
            return
        
        yield from self._extract_company_symbols(response.text)


if __name__=='__main__':
    wikiWorker = WikiWorker()
    
    for symbol in wikiWorker.get_sp_500_companies():
        print(symbol)
        break

    symbol_list = []
    for symbol in wikiWorker.get_sp_500_companies():
        symbol_list.append(symbol)

    print(len(symbol_list))
    print(symbol_list[-1])