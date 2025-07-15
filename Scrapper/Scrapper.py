from bs4 import BeautifulSoup
import requests
import time
import datetime
from Utils.Database import Database

from flask import current_app

def get_url(city):
    return 'https://ogloszenia.trojmiasto.pl/nieruchomosci-mam-do-wynajecia/' + city + '/?strona='

def trojmiasto_pl_collect_data():
    cities = current_app.config['TROJMIASTO_PL'].get("cities")
    start = datetime.datetime.now()
    record = {
        'Date': datetime.datetime.now().strftime('%Y-%m-%d')
    }
    for city in cities:
        city_data = trojmiasto_pl_collect_data_for_city( city)
        record[city] = city_data
        time.sleep(10.0)

    stop = datetime.datetime.now()
    stats = {
        'Date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'Time_difference': divmod((stop - start).seconds, 60)
    }
    Database.insert_new_record(record)
    Database.insert_scraping_stats(stats)

def trojmiasto_pl_collect_data_for_city(city):
    next_page = True
    city_data = None
    page = 0
    url = get_url(city)
    announcements = []

    while next_page:
        content = requests.get(url + str(page)).content
        soup = BeautifulSoup(content, 'html.parser')
        list = soup.find_all('div', {'class': 'list__item__wrap__content'})
        sub_offers_count = 0
        for data in list:
            time.sleep(0.1)
            sub_offers_count += 1
            try:
                price = int(
                    data.find_next('p', {'class': 'list__item__price__value'}).text.replace('zł', '').replace(' ', ''))
            except:
                price = None

            try:
                surface = int(float(data.find_next('li', {
                    'class': 'list__item__details__icons__element details--icons--element--powierzchnia'}). \
                                    find('p', {'class': 'list__item__details__icons__element__desc'}).text.strip().replace('m2', '').strip()))
            except:
                surface = None
            try:
                rooms_data = data.find_next('li',
                                   {'class': 'list__item__details__icons__element details--icons--element--l_pokoi'}). \
                        find('p', {'class': 'list__item__details__icons__element__desc'}).text.strip()
                rooms = int(''.join([c for c in rooms_data if c.isdigit()]))
            except:
                rooms = None
            offer = {
                'Price': price,
                'Surface': surface,
                'Rooms': rooms
            }
            announcements.append(offer)
        navbar = soup.find('div', {'class': 'pages__wrap'})

        if not navbar or sub_offers_count == 0:
            next_page = False
            city_data = {
                'Number_of_announcements': len(announcements),
                'Announcements': announcements
            }
        page += 1
    return city_data
