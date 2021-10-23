from flask import (
    Flask,
    request,
    redirect,
    render_template,
    url_for,
    flash,
    jsonify,
    session,
)
import os
import json
from datetime import date
from models import db, connect_db, Bet, Event

app = Flask(__name__)
app.config["FLASK_ENV"] = os.environ.get("FLASK_ENV")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "my secret"

connect_db(app)


@app.route("/")
def render_home_page():
    """Render home page with 10 upcoming events"""

    events = Event.query.filter(Event.date >= date.today()).limit(10)

    return render_template("home.html", events=events)


@app.route("/event/<id>")
def render_event(id):
    event = Event.query.get(id)
    if event is not None:
        bet = Bet.query.filter(
            Bet.event == event.id, Bet.user_id == session.get("user_id", 1)
        ).first()
    else:
        return redirect("/")
    # redirect to home if event does not exist
    bet_on = False if bet == None else True
    result = event.winner
    return render_template(
        "event.html", event=event, bet_on=bet_on, bet=bet, result=result
    )


# @app.route("/account")
# def render_account():
#     return render_template('account.html')


# API endpoints called from JS event listener to make bet


@app.route("/api/bet", methods=["POST"])
def place_bet():
    """Receives JSON posted from JS event listener with 1) event ID user is betting on 2) user's bet. We can retrieve current user ID from Flask session to update database"""
    # TODO these routes should be protected/have validation
    json_data = json.loads(request.data)
    # get the selection + event ID + amt the user bet
    selection = json_data["selection"]
    amount = json_data["betAmt"]
    event = Event.query.get(json_data["eventId"])

    # add Bet record in database
    db.session.add(
        Bet(
            event=event.id,
            selection=selection,
            amount=int(amount),
            user_id=session.get("logged_in_user", 1),
        )
    )
    db.session.commit()
    return json.dumps({"text": f"You bet on {selection}"})


@app.route("/api/bet", methods=["PATCH"])
def update_bet():
    """Receives JSON posted from JS event listener with 1) event ID user is updating 2) user's update and then updates database"""
    json_data = json.loads(request.data)
    event = Event.query.get(json_data["eventId"])


@app.route("/api/bet", methods=["DELETE"])
def delete_bet():
    """Receives JSON posted from JS event listener with event ID user is deleting and updates database"""
    json_data = json.loads(request.data)
    print("pause")
    return json.dumps({"text": f"You bet on {json_data['selection']}"})
