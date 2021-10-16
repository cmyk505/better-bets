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
import pdb

from models import db, connect_db

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:Pancakes21!@localhost:5432/better_bets_test"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "my secret"

connect_db(app)