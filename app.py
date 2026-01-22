from flask import Flask, render_template, jsonify, url_for, request, redirect, session
import yfinance as yf
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
    return render_template("home.html")


@app.route("/app", methods=["GET", "POST"])
def app_page():
    # if "user" not in session:
    #     return redirect(url_for("login"))
    result = {}
    if request.method == "POST":
        user_budget = request.form.get("user_budget")
        print(user_budget)
        result = stock_analyzer(user_budget)
    return render_template("app.html", recommendations=result)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        res = supabase.auth.sign_up({"email": email, "password": password})
        if getattr(res, "user", None):
            return redirect(url_for("login"))
        return "Signup failed", 400
    return render_template("signup.html")


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
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
