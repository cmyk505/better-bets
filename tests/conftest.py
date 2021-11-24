import pytest
from flask_sqlalchemy import SQLAlchemy
import app
import os
from sqlalchemy import event
from models import db as _db, User, connect_db


# @pytest.fixture(scope="session")
# def test_client():
#     flask_app = app.app
#     testing_client = flask_app.test_client()
#     ctx = flask_app.app_context()
#     ctx.push()
#     yield testing_client
#     ctx.pop()


# @pytest.fixture(scope="session")
# def db(test_client):
#     db = SQLAlchemy(app=test_client.application)
#     print("pause")
#     return db


# @pytest.fixture(scope="session")
# def session(db):
#     db.session.begin_nested()
#     db.drop_all()
#     db.create_all()
#     yield db.session
#     db.session.close()
#     db.session.rollback()


@pytest.fixture(scope="session")
def test_client(request):
    flask_app = app.app

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.

    testing_client = flask_app.test_client()

    # Establish an application context before running the tests.
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
    print("pause")
    # user = User(username='admin', )
    # _db.session.add(user)
    # _db.session.commit()
    # # Commit the changes for the users

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope="session")
def session(test_db, request):
    """Creates a new database session for a test."""
    # connect to the database
    connection = test_db.engine.connect()
    # begin a non-ORM transaction
    transaction = connection.begin()

    # bind an individual session to the connection
    options = dict(bind=connection, binds={})
    session = test_db.create_scoped_session(options=options)

    # overload the default session with the session above
    test_db.session = session

    def teardown():
        session.close()
        # rollback - everything that happened with the
        # session above (including calls to commit())
        # is rolled back.
        transaction.rollback()
        # return connection to the Engine
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session