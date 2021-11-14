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

from helpers import convert_to_named_tuple

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    current_user,
    login_required,
    logout_user,
)

import os
import json
from datetime import date, datetime, timedelta
from models import (
    db,
    connect_db,
    Bet,
    Event,
    bcrypt,
    User,
    UserBalance,
    LoginManager,
    UserMixin,
    login_manager,
)
from forms import RegistrationForm, LoginForm, DeleteUser, ChangePasswordForm
from models import User
from flask_socketio import SocketIO, emit, disconnect
from variables import clients
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from flask_apscheduler import APScheduler

import logging

logging.getLogger("apscheduler").setLevel(logging.DEBUG)

login_manager = LoginManager()
login_manager.login_view = "login"

# app = Flask(__name__, instance_path='/Volumes/GoogleDrive/My Drive/Classes/SoftwareDevelopmentPracticum/better-bets/instance')
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", os.environ.get("SQLALCHEMY_DATABASE_URI")
)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["FLASK_ENV"] = os.environ.get("FLASK_ENV", "development")
app.config["API_KEY"] = os.environ.get("API_KEY")
# For David's local env:  app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:heize_stan@localhost/postgres'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "my secret"
app.config["API_KEY"] = "40130162"
app.debug = True
login_manager.init_app(app)

logging.basicConfig()
logging.getLogger("apscheduler").setLevel(logging.DEBUG)

# liao's environment: no if
# if app.config["FLASK_ENV"] == "development":
from tasks import run_tasks, update_reload_balance

sched = APScheduler()
sched.init_app(app)
sched.start()

@sched.task("interval", id="main-job", seconds=120)
def timed_job():
    with app.app_context():
        run_tasks(db, app.config["API_KEY"])
    now = datetime.now()
    print(f'Running scheduled task at {now.strftime("%H:%M:%S")}')

@sched.task("interval", id="balance-update", days=7)
def balance_update_job():
    with app.app_context():
        update_reload_balance(db)


connect_db(app)


def stop():
    sched.shutdown()


@login_manager.user_loader
def load_user(userid):
    user_id = int(userid)
    return User.query.get(user_id)


@app.route("/")
def render_home_page():
    """Render home page with 10 upcoming events"""

    events = Event.query.filter(Event.date >= date.today()).limit(10)

    # if logged in, show user their 10 most recent bets
    last_30_days = datetime.today() - timedelta(days=30)
    bets = (
        None
        if current_user.is_authenticated is False
        else Bet.query.filter(
            Bet.event_date >= last_30_days, Bet.user_id == current_user.id
        ).limit(10)
    )
    if bets:
        bets_events = []
        for bet in bets:
            bets_events.append(
                {
                    "event": (Event.query.filter(Event.id == bet.event)).first(),
                    "bet": bet,
                }
            )

    else:
        bets_events = None

    return render_template("home.html", events=events, bets_events=bets_events)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            hashed_password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(
            f"Account created for {form.email.data}! 🙌🏼 You can now log in.", "success"
        )

        # create UserBalance record in DB
        res = db.session.execute(
            "SELECT * from users WHERE id = (SELECT max(id) FROM users)"
        )
        new_id = None
        for r in res:
            user_id = r[0]
        user_balance = UserBalance(user_id=user_id)

        db.session.add(user_balance)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
            user.hashed_password, form.password.data
        ):
            login_user(
                user, remember=False
            )  # by default, the user is logged out if browser is closed
            flash(f"Hi {user.first_name}! You are logged in.")
            return redirect(url_for("render_home_page"))
        else:
            flash(f"Login Unsuccessful. Please check email and password")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've logged out")
    return redirect(url_for("render_home_page"))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    user_balance = convert_to_named_tuple(
        db.session.execute(
            "SELECT balance FROM user_balance WHERE user_id = :user_id",
            {"user_id": current_user.id},
        )
    )[0].balance
    # if user clicks on the Delete Account button:
    form = DeleteUser()
    if form.validate_on_submit():
        email = current_user.email
        # delete user_balance row, then delete user from user table
        db.session.execute(
            "DELETE FROM user_balance WHERE user_id = :user_id",
            {"user_id": current_user.id},
        )
        db.session.delete(current_user)
        db.session.commit()
        flash(f'Account deleted for {email}')
        return redirect(url_for('render_home_page'))
    return render_template("account.html", title="Account", user_balance=user_balance, form=form)


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.hashed_password, form.old_password.data):
            db.session.execute(
                "UPDATE users SET hashed_password = 'new_hashed_password' WHERE user_id = :user_id",
            {"user_id": current_user.id},
        )
            flash(f'Password successfully changed')
            return redirect(url_for('account'))
        else:
            flash(f'Password change unsuccessful. Please check your password and try again.')
    return render_template('change-password.html', title='Change Password', form=form)
