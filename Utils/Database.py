from pymongo import MongoClient
import os
import logging
import datetime

from pymongo.errors import ConnectionFailure

client = MongoClient(os.environ['MONGODB_URI'])

class Database:
    @staticmethod
    def connected():
        try:
            client.admin.command("ping")
            return True
        except ConnectionFailure as e:
            logging.critical(f"Connection error: {e}")
            return False

    @staticmethod
    def prepare_collections():
        if not "HousingRent" in client.list_database_names():
            client["HousingRent"].create_collection("Offers")

    @staticmethod
    def inset_test_record():
        record = {
            "Test": "InsertTest",
            "Timestamp": datetime.datetime.now().isoformat()
        }
        client.HousingRent.Offers.insert_one(record)

    @staticmethod
    def insert_new_record(record):
        client.HousingRent.Offers.insert_one(record)

    @staticmethod
    def insert_scraping_stats(stats):
        client.HousingRent.Stats.insert_one(stats)

    @staticmethod
    def get_announcements():
        return client.HousingRent.Offers
