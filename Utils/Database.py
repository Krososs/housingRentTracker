from pymongo import MongoClient
import os

client = MongoClient('localhost', 27017)
clientOnline = MongoClient(os.environ['MONGODB_URI'])


class Database:
    # Online DB
    @staticmethod
    def test_connection():
        db = clientOnline.test

    @staticmethod
    def create_database():
        db = clientOnline["HousingRent"].create_collection("Offers")

    @staticmethod
    def database_exist():
        return "HousingRent" in clientOnline.list_database_names()

    @staticmethod
    def insert_new_record(record):
        # client.HousingRent.Offers.insert_one(record)
        clientOnline.HousingRent.Offers.insert_one(record)

    @staticmethod
    def insert_scraping_stats(stats):
        clientOnline.HousingRent.Stats.insert_one(stats)

    @staticmethod
    def get_announcements(test=False):
        if test:
            return client.HousingRent.Test
        else:
            return clientOnline.HousingRent.Offers
