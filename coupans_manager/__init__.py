from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from coupans_manager.config import Config

db = SQLAlchemy()

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "users.login"  # tells login manager where is our login route
login_manager.login_message_category = "info"

mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    from coupans_manager.users.routes import users
    from coupans_manager.coupans.routes import coupans
    from coupans_manager.main.routes import main

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)


    app.register_blueprint(users)
    app.register_blueprint(coupans)
    app.register_blueprint(main)

    return app

