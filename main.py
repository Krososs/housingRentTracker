import logging
import os

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from Scrapper import Scrapper
from AnnouncementService import AnnouncementService

app = Flask(__name__)

scheduler = BackgroundScheduler(daemon=False)
scheduler.add_job(func=Scrapper.collect_data, trigger='interval', hours=24)
scheduler.start()

@app.route('/', methods=['GET'])
def hello():
    return "Hello world"

@app.route('/test', methods=['POST'])
def test():
    return request.get_json()

@app.route('/announcements', methods=['POST'])
def get_announcements():
    return AnnouncementService.get_announcements(request.get_json())

if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run()
