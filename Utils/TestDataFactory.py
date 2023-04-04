import random
import datetime
import time

from pymongo import MongoClient
from Utils.Database import Database

client = MongoClient('localhost', 27017)


class TestData:
    @staticmethod
    def create_test_offer():
        return {
            'Price': random.randint(1500, 3000),
            'Surface': random.randint(25, 65),
            'Rooms': random.randint(1, 5)
        }

    @staticmethod
    def create_test_city_data():
        i = 0
        announcements = []
        while i < 5:
            announcements.append(TestData.create_test_offer())
            i += 1
        return {
            'Number_of_announcements': len(announcements),
            'Announcements': announcements
        }

    @staticmethod
    def create_test_record():
        start = datetime.datetime.now()
        city_gdansk = TestData.create_test_city_data()
        city_gdynia = TestData.create_test_city_data()
        city_sopot = TestData.create_test_city_data()
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        time.sleep(10)
        record = {
            'Date': today,
            'Gdansk': city_gdansk,
            'Gdynia': city_gdynia,
            'Sopot': city_sopot
        }
        stop = datetime.datetime.now()
        stats = {
            'Date': today,
            'Time_difference': (stop - start).seconds
        }
        Database.insert_scraping_stats(stats)
        return record

    @staticmethod
    def create_test_data(iterator):
        while iterator > 0:
            client.HousingRent.Test.insert_one(TestData.create_test_record())
            iterator -= 1
