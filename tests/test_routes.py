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
from app import app, render_home_page
from forms import RegistrationForm, LoginForm
from models import User


def test_render_home_page(session, test_client):
    """Validates 200 for home page"""
    response = test_client.get("/")
    assert response.status_code == 200


def test_registration_get(session, test_client):
    """Validates 200 for /register get request"""
    response = test_client.get("/register")
    assert response.status_code == 200


def test_registration_post(session, test_client, faker):
    """Tests posting form to /register route"""
    app.config["WTF_CSRF_ENABLED"] = False
    form = RegistrationForm(formdata=None)
    form.data["first_name"] = faker.first_name
    form.data["last_name"] = faker.last_name
    form.data["email"] = faker.email
    form.data["hashed_password"] = "I_AM_FAKE$$!"
    response = test_client.post("/register", data=form.data)
    assert response.status_code == 200
    added_user = session.execute(
        "SELECT user FROM users WHERE email = :email", {"email": form.data["email"]}
    )
    assert added_user


def test_account_logged_out(test_client):
    """Confirm user is redirected if they try to access /account while logged out"""
    res = test_client.get("/account")
    assert res.status_code == 302


def test_logout_redirect(test_client):
    """Confirm user is redirected if they try to access /logout while already logged out"""
    res = test_client.get("/logout")
    assert res.status_code == 302


def test_successful_login(session, test_client, faker):
    """Tests /login route with info that should succeed"""

    app.config["WTF_CSRF_ENABLED"] = False

    # first create user in DB
    email = faker.email()
    session.add(
        User(
            first_name=faker.first_name(),
            last_name=faker.last_name(),
            email=email,
            hashed_password="*FAKE*",
        )
    )
    session.commit()

    form = LoginForm()

    form.data["email"] = email
    form.data["password"] = "*FAKE*"
    form.data["hashed_password"] = "*FAKE*"

    response = test_client.post("/login", data=form.data)

    assert response.status_code == 200