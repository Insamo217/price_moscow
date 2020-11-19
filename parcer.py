import requests
import csv
import lxml
import re
from bs4 import BeautifulSoup as bs
import pickle, shelve
import socks
import socket
import time

headers = {
    'accept': '*/*',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}


def checkIP():
    ip = requests.get('http://checkip.dyndns.org').content
    soup = bs(ip, 'html.parser')
    print(soup.find('body').text)


def change_IP():
    socks.set_default_proxy(socks.SOCKS5, "localhost", 9150)
    socket.socket = socks.socksocket
    time.sleep(11)


def cian_parce(href, headers):
    flats = []
    session = requests.Session()
    request = session.get(href, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('main', attrs={'data-name': 'OfferCardPage'})
        if len(divs) == 0:
            raise Exception
        for div in divs:
            try:
                title = div.find('h1', attrs={'data-name': 'OfferTitle'}).text
                price_digit = div.find('span', attrs={'itemprop': 'price'}).text
                metro_info = div.find('ul', attrs={'class': 'a10a3f92e9--undergrounds--2pop3'}).text
                total_area = div.find('div', attrs={'class': 'a10a3f92e9--info-block--3hCay'}).text
                repair = div.find('div', attrs={'data-name': 'GeneralInformation'}).text
                home = div.find('div', attrs={'class': 'a10a3f92e9--column--2oGBs'}).text
                district_info = div.find('address', attrs={'class': 'a10a3f92e9--address--140Ec'}).text
                pattern = r"[^A-Za-z0-9]+"
                price = (re.sub(pattern, '', price_digit))
                pattern = r"^\w+,\s\w+,\sр-н\s(\w{,17}\W?\w{,17}\s?\w{,17}),\s"
                district = ('\n'.join(re.findall(pattern, district_info)))
                pattern = r"^\w{,17}\W?\w{,17}\s?\w{,17}"
                metro_station = ('\n'.join(re.findall(pattern, metro_info)))
                pattern = r"^\w{,17}\W?\w{,17}\s?\w{,17}\s⋅\s\s(\d{1,2})\sмин.+"
                metro_time = ('\n'.join(re.findall(pattern, metro_info)))
                pattern = r"Дизайнерский|Евроремонт|Косметический"
                type_of_repair = ('\n'.join(re.findall(pattern, repair)))
                pattern = r"\d{4}"
                year_of_const = ('\n'.join(re.findall(pattern, home)))
                pattern = r"Монолитный|Кирпичный|Панельный|Блочный|Кирпично-монолитный|Сталинский"
                type_of_house = ('\n'.join(re.findall(pattern, home)))
                pattern = r"^\w+"
                area = ('\n'.join(re.findall(pattern, total_area)))
                pattern = r"(\d{,2})\sиз\s"
                floor = ('\n'.join(re.findall(pattern, total_area)))
                pattern = r"\sиз\s(\d{,3})Этаж"
                numb_of_floors = ('\n'.join(re.findall(pattern, total_area)))

                flats.append({
                    'title': title,
                    'price': price,
                    'district': district,
                    'metro_station': metro_station,
                    'metro_time': metro_time,
                    'area': area,
                    'floor': floor,
                    'numb_of_floors': numb_of_floors,
                    'type_of_repair': type_of_repair,
                    'year_of_const': year_of_const,
                    'type_of_house': type_of_house
                })
            except:
                pass
            print(title)
            print(price)
            print(district)
            print(metro_station)


    else:
        print('ERROR')
    return flats


def files_writer(flats):
    with open('cian_flats111.csv', 'a', encoding='utf8') as file:
        a_pen = csv.writer(file)
        for flat in flats:
            a_pen.writerow((flat['title'], flat['price'], flat['district'], flat['metro_station'], flat['metro_time'],
                            flat['area'], flat['floor'], flat['numb_of_floors'], flat['type_of_repair'],
                            flat['year_of_const'], flat['type_of_house']))  # запись в CSV


def cian_parce_flats(base_url, headers):
    hrefs = []
    num = 0
    print('Обновление IP')
    change_IP()
    checkIP()
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        print("Ответ с сервера положительный")
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'class': 'c6e8ba5398--main-container--1FMpY'})
        while len(divs) == 0:
            print('Список квартир не получен, меняем IP')
            change_IP()
            checkIP()
            session = requests.Session()
            request = session.get(base_url, headers=headers)
            if request.status_code == 200:
                print("Повторный ответ с сервера положительный")
                soup = bs(request.content, 'lxml')
                divs = soup.find_all('div', attrs={'class': 'c6e8ba5398--main-container--1FMpY'})
        if len(divs) != 0:
            print('Ссылки на объявления по текущей странице поиска')
        for div in divs:
            num += 1
            href = div.find('a', attrs={'class': 'c6e8ba5398--header--1fV2A'})['href']  # ссылка на объявление
            hrefs.append(href)
            print(num, ":", href)
        href_n = 0
        while href_n < len(hrefs):
            try:
                href = hrefs[href_n]
                print("Квартира №", href_n)
                flats = cian_parce(href, headers)
                href_n += 1
                files_writer(flats)
            except:
                print('Данные по квартире не получены, меняем IP')
                change_IP()
                checkIP()
    else:
        print("ERROR flats")


def main():
    f = open('links_of_54_pages.dat', 'rb')
    dict_ = pickle.load(f)
    num_p = 0
    for base_url in dict_:
        num_p += 1
        a = dict_[base_url]
        print("Страница поиска -", num_p, end='\n ')
        cian_parce_flats(a, headers)


main()
