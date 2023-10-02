import logging
import os
import datetime

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from Scrapper import Scrapper
from pymongo import MongoClient
from AnnouncementService import AnnouncementService

app = Flask(__name__)
# def scheduler_test():
#     client = MongoClient(os.environ['MONGODB_URI'])
#     record = {
#         "Test": "HerokuTest"
#     }
#     client.HousingRent.Test.insert_one(record)

# scheduler = BackgroundScheduler(daemon=True)
# #scheduler.add_job(func=scheduler_test, trigger='interval', minutes=2)
# scheduler.start()

@app.route('/', methods=['GET'])
def hello():
    return "Hello world"

@app.route('/test', methods=['POST'])
def test():
    Scrapper.collect_data()
    return request.get_json()

@app.route('/announcements', methods=['POST'])
def get_announcements():
    return AnnouncementService.get_announcements(request.get_json())

if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run()
