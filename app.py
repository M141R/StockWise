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

@app.route("/debug")
def debug_data():
    q = EquityQuery('and', [
    #    EquityQuery('gt', ['percentchange', 3]),
       EquityQuery('eq', ['region', 'in']),
        EquityQuery('gt', ['intradaymarketcap', 1000000000])
])
    response = yf.screen(q, sortField = 'intradaymarketcap', sortAsc = False, size=100)
    return jsonify(response)

@app.route("/stocks")
def stocks():
    High_q = EquityQuery('and', [
        EquityQuery('eq', ['region', 'in']),
        EquityQuery('gt', ['intradaymarketcap', 1000000000])
    ])
    response = yf.screen(High_q, sortField='intradaymarketcap', sortAsc=False, size=100)
    
    stock_list = response.get('quotes', [])
    
    return render_template('stocks.html', stocks=stock_list)
    

if __name__ == '__main__':
    app.run(debug=True)