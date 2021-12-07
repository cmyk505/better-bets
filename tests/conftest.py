import pytest
from flask import template_rendered
from flask_sqlalchemy import SQLAlchemy
import app
import os
from sqlalchemy import event
from models import db as _db, User, connect_db

# code for fixtures based on https://stackoverflow.com/questions/52233896/database-for-pytest-flask-application-does-not-work-correctly


@pytest.fixture(scope="session")
def test_client(request):
    flask_app = app.app

    testing_client = flask_app.test_client()

    # create an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return testing_client


@pytest.fixture(scope="session")
def test_db(test_client, request):
    # Create the database and the database table
    def teardown():
        _db.drop_all()

    _db.app = app
    _db.create_all()

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="session")
def session(test_db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = test_db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = test_db.create_scoped_session(options=options)

    test_db.session = session

    def teardown():
        session.close()
        # rollback - everything that happened with the
        # session above (including calls to commit())
        # is rolled back.
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session