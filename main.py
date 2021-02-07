import os
import hashlib

from dotenv import load_dotenv
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from flask_sqlalchemy import SQLAlchemy

# Load .env file into context for development
load_dotenv()

app = Flask(__name__)

# Google Cloud SQL CONFIGURATIONS
USERNAME = os.environ.get('GOOGLE_CLOUD_SQL_USERNAME')
PASSWORD = os.environ.get('GOOGLE_CLOUD_SQL_PASSWORD')
PUBLIC_IP_ADDRESS = os.environ.get('GOOGLE_CLOUD_PUBLIC_ID')
DBNAME = os.environ.get('GOOGLE_CLOUD_SQL_DB_NAME')
PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT_ID')
CONNECTION_NAME = os.environ.get('GOOGLE_CLOUD_SQL_CONNECTION_NAME')

# PW Config
SALT = os.environ.get('SALT')

# Flask app configurations
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqldb://{USERNAME}:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{CONNECTION_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

# START OF MODELS

vaccines = db.Table('vaccines',
    db.Column('vaccine_id', db.Integer, db.ForeignKey(
        'vaccine.id'), primary_key=True),
    db.Column('patient_id', db.Integer, db.ForeignKey(
        'patient.id'), primary_key=True),
    db.Column('injection_site', db.String(10), nullable=False)
)


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    pw = db.Column(db.Text(), nullable=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.String(50), nullable=False)
    vaccines = db.relationship('Vaccine', secondary=vaccines, lazy='subquery',
        backref=db.backref('patients', lazy=True))


class Technician(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    pw = db.Column(db.Text(), nullable=False)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)


class Vaccine(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(200), nullable=False, unique=True)
    number_of_doses = db.Column(db.Integer, nullable=False)

# END OF MODELS

# START OF HELPER FUNCTIONS #

def create_patient(f_name, l_name, phone, dob, pw=None):
    if pw:
        dk = hashlib.pbkdf2_hmac('sha256', bytes(pw, 'utf-8'), bytes(SALT, 'utf-8'), 100000)
    else:
        dk = None

    user = Patient (
        f_name = f_name,
        l_name = l_name,
        phone = phone,
        dob = dob,
        pw = dk.hex() if dk else None
    )

    # adding the fields to users table
    db.session.add(user)
    db.session.commit()
    db.session.close()

def create_tech(f_name, l_name, username, pw, company):
    dk = hashlib.pbkdf2_hmac('sha256', bytes(pw, 'utf-8'), bytes(SALT, 'utf-8'), 100000)

    user = Technician (
        f_name = f_name,
        l_name = l_name,
        username = username,
        pw = dk.hex(),
        company = company
    )

    # adding the fields to users table
    db.session.add(user)
    db.session.commit()
    db.session.close()

def verify_tech(username, pw):
    user = Technician.query.filter(Technician.username == username).first()

    # Handle non existant user
    if not user: 
        return False

    user = user.__dict__

    dk = hashlib.pbkdf2_hmac('sha256', bytes(pw, 'utf-8'), bytes(SALT, 'utf-8'), 100000)
    hash = dk.hex()
    if (user["pw"] == hash):
        return user["id"]
    return False

def verify_patient(phone, pw):
    user = Patient.query.filter(Patient.phone == phone).first()

    # Handle non existant user
    if not user:
        return False

    user = user.__dict__

    dk = hashlib.pbkdf2_hmac('sha256', bytes(pw, 'utf-8'), bytes(SALT, 'utf-8'), 100000)
    hash = dk.hex()
    if (user["pw"] == hash):
        return user["id"]
    return False

def get_tech_data(user_id):
    user = Technician.query.filter(Technician.id == user_id).first()

    # Handle non existant user
    if not user: 
        return False

    user = user.__dict__

    return user

def get_patient_data(user_id):
    user = Patient.query.filter(Patient.id == user_id).first()

    # Handle non existant user
    if not user: 
        return False

    user = user.__dict__

    return user

# END OF HELPER FUNCTIONS #

@app.route("/")
def index():
    return render_template("index.jinja.html")

@app.route("/insights")
def insights():
    user_id = session.get("id", None)
    user_type = session.get("user", None)

    if user_id:
        user_data = {}
        for key, data in session.items():
            user_data[key] = data

        if user_type == "tech":
            return render_template("insights.jinja.html", data=user_data)
        else:
            return redirect(url_for("home"))
    
    return redirect(url_for("index"))

@app.route("/signin", methods = ["POST", "GET"])
def signin():
    if request.method == 'POST':
        phone = request.form.get("phone")
        pw = request.form.get("pw")

        if phone and pw:
            id = verify_patient(phone, pw)

            if id:
                user_data = get_patient_data(id)
                session["user"] = "patient"
                
                for key, value in user_data.items():
                    if key != "_sa_instance_state":
                        session[key] = value

                return redirect(url_for("home"))

        return render_template("signin.jinja.html", user="patient", invalid=True)
    
    user_id = session.get("id", None)

    if user_id:
        return redirect(url_for("home"))

    return render_template("signin.jinja.html", user="patient")

@app.route("/tech-signin", methods = ["POST", "GET"])
def tech_signin():
    if request.method == 'POST':
        username = request.form.get("username")
        pw = request.form.get("pw")

        if username and pw:
            id = verify_tech(username, pw)

            if id:
                user_data = get_tech_data(id)
                session["user"] = "tech"
                
                for key, value in user_data.items():
                    if key != "_sa_instance_state":
                        session[key] = value

                return redirect(url_for("home"))

        return render_template("signin.jinja.html", user="tech", invalid=True)

    user_id = session.get("id", None)

    print(user_id)

    if user_id:
        return redirect(url_for("home"))

    return render_template("signin.jinja.html", user="tech")

@app.route("/logout")
def logout():
    session.clear()
    return(redirect(url_for("index")))

@app.route("/register")
def register():
    return render_template("index.jinja.html")

@app.route("/home")
def home():
    user_id = session.get("id", None)
    user_type = session.get("user", None)

    print(user_id)

    if user_id:
        user_data = {}
        for key, data in session.items():
            user_data[key] = data

        if user_type == "tech":
            return render_template("tech-home.jinja.html", data=user_data)
        else:
            return render_template("patient-home.jinja.html", data=user_data)
    
    return redirect(url_for("index"))

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