# todo create change-password.html template


@app.route("/search")
def search():
    """For use with JS event listener to filter events on home page"""
    search = request.args["q"]
    last_30_days = datetime.today() - timedelta(days=30)
    month_forward = datetime.today() + timedelta(days=30)

    search_result = (
        Event.query.filter(
            Event.title.ilike(f"%{search}%"),
            Event.date >= datetime.today(),
            Event.date <= month_forward,
        )
        .limit(10)
        .all()
    )

    s = [
        {
            "title": s.title,
            "date": str(s.date),
            "id": s.id,
            "home_team": s.home_team,
            "away_team": s.away_team,
        }
        for s in search_result
    ]
    return json.dumps(s)


@app.route("/event/<id>")
def render_event(id):
    event = Event.query.get(id)

    # redirect to home if event does not exist
    if event is None:
        return redirect("/")

    if event is not None and current_user.is_authenticated:
        bet = Bet.query.filter(
            Bet.event == event.id, Bet.user_id == current_user.id
        ).first()
    else:
        bet = None
    bet_on = False if bet == None else True
    result = event.winner

    # get 5 most recent bets on event

    if len(event.bets) > 0:
        bets = event.bets[-5:]
    else:
        bets = None

    return render_template(
        "event.html", event=event, bet_on=bet_on, bet=bet, bets=bets, result=result
    )


# @app.route("/account")
# def render_account():
#     return render_template('account.html')


# API endpoints called from JS event listener to make bet


@app.route("/api/bet", methods=["POST"])
@login_required
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
            event_date=event.date,
            selection=selection,
            amount=int(amount),
            user_id=current_user.id,
        )
    )

    # get current user balance, then update it
    user_balance = convert_to_named_tuple(
        db.session.execute(
            "SELECT balance FROM user_balance WHERE user_id = :user_id",
            {"user_id": current_user.id},
        )
    )[0].balance

    new_balance = user_balance - int(amount)
    # prevent any bet that brings user balance below 0
    if new_balance < 0:
        return json.dumps(
            {"text": f"Your balance of {user_balance} is too low for this bet."}
        )
    else:
        db.session.execute(
            "UPDATE user_balance SET balance = :new_balance WHERE user_id = :id",
            {"new_balance": new_balance, "id": current_user.id},
        )
        db.session.commit()
        return json.dumps(
            {"text": f"You bet on {selection}. New balance is {new_balance}"}
        )


@app.route("/api/bet", methods=["PATCH"])
def update_bet():
    """Receives JSON posted from scheduled task with 1) event ID 2) resolution to bet and then updates database"""
    json_data = json.loads(request.data)
    event = Event.query.get(json_data["eventId"])


@app.route("/api/bet", methods=["DELETE"])
def delete_bet():
    """Receives JSON posted from JS event listener with event ID user is deleting and updates database"""
    json_data = json.loads(request.data)
    print("pause")
    return json.dumps({"text": f"You bet on {json_data['selection']}"})


@app.route("/balance/<id>")
def reload_balance(id):
    """Reloads balance if user is eligible"""
    user_record = convert_to_named_tuple(
        db.session.execute(
            "SELECT can_refill_balance FROM users WHERE id = :id", {"id": id}
        )
    )
    if user_record[0].can_refill_balance:
        db.session.execute(
            "UPDATE user_balance SET balance = (balance + 500) WHERE user_id = :id",
            {"id": id},
        )
        db.session.execute(
            "UPDATE users SET can_refill_balance = FALSE WHERE id=:id", {"id": id}
        )
        db.session.commit()
        balance_record = convert_to_named_tuple(
            db.session.execute(
                "SELECT balance FROM user_balance WHERE user_id = :id", {"id": id}
            )
        )
        return json.dumps({"balance": balance_record[0].balance, "eligible": True})
    else:
        return json.dumps({"eligible": False})


# Route for use testing scheduling functionality


# @app.route("/test_scheduler", methods=["GET"])
# def render_schedule():
#     """Renders template with button that calls JS to test scheduling functionality"""
#     return render_template("test_scheduler.html")


# @app.route("/start", methods=["POST"])
# def schedule_start():
#     """Runs scheduler"""
#     start()
#     return json.dumps({"result": "started"})


# @app.route("/stop", methods=["POST"])
# def schedule_stop():
#     """Stops scheduler"""
#     stop()
#     return json.dumps({"result": "stopped"})
