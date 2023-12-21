from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from coupans_manager.models import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), Length(min=2, max=20)]
    )  # username required and length between 2 and 20
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        label="Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken.Please choose different one")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken.Please choose different one")


class LoginForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        label="Username", validators=[DataRequired(), Length(min=2, max=20)]
    )  # username required and length between 2 and 20
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken.Please choose different one"
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is taken.Please choose different one")


class CoupanForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=2, max=20)])
    code = StringField("Code", validators=[DataRequired(), Length(min=2, max=20)])
    platform_apply = StringField(
        "Applicable on platform", validators=[DataRequired(), Length(min=2, max=20)]
    )
    platform_get = StringField(
        "From where you got it", validators=[DataRequired(), Length(min=2, max=20)]
    )
    expiry_date = DateField("expiry", validators=[DataRequired()], format="%Y-%m-%d")
    details = TextAreaField("details", validators=[DataRequired()])
    submit = SubmitField("Add Coupan")


class RequestResetForm(FlaskForm):
    email = StringField(label="Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No account exists for provided email")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label="Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        label="Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
