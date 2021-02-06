import os

from dotenv import load_dotenv
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from flask_sqlalchemy import SQLAlchemy

# Load .env file into context for development
load_dotenv()

app = Flask(__name__, template_folder="public/templates", static_url_path="/static", static_folder="public/static")

# Google Cloud SQL CONFIGURATIONS
USERNAME = os.environ.get('GOOGLE_CLOUD_SQL_USERNAME')
PASSWORD = os.environ.get('GOOGLE_CLOUD_SQL_PASSWORD')
PUBLIC_IP_ADDRESS = os.environ.get('GOOGLE_CLOUD_PUBLIC_ID')
DBNAME = os.environ.get('GOOGLE_CLOUD_SQL_DB_NAME')
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
CONNECTION_NAME = os.environ.get('GOOGLE_CLOUD_SQL_CONNECTION_NAME')

# Flask app configurations
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://{USERNAME}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{CONNECTION_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app) 

# Models for SQLAlchemy

vaccines = db.Table('vaccines',
    db.Column('vaccine_id', db.Integer, db.ForeignKey('vaccine.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id'), primary_key=True)
)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    phone = db.Column(db.String(20), nullable = False, unique = True)
    pw = db.Column(db.Text(), nullable = True)
    f_name = db.Column(db.String(50), nullable = False)
    l_name = db.Column(db.String(50), nullable = False)
    dob = db.Column(db.String(50), nullable = False)
    vaccines = db.relationship('Vaccine', secondary=vaccines, lazy='subquery',
        backref=db.backref('patients', lazy=True))

class Technician(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    username = db.Column(db.String(50), nullable = False, unique = True)
    pw = db.Column(db.Text(), nullable = False)
    f_name = db.Column(db.String(50), nullable = False)
    l_name = db.Column(db.String(50), nullable = False)
    company = db.Column(db.String(50), nullable = False)

class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(200), nullable = False, unique = True)
    number_of_doses = db.Column(db.Integer, nullable = False)


@app.route("/")
def index():
    return render_template("index.jinja.html")


@app.errorhandler(401)
def FUN_401(error):
    return render_template("401.jinja.html"), 401


@app.errorhandler(403)
def FUN_403(error):
    return render_template("403.jinja.html"), 403


@app.errorhandler(404)
def FUN_404(error):
    return render_template("404.jinja.html"), 404


@app.errorhandler(405)
def FUN_405(error):
    return render_template("405.jinja.html"), 405


@app.errorhandler(413)
def FUN_413(error):
    return render_template("413.jinja.html"), 413


@app.errorhandler(500)
def FUN_500(error):
    return render_template("500.jinja.html"), 500


if __name__ == "__main__":
    # db.create_all() <-- function to create tables in the database from the new models
    app.run(debug=True, host="localhost")
