from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "575a581e34d929fc5215c09a934d9a32"  # For dev it can be hardcoded # for prod get it from env variable
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # tells login manager where is our login route
login_manager.login_message_category = "info"

from coupans_manager import routes
