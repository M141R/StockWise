from flask import Flask, render_template, jsonify, url_for, request, redirect, session
from flask import jsonify, request
import yfinance as yf
import datetime
from yfinance import EquityQuery
import pandas as pd
from stock_analyzer import stock_analyzer
from dotenv import load_dotenv
import os
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = Flask(__name__)

app.secret_key = "your_secret_key"


@app.route("/")
def hello_world():
    return render_template("home.html", title="Home")


@app.route("/app", methods=["GET", "POST"])
def app_page():
    # if "user" not in session:
    #     return redirect(url_for("login"))
    result = {}
    if request.method == "POST":
        user_budget = request.form.get("user_budget")
        print(user_budget)
        result = stock_analyzer(user_budget)
    return render_template("app.html", recommendations=result, title="App")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        res = supabase.auth.sign_up({"email": email, "password": password})
        if getattr(res, "user", None):
            return redirect(url_for("account"))
        return "Signup failed", 400
    return render_template("signup.html", title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        res = supabase.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        if getattr(res, "user", None):
            session["user"] = res.user.id
            return redirect(url_for("app_page"))
        return "Login failed", 401
    return render_template("login.html", title="Login")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route("/stock/<symbol>")
def stock_detail(symbol):
    # Fetch 6 months historical data
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="6mo")
    # Prepare data for chart.js
    chart_data = {
        "dates": hist.index.strftime("%Y-%m-%d").tolist(),
        "close": hist["Close"].fillna(method="ffill").tolist(),
    }
    # Fetch latest news (yfinance)
    news = []
    try:
        news = ticker.news[:5]  # Get top 5 news articles
    except Exception:
        pass
    # You can add more: e.g. key stats, company info, analyst recommendations
    info = ticker.info
    return render_template(
        "stock_detail.html",
        symbol=symbol,
        chart_data=chart_data,
        news=news,
        info=info,
    )


def get_user_id():
    return session.get("user")


@app.route("/save_stock", methods=["POST"])
def save_stock():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    symbol = request.json.get("symbol")
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400
    # Save to Supabase (table: saved_stocks)
    data = {"user_id": user_id, "symbol": symbol}
    supabase.table("saved_stocks").insert(data).execute()
    return jsonify({"success": True})


@app.route("/save_list", methods=["POST"])
def save_list():
    user_id = get_user_id()
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    symbols = request.json.get("symbols")
    if not symbols or not isinstance(symbols, list):
        return jsonify({"error": "No symbols provided"}), 400
    data = [{"user_id": user_id, "symbol": s} for s in symbols]
    supabase.table("saved_stocks").insert(data).execute()
    return jsonify({"success": True})


@app.route("/account", methods=["GET", "POST"])
def account():
    user_id = session.get("user")
    if not user_id:
        return redirect(url_for("login"))
    # Get user info from Supabase
    user = supabase.auth.get_user()
    email = user.user.email if user and user.user else "Unknown"
    is_confirmed = user.user.confirmed_at is not None if user and user.user else False
    resend_success = None
    if request.method == "POST" and request.form.get("resend_confirm"):
        try:
            # Use Supabase API to resend confirmation email
            supabase.auth.api.resend(email)
            resend_success = True
        except Exception as e:
            print("Resend error:", e)
            resend_success = False
    # Get saved stocks
    saved = (
        supabase.table("saved_stocks").select("symbol").eq("user_id", user_id).execute()
    )
    saved_symbols = (
        [row["symbol"] for row in saved.data] if saved and saved.data else []
    )
    return render_template(
        "account.html",
        email=email,
        is_confirmed=is_confirmed,
        resend_success=resend_success,
        saved_symbols=saved_symbols,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
