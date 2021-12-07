import unittest
from pytest_mock import mocker
from unittest.mock import MagicMock
import mock
import flask_testing
from flask import Flask
from flask_testing import TestCase
import os
from models import User, Event, Bet, db
from faker import Faker
from app import app
from tasks import run_tasks, get_event_result

mock_event_results = {
    "idEvent": 1,
    "strEvent": "something",
    "strHomeTeam": "Atlanta Hawks",
    "strAwayTeam": "Houston Rockets",
    "intHomeScore": 100,
    "intAwayScore": 100,
    "strTimestamp": "",
    "strStatus": "OT",
    "dateEvent": 12 / 2 / 1993,
    "winner": "Atlanta Hawks",
}


def test_transaction(session):

    user = User(
        first_name="Tristan",
        last_name="Test",
        email="fake@gmail.com",
        hashed_password="*test*",
    )
    session.add(user)
    session.commit()

    assert user in session


# @mock.patch("tasks.get_event_result")
def test_run_tasks(session):
    """Ensure database is updated correctly by scheduled task (stubbing API call to sportsdb.com)"""

    faker = Faker()

    session.add(
        User(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=faker.email(),
            hashed_password="*FAKE*",
        )
    )
    session.add_all(
        [
            Event(
                sportsdb_id=1,
                sportsdb_status="",
                title=faker.text(100),
                home_team=faker.text(10),
                away_team=faker.text(10),
                resolved=False,
                date=faker.date_this_month(before_today=False, after_today=True),
            ),
            Event(
                sportsdb_id=faker.unique.random_int(),
                sportsdb_status="",
                title=faker.text(100),
                home_team=faker.text(10),
                resolved=True,
                away_team=faker.text(10),
                date=faker.date_this_month(before_today=False, after_today=True),
            ),
            Event(
                sportsdb_id=faker.unique.random_int(),
                sportsdb_status="",
                title=faker.text(100),
                home_team=faker.text(10),
                resolved=True,
                away_team=faker.text(10),
                date=faker.date_this_month(before_today=False, after_today=True),
            ),
        ]
    )

    session.commit()

    session.add_all(
        [
            Bet(
                user_id=1,
                event=1,
                event_date=faker.date_this_month(),
                selection="something",
                amount=100,
            ),
            Bet(
                user_id=1,
                event=1,
                event_date=faker.date_this_month(),
                selection="something",
                amount=100,
            ),
            Bet(
                user_id=1,
                event=1,
                event_date=faker.date_this_month(),
                selection="something",
                amount=100,
            ),
        ],
    )

    # mock the API call made in run_tasks to avoid testing the API
    with mock.patch("tasks.get_event_result") as mock_get_event_result:
        mock_get_event_result.return_value = mock_event_results
        run_tasks(db, os.environ.get("API_KEY"))

    event = Event.query.filter(Event.id == 1)
    event_updated = True if event[0].resolved == True else False
    session.commit()
