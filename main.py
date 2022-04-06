import requests
#import json
from bs4 import BeautifulSoup as BS


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4878.0 Safari/537.36'
    }

def get_articles(url):
    #print("hello")
    s = requests.session()
    response = s.get(url=url, headers=headers)
    soup = BS(response.text, 'lxml')
    items = soup.find_all('div', class_='search-registry-entry-block')
    print(f'Получено {len(items)} записей.')
    for i in items:
        types_law = i.find('div', class_='registry-entry__header-top__title').text.strip().split('\n')
        types = types_law[0].strip()
        law = types_law[1].strip()
        print(f'|{types}_{law}|')
                                    
                                

def main():
    #print("hello")
    get_articles(url="https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString&morphology=on&strictEqual=on&openMode=USE_DEFAULT_PARAMS&pageNumber=1&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&fz44=on&fz223=on&fz94=on&orderNumber&placingWaysList&placingWaysList223&priceFrom&priceTo&currencyId&participantName&publishDateFrom&publishDateTo&updateDateFrom&updateDateTo&customerTitle&customerCode&customerFz94id&customerFz223id&customerInn&agencyTitle=+...++%D0%97%D0%94%D0%A0%D0%90%D0%92%D0%9E%D0%9E%D0%A5%D0%A0%D0%90%D0%9D%D0%95%D0%9D%D0%98%D0%AF+%22%D0%A6%D0%95%D0%9D%D0%A2%D0%A0%D0%90%D0%9B%D0%AC%D0%9D%D0%90%D0%AF+%D0%93%D0%9E%D0%A0%D0%9E%D0%94%D0%A1%D0%9A%D0%90%D0%AF+%D0%91%D0%9E%D0%9B%D0%AC%D0%9D%D0%98%D0%A6%D0%90%22+%D0%93%D0%9E%D0%A0%D0%9E%D0%94%D0%90+%D0%94%D0%9E%D0%9D%D0%95%D0%A6%D0%9A%D0%90+%D0%A0%D0%9E%D0%A1%D0%A2%D0%9E%D0%92%D0%A1%D0%9A%D0%9E%D0%99+%D0%9E%D0%91%D0%9B%D0%90%D0%A1%D0%A2%D0%98&agencyCode=03583000707&agencyFz94id=688357&agencyFz223id&agencyInn=6145000407&districts&regions&af=on&ca=on&deliveryAddress&sortBy=UPDATE_DATE#")

if __name__ == "__main__":
    main()

