from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CouponForm(FlaskForm):
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
    submit = SubmitField("Add Coupon")
