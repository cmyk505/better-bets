from flask import Flask, request, session, render_template
from dotenv import load_dotenv
import datetime
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from app import app, socket_
from tasks import run_tasks
from variables import clients


logging.basicConfig()
logging.getLogger("apscheduler").setLevel(logging.DEBUG)

sched = BlockingScheduler()


# @sched.scheduled_job("interval", minutes=1)
# def timed_job():
#     with app.app_context():
#         run_tasks()
#     return "tried to do something"


def start():
    """"""

    @sched.scheduled_job("interval", seconds=3)
    def timed_job():
        with app.app_context():
            run_tasks()
        return "tried to do something"

    sched.start()


def stop():
    sched.shutdown()
