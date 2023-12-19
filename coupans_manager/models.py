from datetime import datetime
from coupans_manager import db
from sqlalchemy.ext.hybrid import hybrid_property
from coupans_manager import login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    coupans = db.relationship("Coupan", backref="author", lazy=True)

    def __repr__(self):
        return f"User {self.username}, {self.email} "


class Coupan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    code = db.Column(db.String(30), nullable=False)
    platform_apply = db.Column(db.String(50), nullable=False)
    platform_get = db.Column(db.String(50), nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    details = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    @hybrid_property
    def is_expired(self):
        return bool(datetime.utcnow() > self.expiry_date)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
