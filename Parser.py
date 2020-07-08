import urllib.parse
from collections import namedtuple
import re
import bs4
import requests
import time
import telebot
#import TelegramBot
#HTTP API: Bot 923519796:AAFJ92lf4eAJnZuLFtY0JX7_6Lqnup6DBYo


InnerBlock = namedtuple('Block', 'title,price,url')
avitoData=[]
avitoData2=[]
class Block(InnerBlock):

    def __str__(self):

        return f'{self.title}\t{self.price}\t{self.url}'
class AvitoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.2 Safari/605.1.15',
            'Accept-Language': 'ru',
        }
    def get_page(self, page: int = None):
        params = {
            #'geoCoords': '59.99902367258219%2C30.27511991730142',
            #'radius': 5,
            'cd': 1,
            'pmax': 5000,
            'pmin': 100,
            'user': 1,
            'q': 'xiaomi+redmi+4x',
        }
        if page and page > 1:
            params['p'] = page

        #url = 'https://www.avito.ru/moskva/avtomobili/bmw/5'
        #url = 'https://www.avito.ru/sankt-peterburg/telefony/xiaomi-ASgBAgICAUSeAoakAg'
        #r = self.session.get(url, params=params)
        r = self.session.get('https://www.avito.ru/sankt-peterburg/telefony/xiaomi-ASgBAgICAUSeAoakAg?geoCoords=59.999630225558036%2C30.276290826049145&radius=5&user=1&q=xiaomi+redmi+4x')
        print(r)
        return r.text
    def get_blocks(self, page: int = None):
        text = self.get_page(page=page)
        soup = bs4.BeautifulSoup(text, 'lxml')

        # Запрос CSS-селектора, состоящего из множества классов, производится через select
        container = soup.select('div.snippet-horizontal.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended')
        for item in container:
            block = self.parse_block(item=item)
            filter = ['модул', 'диспле', 'заменой', 'аккумулятор', 'запчасти', 'стёкл', 'стекл','адаптер',"чехлы", "чехол",'пленк',"плёнк","аксессуар", "коробк", "рамк","плат","крышк"]
            tmp_x=0
            for t in filter:
                block_tmp=str(block)
                block_tmp=block_tmp.lower()
                if re.search(t, str(block_tmp)):
                    #print(t)
                    #print(block_tmp)
                    tmp_x=+1
                    #print(tmp_x)
                else:
                    pass
            if tmp_x==0:
                avitoData.append(block)
                #print(avitoData)
                tmp_x=0
            else:
                pass
                tmp_x = 0

    def parse_block(self, item):
        # Выбрать блок со ссылкой
        url_block = item.select_one('a.snippet-link')
        href = url_block.get('href')
        if href:
            url = 'https://www.avito.ru' + href
        else:
            url = None

        # Выбрать блок с названием
        title_block = item.select_one('a.snippet-link')
        title = title_block.string.strip()

        # Выбрать блок с названием и валютой
        price_block = item.select_one('span.snippet-price ')
        price=price_block.string.strip()
        total=str(title)+'  '+str(price)+'  '+str(url)
        return total

    def get_pagination_limit(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')

        container = soup.select('a.pagination-page')
        if len(container) == 0:
            return 1
        last_button = container[-1]
        href = last_button.get('href')
        if not href:
            return 1

        r = urllib.parse.urlparse(href)
        params = urllib.parse.parse_qs(r.query)
        return int(params['p'][0])

    def parse_all(self):
        limit = self.get_pagination_limit()
        print(f'Всего страниц: {limit}')

        for i in range(1, limit + 1):
            self.get_blocks(page=i)
    def database(self, avitoData):
        x=avitoData
        avitoData=[]
        return x
def main():
    x=1
    while x==1:
        p=AvitoParser()
        p.parse_all()
        x=p.database(avitoData)
        return x
        x=[]
bot = telebot.TeleBot('923519796:AAFJ92lf4eAJnZuLFtY0JX7_6Lqnup6DBYo')
X=1
AvitoBase1 = []
AvitoBase2 = []
p=AvitoParser()
ressult2 = []
filter_message=0
while X==1:
    p.parse_all()
    AvitoBase1=avitoData
    print(len(AvitoBase1))
    print(len(AvitoBase2))
    if AvitoBase2==[]:
        AvitoBase2=AvitoBase1
        bot.send_message(-1001310833138, "Касандра(version 0.05) На сервере, начинет ослеживание Avito каждые 2 минуты")
    else:
        result = list(set(AvitoBase1) - set(AvitoBase2))
        print(result) 

        for t in result:
            for t2 in ressult2:
                if t == t2:
                    filter_message=1
            if filter_message == 0:
                ressult2.append(t)
                bot.send_message(-1001310833138, t)
                print(t)
            else:
                filter_message=0

        AvitoBase2 = AvitoBase1
        AvitoBase1 = []
        avitoData = []
        print(filter_message)

    time.sleep(120)

