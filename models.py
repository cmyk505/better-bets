import requests, json
from datetime import datetime
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from faker import Faker
from flask_login import LoginManager, UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import update
from datetime import datetime
import pytz


# fmt: off

# using bcrypt for password hashing
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def connect_db(app):
    """Attach db to Flask app"""
    db.app = app
    db.init_app(app)
    # if app.config["FLASK_ENV"] == "development":
    #     User.query.delete()
    # Event.query.delete()
    # db.drop_all()
    # db.create_all()
    # seed_database(app, db)

def seed_database(app, db):
    def get_all_NBA_events_current_season():
        """Calls out to datadb API for all NBA events for the current season"""
        current_season_str = (
            str(datetime.now().year) + "-" + str(datetime.now().year + 1)
        )
        res = requests.get(
            f"https://www.thesportsdb.com/api/v1/json/{app.config['API_KEY']}/eventsseason.php?id=4387&s={current_season_str}"
        )

        return res.json()

# NOTE: pytz.reference.LocalTimezone() would produce wrong result here

## You could use `tzlocal` module to get local timezone on Unix and Win32
# from tzlocal import get_localzone # $ pip install tzlocal

# # get local timezone    
# local_tz = get_localzone()
    def utc_to_local(utc_dt):
        """Convert UTC/GMT to pacific time"""
        local_tz = pytz.timezone('US/Pacific') # use your local timezone name here
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        return f'{local_dt.year}-{local_dt.month}-{local_dt.day}'

    def utc_to_local_datetime(utc_dt):
        """Convert UTC/GMT to pacific time including time"""
        local_tz = pytz.timezone('US/Pacific') # use your local timezone name here
        local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
        minutes = local_dt.minute
        if minutes == '0' or minutes==0:
            minutes = '00'
        return f'{local_dt.year}-{local_dt.month}-{local_dt.day} {local_dt.hour}:{minutes}:00'

    def add_api_results_to_db():
        """Add all new NBA events from API into database"""
        res = get_all_NBA_events_current_season()
        new_events = []
        for r in res["events"]:
            new_events.append(
                Event(
                    sportsdb_id=r["idEvent"],
                    title=r["strEvent"],
                    home_team=r["strHomeTeam"],
                    away_team=r["strAwayTeam"],
                    home_score=r["intHomeScore"],
                    away_score=r["intAwayScore"],
                    datetime=utc_to_local_datetime(datetime.strptime(r["strTimestamp"][:len(r["strTimestamp"])-6], '%Y-%m-%dT%H:%M:%S')),
                    date=utc_to_local(datetime.strptime(r["dateEvent"], '%Y-%m-%d')),
                    sportsdb_status=r["strStatus"],
                    strThumb=r["strThumb"],
                )
            )
        return new_events

    db.session.add_all(add_api_results_to_db())
    db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
class User(db.Model, UserMixin):
    """User table columns in the database"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(200), nullable=False, unique=True)
    hashed_password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    can_refill_balance = db.Column(db.Boolean, default=False)
    image_file = db.Column(
        db.String(50), nullable=False, default="defaultProfilePic.jpg"
    )

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.image_file}')"

    @classmethod
    def register(cls, password, email):
        """Hash the provided password upon user registration, pass that into the db"""
        hashed_password = bcrypt.generate_password_hash(password)
        hashed_password_utf8 = hashed_password.decode("utf8")
        return cls(hashed_password=hashed_password_utf8, email=email)

    @classmethod
    def authenticate(cls, email, password):
        """Authentication: check if email and password hash matches db record"""
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False

    @classmethod
    def change_password(cls, id, current_password, new_password):
        """Change password for an existing user
        Return false if current password passed into function is incorrect. Otherwise
        return the user
        """

        user = cls.query.filter_by(id=id).first()
        if user:
            correct_password = bcrypt.check_password_hash(
                user.password, current_password
            )
            if correct_password:
                return user

        return False


class UserFollow(db.Model):
    """User follow model not implemented in final product"""
    __tablename__ = "user_follow"
    id = db.Column(db.Integer, unique=True)
    follower_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, primary_key=True
    )
    followed_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, primary_key=True
    )


class Event(db.Model):
    """Columns for the event table in db"""
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sportsdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    home_team = db.Column(db.String(50), nullable=False)
    away_team = db.Column(db.String(50), nullable=False)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    sportsdb_status = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    resolved = db.Column(db.Boolean, default=False)
    winner = db.Column(db.String(50),default="Undecided")
    strThumb = db.Column(db.String(500))
    bets = db.relationship("Bet", backref="event_ref")
    # fmt: on

class UserBalance(db.Model):
    """User balance table columns"""
    __tablename__ = "user_balance"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=500)


class Bet(db.Model):
    """Bet table columns"""
    __tablename__ = "bet"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    selection = db.Column(db.String(100), nullable=False)
    final_margin = db.Column(db.Integer, default=0)
    amount = db.Column(db.Integer, nullable=False)


class Comment(db.Model):
    """Comment table columns"""
    __tablename__ = "comment"
    commenter = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    id = db.Column(db.Integer, primary_key=True, unique=True)
    datetime = db.Column(db.DateTime)
    date = db.Column(db.Date, nullable=False)
    comment = db.Column(db.String(500), nullable=False)
    event = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)

    @classmethod
    def add_comment(cls, commenter, comment, event):
        import datetime

        date = str(datetime.datetime.today()).split()[0]
        datetime = datetime.datetime.now()
        return cls(
            commenter=commenter,
            datetime=datetime,
            date=date,
            comment=comment,
            event=event,
        )
