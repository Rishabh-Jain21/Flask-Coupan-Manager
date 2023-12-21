from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from coupans_manager.coupans.forms import CoupanForm
from coupans_manager.models import Coupan
from coupans_manager import db

coupans = Blueprint("coupans", __name__)


@coupans.route("/coupan/new", methods=["GET", "POST"])
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
        return redirect(url_for("main.show_coupans"))

    return render_template(
        "create_coupan.html", title="New Coupan", form=form, legend="CReate COupan"
    )


@coupans.route("/coupan/<int:coupan_id>")
def coupan(coupan_id):
    coupan_1 = Coupan.query.get_or_404(coupan_id)
    return render_template(
        "coupan.html",
        title=coupan_1.title,
        coupan=coupan_1,
    )


@coupans.route("/coupan/<int:coupan_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("coupans.coupan", coupan_id=coupan_1.id))
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


@coupans.route("/coupan/<int:coupan_id>/delete", methods=["POST"])
@login_required
def delete_coupan(coupan_id):
    coupan_1 = Coupan.query.get_or_404(coupan_id)
    if coupan_1.author != current_user:
        abort(403)
    db.session.delete(coupan_1)
    db.session.commit()
    flash("Coupan Deleted", "success")
    return redirect(url_for("main.show_coupans"))
