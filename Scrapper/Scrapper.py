from bs4 import BeautifulSoup
import requests
import time
import datetime
from Utils.Database import Database


def get_url(city):
    return 'https://ogloszenia.trojmiasto.pl/nieruchomosci-mam-do-wynajecia/' + city + '/?strona='

def collect_data():
    start = datetime.datetime.now()
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    city_gdansk = collect_data_for_city('gdansk')
    time.sleep(10.0)
    city_gdynia = collect_data_for_city('gdynia')
    time.sleep(10.0)
    city_sopot = collect_data_for_city('sopot')
    record = {
        'Date': today,
        'Gdansk': city_gdansk,
        'Gdynia': city_gdynia,
        'Sopot': city_sopot
    }
    stop = datetime.datetime.now()
    stats = {
        'Date': today,
        'Time_difference': divmod((stop - start).seconds, 60)
    }
    Database.insert_new_record(record)
    Database.insert_scraping_stats(stats)


def get_number_of_announcements(soup):
    announcements = soup.find('div', {'class': 'form-heading__desc'}).find('span')
    return int(announcements.text.replace('(', '').replace(')', ''))


def collect_data_for_city(city):
    page = 0
    next_page = True
    url = get_url(city)
    announcements = []
    city_data = None
    while next_page:
        content = requests.get(url + str(page)).content
        soup = BeautifulSoup(content, 'html.parser')
        list = soup.find_all('div', {'class': 'list__item__wrap__content'})

        sub_offers_count = 0
        for data in list:
            time.sleep(0.4)
            sub_offers_count += 1
            try:
                price = int(
                    data.find_next('p', {'class': 'list__item__price__value'}).text.replace('zł', '').replace(' ', ''))
            except:
                price = None

            try:
                surface = int(float(data.find_next('li', {
                    'class': 'list__item__details__icons__element details--icons--element--powierzchnia'}). \
                                    find('p', {'class': 'list__item__details__icons__element__desc'}).text.strip()))
            except:
                surface = None
            try:
                rooms = int(float(
                    data.find_next('li',
                                   {'class': 'list__item__details__icons__element details--icons--element--l_pokoi'}). \
                        find('p', {'class': 'list__item__details__icons__element__desc'}).text.strip()))
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
            number_of_announcements = get_number_of_announcements(soup)
            next_page = False
            city_data = {
                'Number_of_announcements': number_of_announcements,
                'Announcements': announcements
            }
        page += 1
    return city_data
