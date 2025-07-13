import logging
import threading
import sys

from flask import Flask, request
from apscheduler.schedulers.background import BackgroundScheduler
from Scrapper import Scrapper
from AnnouncementService import AnnouncementService
from Utils.Database import Database

logging.basicConfig(
    level=logging.INFO
)

scheduler = BackgroundScheduler(daemon=True)


def run_scheduler():
    scheduler.add_job(func=Database.inset_test_record, trigger='interval', minutes=1)
    scheduler.start()

def on_run():
    logging.info("APP STARTING")
    if not Database.connected():
        logging.info("APP CLOSING ON ERROR")
        sys.exit(1)
    Database.prepare_collections()
    run_scheduler()

class FlaskApp(Flask):
  def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
    if not self.debug:
      with self.app_context():
        on_run()
    super(FlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = FlaskApp(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello world"

@app.route('/test', methods=['POST'])
def test():
    thread = threading.Thread(target=Scrapper.collect_data, daemon=True)
    # Scrapper.collect_data()
    thread.start()
    return request.get_json()

@app.route('/announcements', methods=['POST'])
def get_announcements():
    return AnnouncementService.get_announcements(request.get_json())

if __name__ == '__main__':
    app.run()

