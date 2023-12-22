from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from coupons_manager.coupons.forms import CouponForm
from coupons_manager.models import Coupon
from coupons_manager import db

coupons = Blueprint("coupons", __name__)


@coupons.route("/coupon/new", methods=["GET", "POST"])
@login_required
def new_coupon():
    form = CouponForm()
    if form.validate_on_submit():
        coupon_1 = Coupon(
            title=form.title.data,
            code=form.code.data,
            platform_apply=form.platform_apply.data,
            platform_get=form.platform_get.data,
            expiry_date=form.expiry_date.data,
            details=form.details.data,
            author=current_user,
        )
        db.session.add(coupon_1)
        db.session.commit()

        flash("New Coupon Added", "success")
        return redirect(url_for("main.show_coupons"))

    return render_template(
        "create_coupon.html", title="New Coupon", form=form, legend="Create Coupan"
    )


@coupons.route("/coupon/<int:coupon_id>")
def coupon(coupon_id):
    coupon_1 = Coupon.query.get_or_404(coupon_id)
    return render_template(
        "coupon.html",
        title=coupon_1.title,
        coupon=coupon_1,
    )


@coupons.route("/coupon/<int:coupon_id>/update", methods=["GET", "POST"])
@login_required
def update_coupon(coupon_id):
    coupon_1 = Coupon.query.get_or_404(coupon_id)
    if coupon_1.author != current_user:
        abort(403)
    form = CouponForm()

    if form.validate_on_submit():
        coupon_1.title = form.title.data
        coupon_1.code = form.code.data
        coupon_1.platform_apply = form.platform_apply.data
        coupon_1.platform_get = form.platform_get.data
        coupon_1.details = form.details.data
        coupon_1.date_posted = datetime.utcnow()
        db.session.commit()
        flash("Coupons details Updated", "success")
        return redirect(url_for("coupons.coupon", coupon_id=coupon_1.id))
    elif request.method == "GET":
        form.title.data = coupon_1.title
        form.code.data = coupon_1.code
        form.platform_apply.data = coupon_1.platform_apply
        form.platform_get.data = coupon_1.platform_get
        form.expiry_date.data = coupon_1.expiry_date
        form.details.data = coupon_1.details

    return render_template(
        "create_coupon.html", title="Update Coupon", form=form, legend="Update COupan"
    )


@coupons.route("/coupon/<int:coupon_id>/delete", methods=["POST"])
@login_required
def delete_coupon(coupon_id):
    coupon_1 = Coupon.query.get_or_404(coupon_id)
    if coupon_1.author != current_user:
        abort(403)
    db.session.delete(coupon_1)
    db.session.commit()
    flash("Coupon Deleted", "success")
    return redirect(url_for("main.show_coupons"))
