import unittest
import mock
from unittest.mock import MagicMock
import flask_testing
from flask import Flask
from flask_testing import TestCase
import os
from models import User, Event, Bet, db
from faker import Faker
from app import app
from tasks import run_tasks, get_event_result


class ScheduledTests(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI"
        )

        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):

        db.session.remove()
        db.drop_all()

    def mock_get_event_result(self, _):
        return {
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

    def test_transaction(self):

        user = User(
            first_name="Tristan",
            last_name="Test",
            email="fake@gmail.com",
            hashed_password="*test*",
        )
        db.session.add(user)
        db.session.commit()

        assert user in db.session

    @mock.patch("tasks.get_event_result", side_effect=mock_get_event_result)
    def test_run_tasks(self, _):
        """Ensure database is updated correctly by scheduled task (stubbing API call to sportsdb.com)"""

        faker = Faker()

        db.session.add(
            User(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                hashed_password="*FAKE*",
            )
        )
        db.session.add_all(
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

        db.session.commit()

        db.session.add_all(
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
        run_tasks(db, os.environ.get("API_KEY"))

        db.session.commit()


if __name__ == "__main__":
    unittest.main()
