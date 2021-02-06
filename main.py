import hashlib
import os

from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="public/templates", static_url_path="/static", static_folder="public/static")

# app.secret_key = os.getenv("APP_SECRET")
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

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
    app.run(debug=True, host="localhost")