from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)
    db.drop_all
    db.create_all()


class UserFollow(db.Model):
    __tablename__ = "UserFollow"
    id = db.Column(db.Integer, unique=True)
    follower_id = db.Column(
        db.Integer, db.ForeignKey("User.id"), nullable=False, primary_key=True
    )
    followed_id = db.Column(
        db.Integer, db.ForeignKey("User.id", nullable=False, primary_key=True)
    )


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    hashed_password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


class Event(db.Model):
    __tablename__ = "Event"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sportsdb_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    home_team = db.Column(db.String(50), nullable=False)
    away_team = db.Column(db.String(50), nullable=False)
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    date = db.Column(db.Date, nullable=False)


class UserBalance(db.Model):
    __tablename__ = "UserBalance"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=500)


class Comment(db.Model):
    __tablename__ = "Comment"
    commenter = db.Column(db.Integer, db.ForeignKey("User.id", nullable=False))
    id = db.Column(db.Integer, primary_key=True, unique=True)
    datetime = db.Column(db.DateTime)
    date = db.Column(db.Date, nullable=False)
    event = db.Column(db.Integer, db.ForeignKey("Event.id", nullable=False))
