from flask import Blueprint, render_template, request

from coupans_manager.models import Coupan

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/coupans")
def show_coupans():
    page = request.args.get("page", 1, type=int)
    coupans_list = Coupan.query.order_by(Coupan.expiry_date).paginate(
        per_page=5, page=page
    )
    return render_template("coupans.html", coupans=coupans_list, title="ALL COUPANS")

