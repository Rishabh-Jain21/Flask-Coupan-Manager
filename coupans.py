from flask import Flask, render_template

app = Flask(__name__)

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
