import os
from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from Scrapper import Scrapper
from Utils.Database import Database
from AnnouncementService import AnnouncementService


def init():
    if not Database.database_exist():
        Database.create_database()
    Database.test_connection()


def collect_data():
    Scrapper.collect_data()


app = Flask(__name__)

# init()
# collect_data()
scheduler = BackgroundScheduler(daemon=True)

scheduler.add_job(id='collect_data', func=collect_data, trigger='interval', hours=24)
scheduler.start()
scheduler.print_jobs()


@app.route('/', methods=['GET'])
def hello_world():
    data = request.get_json()
    return AnnouncementService.get_announcements(data, False)


if __name__ == '__main__':
    app.run(debug=True)
