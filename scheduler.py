from flask import Flask, request, session, render_template
from dotenv import load_dotenv
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from app import app

from tasks import run_tasks


logging.basicConfig()
logging.getLogger("apscheduler").setLevel(logging.DEBUG)

sched = BlockingScheduler()


def start():
    """"""

    @sched.scheduled_job("interval", minutes=1)
    def timed_job():
        with app.app_context():
            run_tasks()
        now = datetime.now()
        print(f'Running scheduled task at {now.strftime("%H:%M:%S")}')

    sched.start()


def stop():
    sched.shutdown()
