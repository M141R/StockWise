from flask import Flask, render_template, jsonify, url_for, request
import yfinance as yf
from yfinance import EquityQuery
import pandas as pd
from stock_analyzer import stock_analyzer

app = Flask(__name__)


@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route("/app", methods=["GET", "POST"])
def app_page():
    result = {}
    if request.method == "POST":
        user_budget = request.form.get("user_budget")
        print(user_budget)
        result = stock_analyzer(user_budget)
    return render_template("app.html", recommendations=result)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
