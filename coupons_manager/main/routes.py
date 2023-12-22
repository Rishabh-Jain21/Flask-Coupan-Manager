from flask import Blueprint, render_template, request

from coupons_manager.models import Coupon

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/coupons")
def show_coupons():
    page = request.args.get("page", 1, type=int)
    coupons_list = Coupon.query.order_by(Coupon.expiry_date).paginate(
        per_page=5, page=page
    )
    return render_template("coupons.html", coupons=coupons_list, title="ALL COUPANS")
