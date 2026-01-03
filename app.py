from flask import Flask,render_template,jsonify,url_for
import yfinance as yf
from yfinance import EquityQuery

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('home.html')

@app.route("/debug")
def debug_data():
    q = EquityQuery('and', [
    #    EquityQuery('gt', ['percentchange', 3]),
       EquityQuery('eq', ['region', 'in']),
        EquityQuery('gt', ['intradaymarketcap', 1000000000])
])
    response = yf.screen(q, sortField = 'intradaymarketcap', sortAsc = False, size=100)
    return jsonify(response)


    
    return render_template('stocks.html', stocks=stock_list)
    
        
 

if __name__ == '__main__':
    app.run(debug=True)