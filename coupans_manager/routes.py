from coupans_manager.models import User, Coupan
from flask import render_template, flash, redirect, url_for, request
from coupans_manager.forms import RegistrationForm, LoginForm, UpdateAccountForm
from coupans_manager import app, bcrypt, db
from flask_login import login_required, login_user, current_user, logout_user

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
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        user_1 = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user_1)
        db.session.commit()

        flash(f"Your Account is created", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user_1 = User.query.filter_by(email=form.email.data).first()

        if user_1 and bcrypt.check_password_hash(user_1.password, form.password.data):
            login_user(user_1, form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Unsuccessful login attempt.Check details", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been  updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)
