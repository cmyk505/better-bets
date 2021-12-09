import flask_testing
from flask import Flask
import os
from models import User, Event, Bet, db
from app import app, render_home_page
from datetime import date, datetime, timedelta
import pytest


def test_search(test_client, session):
    """Ensure valid search gets response from database"""
    today = date.today()
    session.execute(
        "INSERT INTO EVENT (title, date, sportsdb_id, sportsdb_status, home_team, away_team, resolved) VALUES ('lakers v spurs', :today, 1234, 'AOT', 'lakers', 'spurs', 'False')",
        {"today": today},
    )
    session.commit()
    res = test_client.get("/search?q=lakers&completed=f")
    assert res.status_code == 200
    assert b'"title": "lakers v spurs"' in res.data


def test_invalid_search(test_client, session):
    """Invalid search result does not get 200"""
    with pytest.raises(Exception):
        res = test_client.get("/search?q=lakers")