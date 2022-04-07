import requests
#import json
from bs4 import BeautifulSoup as BS
from prettytable import PrettyTable
from fake_headers import Headers

header = Headers(browser="chrome", os="win", headers=True)

def get_articles(url):
    th = ['№','Статус','Закон','Тип','Стартовая цена','Размещено','Обновлено','Окон. подачи заявок']
    table = PrettyTable(th)
    s = requests.session()

    pages = 1
    page = 0
    items = []

    while page <= pages:
        page += 1
        response = s.get(url=f'{url}&pageNumber={page}', headers=header.generate())
        soup = BS(response.text, 'lxml')
        paginator = soup.find_all('a', attrs={'class':'page__link'})
        try:
            pages = int(paginator[-1].find('span').text)
        except Exception as e:
            #print(e)
            pages = 1
             
        items = items + soup.find_all('div', class_='search-registry-entry-block')
        
        print(f'Получены данные с {page}/{pages} ')
        if page == pages:
            break

    print(f'Получено {len(items)} записей.')
        
    for item in range(len(items)):
        i = items[item]
        th = []
        types_law = i.find('div', class_='registry-entry__header-top__title').text.strip().split('\n')
        types = types_law[0].strip()
        law = types_law[1].strip()
        nomber = i.find('div', class_="registry-entry__header-mid__number").find('a').get('href').split('=')[1]
        status = i.find('div', class_="registry-entry__header-mid__title").text.strip()
        start_price = i.find('div', class_="price-block__value").text.replace('&nbsp;','_').replace('₽','').strip()
        dates = i.find('div', class_="data-block").find_all('div', class_='data-block__value')
        date_cri = dates[0].text
        date_upd = dates[1].text
        try:
            date_stop = dates[2].text
        except Exception as e:
            date_stop = None
            #raise e 
        object_buy = i.find('div', class_="registry-entry__body-value").text.strip()
        #print(f'|{nomber} - ({status})\t{types}_{law}|\n|\tstart_price = {start_price} dates {date_cri},{date_upd},{date_stop}|')
        table.add_row([nomber,status,law,types,start_price,date_cri,date_upd,date_stop])

    print(table)                                
                                

def main():
    state = ''
    applying = True     # Подача заявок
    commission = True   # Работа комиссии
    completed = False   # Закупка завершена
    canceled = False    # Закупка отменена
    
    if applying: state += '&af=on'
    if commission: state += '&ca=on'
    if completed: state += '&pc=on'
    if canceled: state += '&pa=on'

    laws = ''
    fz44 = True         # 44-ФЗ
    fz223 = True        # 223-ФЗ
    pp615 = True        # ПП РФ 615 (Капитальный ремонт)
    fz94 = True         # 94-ФЗ
   
    if fz44: laws += '&fz44=on'
    if fz223: laws += '&fz223=on'
    if pp615: laws += '&ppRf615=on'
    if fz94: laws += ' &fz94=on'

    inn=6145000407      # ИНН Организации
    print(f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={inn}&recordsPerPage=_50{laws}{state}")
    get_articles(url=f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={inn}&recordsPerPage=_50{laws}{state}")

if __name__ == "__main__":
    main()

