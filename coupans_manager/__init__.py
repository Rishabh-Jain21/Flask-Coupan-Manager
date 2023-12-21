from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import os


def set_mailer_config(app, environment: str = "localhost"):
    if environment == "localhost":
        # run a local smtp server to simulate it
        # run smtp_server.py in another terminal
        # localhost only for testing # for prod write actual smtp server
        app.config["MAIL_SERVER"] = "localhost"
        app.config["MAIL_PORT"] = 1025
    else:
        app.config["MAIL_SERVER"] = "smtp.googlemail.com"  # Google smtp server
        app.config["MAIL_PORT"] = 587
        app.config["MAIL_USE_TLS"] = True
        app.config["MAIL_USEERNAME"] = os.environ.get("USER_EMAIL")
        app.config["MAIL_PASSWORD"] = os.environ.get("EMAIL_PASS")


app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "575a581e34d929fc5215c09a934d9a32"  # For dev it can be hardcoded # for prod get it from env variable
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"  # tells login manager where is our login route
login_manager.login_message_category = "info"

set_mailer_config(app)
mail = Mail(app)

from coupans_manager.users.routes import users
from coupans_manager.coupans.routes import coupans
from coupans_manager.main.routes import main

app.register_blueprint(users)
app.register_blueprint(coupans)
app.register_blueprint(main)
