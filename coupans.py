from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property

app = Flask(__name__)
app.config[
    "SECRET_KEY"
] = "575a581e34d929fc5215c09a934d9a32"  # For dev it can be hardcoded # for prod get it from env variable
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)


class User(db.Model):
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


coupans_list = [
    {
        "coupan_id": 1,
        "title": "get 50% off on any product",
        "code": "123456789",
        "platform_to_apply": "Flipkart",
        "platform_we_got_from": "googlepay",
        "expiry_date": "Oct 12,2025",
        "details": "get 50% off on any product, Valid only on first purchase",
        "is_expired": False,
        "is_redemmed": False,
    },
    {
        "coupan_id": 2,
        "title": "get 70% off on first purchase",
        "code": "987654",
        "platform_to_apply": "Amazon",
        "platform_we_got_from": "paytm",
        "expiry_date": "Aug 17,2024",
        "details": "get 70% off on first purchase,valid for new users",
        "is_expired": False,
        "is_redemmed": False,
    },
]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/coupans")
def show_coupans():
    return render_template("coupans.html", coupans=coupans_list, title="ALL COUPANS")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f"Accounted Created for {form.username.data}", "success")
        return redirect(url_for("show_coupans"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "admin":
            flash("You have been logged in", "success")
            return redirect(url_for("show_coupans"))
        else:
            flash("Unsuccessful login attempt.Check details", "danger")

    return render_template("login.html", title="Login", form=form)
