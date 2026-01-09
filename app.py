from flask import Flask,render_template,jsonify,url_for,request
import yfinance as yf
from yfinance import EquityQuery
import pandas as pd
from stock_analyzer import stock_analyzer

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello_world():
    result = {}
    if request.method == 'POST':
        user_budget = request.form.get("user_budget")
        print(user_budget)
        result = stock_analyzer(user_budget)
    return render_template('home.html',recommendations=result)
    

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')