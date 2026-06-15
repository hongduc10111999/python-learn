from pathlib import Path

import pandas as pd
import requests
from flask import Flask, abort, jsonify, render_template, request

from lessons_basic import LESSONS

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR.parent / "day4_5_data" / "data" / "orders.csv"
API_URL = "https://open.er-api.com/v6/latest/USD"

app = Flask(__name__)


def load_orders():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")
    df["total_usd"] = df["quantity"] * df["unit_price_usd"]
    return df


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/lesson/basic/<key>")
def lesson_basic(key):
    if key not in LESSONS:
        abort(404)
    lesson = LESSONS[key]
    rows = lesson["run"]()
    return render_template(
        "basic.html",
        title=lesson["title"],
        file=lesson["file"],
        rows=rows,
        lessons=LESSONS,
        active=key,
    )


@app.route("/lesson/orders")
def lesson_orders():
    return render_template("orders.html")


@app.route("/lesson/stats")
def lesson_stats():
    return render_template("stats.html")


@app.route("/lesson/exchange")
def lesson_exchange():
    return render_template("exchange.html")


@app.route("/api/orders")
def api_orders():
    category = request.args.get("category", "All")
    df = load_orders()
    if category != "All":
        df = df[df["category"] == category]
    return jsonify(
        {
            "categories": ["All"] + sorted(load_orders()["category"].unique().tolist()),
            "orders": df.to_dict(orient="records"),
            "count": len(df),
        }
    )


@app.route("/api/stats")
def api_stats():
    df = load_orders()
    by_category = (
        df.groupby("category")["total_usd"].sum().sort_values(ascending=False)
    )
    by_customer = (
        df.groupby("customer")["total_usd"].sum().sort_values(ascending=False)
    )
    return jsonify(
        {
            "total_orders": int(len(df)),
            "total_revenue": round(float(df["total_usd"].sum()), 2),
            "by_category": by_category.round(2).to_dict(),
            "by_customer": by_customer.round(2).to_dict(),
        }
    )


@app.route("/api/exchange")
def api_exchange():
    currency = request.args.get("currency", "VND")
    df = load_orders()
    total_usd = float(df["total_usd"].sum())
    data = requests.get(API_URL, timeout=10).json()
    rate = data["rates"].get(currency)
    return jsonify(
        {
            "currency": currency,
            "rate": rate,
            "total_usd": round(total_usd, 2),
            "converted": round(total_usd * rate, 2),
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)
