from flask import Flask, request, redirect, render_template, url_for, flash, jsonify, session

import os
import json
from datetime import date
from models import db, connect_db, Bet, Event
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:heize_stan@localhost/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "my secret"
app.debug = True

connect_db(app)


@app.route("/")
def render_home_page():
    """Render home page with 10 upcoming events"""

    events = Event.query.filter(Event.date >= date.today()).limit(10)

    return render_template("home.html", events=events)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

@app.route("/event/<id>")
def render_event(id):
    return render_template("event.html", id=id)


# @app.route("/account")
# def render_account():
#     return render_template('account.html')


# API endpoints called from JS event listener to make bet


@app.route("/api/bet", methods=["POST"])
def place_bet():
    """Receives JSON posted from JS event listener with 1) event ID user is betting on 2) user's bet. We can retrieve current user ID from Flask session"""
    json_data = json.loads(request.data)
    print("pause")
    return json.dumps({"text": f"You bet on {json_data['selection']}"})

if __name__ == '__main__':
    app.run(debug=True)