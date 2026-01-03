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

@app.route("/stocks")
def stocks():
    High_q = EquityQuery('and', [
        EquityQuery('eq', ['region', 'in']),
        EquityQuery('gt', ['intradaymarketcap', 1000000000])
    ])
    response = yf.screen(High_q, sortField='intradaymarketcap', sortAsc=False, size=100)
    
    stock_list = response.get('quotes', [])
    

    # Mid_q = EquityQuery('and', [
    #     EquityQuery('eq', ['region', 'in']),
    #     EquityQuery('gt', ['intradaymarketcap',600000000]),
    #     EquityQuery('lt', ['intradaymarketcap', 2500000000])
    # ])
    # response2 = yf.screen(Mid_q, sortField='intradaymarketcap', size=250)
    # stock_list_mid = response2.get('quotes',[])
    
    # Small_q = EquityQuery(
    # 'and', [
    #     EquityQuery('eq', ['region', 'in']),
    #     EquityQuery('lt', ['intradaymarketcap', 600_000_000])
    # ])

    # response3 = yf.screen(
    #     Small_q,
    #     sortField='intradaymarketcap',
    #     sortAsc=False,
    #     size=250
    # )

    # stock_list_small = response3.get('quotes', [])
    
    return render_template('stocks.html', stocks=stock_list)
    
        
 

if __name__ == '__main__':
    app.run(debug=True)