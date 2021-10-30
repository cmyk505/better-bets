from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from faker import Faker
from flask_login import LoginManager, UserMixin
from sqlalchemy.orm import relationship

# using bcrypt for password hashing
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def connect_db(app):
    db.app = app
    db.init_app(app)
    # liao local environment:  comment out if clause
    # because you're not using .env file
<<<<<<< HEAD
    #if app.config["FLASK_ENV"] == "development":
        # User.query.delete()
        # Event.query.delete()
=======
    # if app.config["FLASK_ENV"] == "development":
    #     User.query.delete()
    #     Event.query.delete()
>>>>>>> 481bcc44e14fd697f8e3b1ff02fb1feffde7c9ba
    db.drop_all()
    db.create_all()
    seed_database(app, db)


def seed_database(app, db):
    """Seed database with test data"""

    faker = Faker()
    for _ in range(30):
        db.session.add(
            User(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.email(),
                hashed_password="*FAKE*",
            )
        )
        db.session.add(
            (
                Event(
                    sportsdb_id=faker.unique.random_int(),
                    title=faker.text(100),
                    home_team=faker.text(10),
                    away_team=faker.text(10),
                    date=faker.date_this_month(before_today=False, after_today=True),
                )
            )
        )
    db.session.commit()
    # add user ID of 1 to session ID so we can simulate logged-in user activity


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(200), nullable=False, unique=True)
    hashed_password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    image_file = db.Column(
        db.String(50), nullable=False, default="defaultProfilePic.jpg"
    )

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.image_file}')"

    @classmethod
    def register(cls, password, email):
        hashed_password = bcrypt.generate_password_hash(password)
        hashed_password_utf8 = hashed_password.decode("utf8")
        return cls(hashed_password=hashed_password_utf8, email=email)

    @classmethod
    def authenticate(cls, email, password):
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
    __tablename__ = "user_follow"
    id = db.Column(db.Integer, unique=True)
    follower_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, primary_key=True
    )
    followed_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, primary_key=True
    )


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sportsdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    home_team = db.Column(db.String(50), nullable=False)
    away_team = db.Column(db.String(50), nullable=False)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    resolved = db.Column(db.Boolean, default=False)
    winner = db.Column(db.String(50), default="Undecided")
    date = db.Column(db.Date, nullable=False)

    bets = db.relationship("Bet", backref="event_ref")

    # write methods
    # 1 call api, use sqlalchemy to get event data, write to db
    # 2 determine the winner
    # 3 function that figures out what events need to updated.
    # 4 function update the event records with the results


class UserBalance(db.Model):
    __tablename__ = "user_balance"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=500)


class Bet(db.Model):
    __tablename__ = "bet"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    event = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    selection = db.Column(db.String(100), nullable=False)
    result = db.String(db.String(1))
    final_margin = db.Column(db.Integer, default=0)
    amount = db.Column(db.Integer, nullable=False)


class Comment(db.Model):
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

