from coupans_manager.models import User, Coupan
from flask import render_template, flash, redirect, url_for
from coupans_manager.forms import RegistrationForm, LoginForm
from coupans_manager import app


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
