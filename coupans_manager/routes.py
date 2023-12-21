from datetime import datetime
from coupans_manager.models import User, Coupan
from flask import abort, render_template, flash, redirect, url_for, request
from coupans_manager.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    CoupanForm,
    RequestResetForm,
    ResetPasswordForm,
)
from coupans_manager import app, bcrypt, db, mail
from flask_login import login_required, login_user, current_user, logout_user
from flask_mail import Message


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/coupans")
def show_coupans():
    page = request.args.get("page", 1, type=int)
    coupans_list = Coupan.query.order_by(Coupan.expiry_date).paginate(
        per_page=5, page=page
    )
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


@app.route("/coupan/new", methods=["GET", "POST"])
@login_required
def new_coupan():
    form = CoupanForm()
    if form.validate_on_submit():
        coupan_1 = Coupan(
            title=form.title.data,
            code=form.code.data,
            platform_apply=form.platform_apply.data,
            platform_get=form.platform_get.data,
            expiry_date=form.expiry_date.data,
            details=form.details.data,
            author=current_user,
        )
        db.session.add(coupan_1)
        db.session.commit()

        flash("New Coupan Added", "success")
        return redirect(url_for("show_coupans"))

    return render_template(
        "create_coupan.html", title="New Coupan", form=form, legend="CReate COupan"
    )


@app.route("/coupan/<int:coupan_id>")
def coupan(coupan_id):
    coupan_1 = Coupan.query.get_or_404(coupan_id)
    return render_template(
        "coupan.html",
        title=coupan_1.title,
        coupan=coupan_1,
    )


@app.route("/coupan/<int:coupan_id>/update", methods=["GET", "POST"])
@login_required
def update_coupan(coupan_id):
    coupan_1 = Coupan.query.get_or_404(coupan_id)
    if coupan_1.author != current_user:
        abort(403)
    form = CoupanForm()

    if form.validate_on_submit():
        coupan_1.title = form.title.data
        coupan_1.code = form.code.data
        coupan_1.platform_apply = form.platform_apply.data
        coupan_1.platform_get = form.platform_get.data
        coupan_1.details = form.details.data
        coupan_1.date_posted = datetime.utcnow()
        db.session.commit()
        flash("Coupans details Updated", "success")
        return redirect(url_for("coupan", coupan_id=coupan_1.id))
    elif request.method == "GET":
        form.title.data = coupan_1.title
        form.code.data = coupan_1.code
        form.platform_apply.data = coupan_1.platform_apply
        form.platform_get.data = coupan_1.platform_get
        form.expiry_date.data = coupan_1.expiry_date
        form.details.data = coupan_1.details

    return render_template(
        "create_coupan.html", title="Update Coupan", form=form, legend="Update COupan"
    )


@app.route("/coupan/<int:coupan_id>/delete", methods=["POST"])
@login_required
def delete_coupan(coupan_id):
    coupan_1 = Coupan.query.get_or_404(coupan_id)
    if coupan_1.author != current_user:
        abort(403)
    db.session.delete(coupan_1)
    db.session.commit()
    flash("Coupan Deleted", "success")
    return redirect(url_for("show_coupans"))


@app.route("/user/<string:username>")
def user_coupans(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    coupans_list = (
        Coupan.query.filter_by(author=user)
        .order_by(Coupan.expiry_date)
        .paginate(per_page=5, page=page)
    )
    return render_template(
        "user_coupans.html",
        coupans=coupans_list,
        title=f"{username} Coupans",
        user=user,
    )


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        subject="Password Reset Request",
        sender="noreply@demo.com",
        recipients=[user.email],
    )
    msg.body = f"""
        Password Reset request is generated
        The link is valid for 30 
        To reset password visit following link
             {url_for('reset_token',token=token,_external=True)}

        Valid only for 30 minutes
        If you did not make this request ignore it.

         """
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email has been sent with instructions to reset password", "info")
        return redirect(url_for("login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    user = User.verify_reset_toekn(token)
    if user is None:
        flash("That is an invalid or ecpired token", "warning")
        return redirect(url_for("reset_request"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )

        user.password = hashed_password
        db.session.commit()

        flash(f"Your Password has bee updated", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
