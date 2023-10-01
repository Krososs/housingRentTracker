from pymongo import MongoClient
import os

client = MongoClient(os.environ['MONGODB_URI'])


class Database:
    @staticmethod
    def test_connection():
        db = client.test

    @staticmethod
    def create_database():
        db = client["HousingRent"].create_collection("Offers")

    @staticmethod
    def database_exist():
        return "HousingRent" in client.list_database_names()

    @staticmethod
    def insert_new_record(record):
        client.HousingRent.Offers.insert_one(record)

    @staticmethod
    def insert_scraping_stats(stats):
        client.HousingRent.Stats.insert_one(stats)

    @staticmethod
    def get_announcements():
        return client.HousingRent.Offers
