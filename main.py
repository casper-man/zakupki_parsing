import requests
import json
import csv
import jinja2
from bs4 import BeautifulSoup as BS
from prettytable import PrettyTable
from fake_headers import Headers
from progress.bar import Bar, ShadyBar
from progress.spinner import Spinner, PieSpinner

header = Headers(browser="chrome", os="win", headers=True)

def preview(text):
    text_short = (text[:23] + '..') if len(text) > 25 else text
    return text_short

def save_json(data):
    bar = PieSpinner('save_json ')
    with open(f"test_data.json", "w") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        bar.next()
    bar.finish()


def save_csv(data):
    bar = ShadyBar('save_csv',max=len(data))
    with open(f"test_data.csv", "w", newline='') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'id_articles',
                'link',
                'owner',
                'owner_link',
                'object_buy',
                'law',
                'types',
                'status',
                'start_price',
                'date_begin',
                'date_update',
                'date_stop'
            )
        )
        for i in data:
            writer.writerow(
            (
                i['id_articles'],
                i['link'],
                i['owner'],
                i['owner_link'],
                i['object_buy'],
                i['law'],
                i['types'],
                i['status'],
                i['start_price'],
                i['date_begin'],
                i['date_update'],
                i['date_stop']
                )
            )
            bar.next()

    bar.finish()

def save_html(data):


    templateLoader = jinja2.FileSystemLoader(searchpath="./")
    templateEnv = jinja2.Environment(loader=templateLoader)
    TEMPLATE_FILE = "test_template.html"
    template = templateEnv.get_template(TEMPLATE_FILE)
    
    template_0 = jinja2.Template("""\
    <title>{{ title }}</title>
    <ul>
    {% for user in users %}
      <li><a href="{{ user.url }}">{{ user.username }}</a></li>
    {% endfor %}
    </ul>
    """)

    users = [
        {'username': '1', 'url': 'https://a.bc/user/1'},
        {'username': '2', 'url': 'https://a.bc/user/2'},
        {'username': '3', 'url': 'https://a.bc/user/3'}
    ]

    html = template.render(title="Hello World!", data=data)
    #with open(f"test_data.html", "w") as file:
    #    file.writer(html)
    print(html)

def get_articles(url):
    th = ['№','Статус','Тип','Закон','Объект покупки','Стартовая цена','Размещено','Обновлено','Окончание']
    table = PrettyTable(th)
    s = requests.session()

    response = s.get(url=f'{url}', headers=header.generate())
    soup = BS(response.text, 'lxml')
    paginator = soup.find_all('a', attrs={'class':'page__link'})
    try:
        pages = int(paginator[-1].find('span').text)
    except:
        pages = 1
    bar = ShadyBar('Получение записей',max=pages)
    page = 0
    items = []

    items_dict = []

    while page <= pages:
        page += 1
        response = s.get(url=f'{url}&pageNumber={page}', headers=header.generate())
        soup = BS(response.text, 'lxml')             
        items = items + soup.find_all('div', class_='search-registry-entry-block')
        
        #print(f'Получены данные с {page}/{pages} ')
        bar.next()
        if page == pages:
            break


    bar.finish()
    print(f'Получено {len(items)} записей.')
        
    # save_json(items)
    # save_csv(items)
    # save_html(items)

    for item in range(len(items)):
        i = items[item]
        th = []
        types_law = i.find('div', class_='registry-entry__header-top__title').text.strip().split('\n')
        law = types_law[0].strip()
        types = types_law[1].strip()
        link = i.find('div', class_="registry-entry__header-mid__number").find('a').get('href')
        id_articles = i.find('div', class_="registry-entry__header-mid__number").find('a').text.replace('№','').strip()
        status = i.find('div', class_="registry-entry__header-mid__title").text.strip()
        start_price = i.find('div', class_="price-block__value").text.strip() #.replace('₽','').strip()
        dates = i.find('div', class_="data-block").find_all('div', class_='data-block__value')
        date_begin = dates[0].text
        date_update = dates[1].text
        try:
            date_stop = dates[2].text
        except:
            date_stop = None
        object_buy = i.find('div', class_="registry-entry__body-value").text.replace(u'\xa0','').replace('\n','').strip()
        owner_link = i.find('div', class_="registry-entry__body-href").find('a').get('href')
        owner = i.find('div', class_="registry-entry__body-href").find('a').text.strip()

        items_dict.append({
            'id_articles': id_articles,
            'link': f'https://zakupki.gov.ru{link}',
            'owner': owner,
            'owner_link': f'https://zakupki.gov.ru{owner_link}',
            'object_buy': object_buy,
            'law': law,
            'types': types,
            'status': status,
            'start_price': float('{:.2f}'.format(float(start_price.replace('₽','').replace(u'\xa0','').replace(',','.').strip()))),
            'date_begin': date_begin,
            'date_update': date_update,
            'date_stop': date_stop
        })

        # print(f'|{id_articles} - ({status})\t{types}_{law}|\n|\tstart_price = {start_price} dates {date_begin},{date_update},{date_stop}|')
        table.add_row([id_articles,preview(status),preview(types),law,preview(object_buy),start_price,date_begin,date_update,date_stop])

    print(table)                                
    save_csv(items_dict)                                 
    save_json(items_dict)      
    save_html(items_dict)                         
                                

def main():
    state = ''
    applying = True     # Подача заявок
    commission = True   # Работа комиссии
    completed = False   # Закупка завершена
    canceled = False    # Закупка отменена
        
    state += ('&af=on') if applying else ''
    state += ('&ca=on') if commission else ''
    state += ('&pc=on') if completed else ''
    state += ('&pa=on') if canceled else ''

    laws = ''
    fz44 = True         # 44-ФЗ
    fz223 = True        # 223-ФЗ
    pp615 = True        # ПП РФ 615 (Капитальный ремонт)
    fz94 = True         # 94-ФЗ
   
    laws += ('&fz44=on') if fz44 else ''
    laws += ('&fz223=on') if fz223 else ''
    laws += ('&ppRf615=on') if pp615 else ''
    laws += ('&fz94=on') if fz94 else ''

    searchString = 6145000407   # Строка поиска

    url = f"https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString={searchString}&recordsPerPage=_50{laws}{state}"
    # print(url)
    get_articles(url=url)

if __name__ == "__main__":
    main()

