import yfinance as yf
from yfinance import EquityQuery
import pandas as pd

def stock_analyzer(user_budget):
    High_q = EquityQuery('and', [
            EquityQuery('is-in',['exchange','NSI']),
            EquityQuery('eq', ['region', 'in']),
            # EquityQuery('gt', ['intradaymarketcap', 1000000000])
        ])
    response = yf.screen(High_q, sortField='intradaymarketcap', sortAsc=False, size=250)
        
    stock_list = response.get('quotes', [])
    df = pd.DataFrame(stock_list)
    df_filtered = df[df['regularMarketPreviousClose'] <= float(user_budget)*(0.85)]
    # df_filtered.to_csv('filtered.csv')
    # df.to_csv('marketdata.csv')
    # print(df_filtered.columns)
    results = []
    for symbol in df_filtered['symbol']:
        hist_data = pd.DataFrame(yf.Ticker(symbol).history(period='20d'))
        
        daily_return = hist_data['Close'].pct_change()
        volatility = daily_return.std()
        sma = hist_data['Close'].rolling(window=20).mean().iloc[-1]
        running_max = hist_data['Close'].cummax()
        drawdown = (hist_data['Close'] - running_max) / running_max
        
        score = 100
        if volatility<0.015:
            score=+10
        elif volatility>0.025:
            score=-10
        
        # Drawdown closer to 0 = better
        # Drawdown worse than -5% = subtract points
        if drawdown.min() > -0.03:  # Less than 3% drawdown
            score += 15
        elif drawdown.min() < -0.05:  # More than 5% drawdown
            score -= 15
            
        current_price = hist_data['Close'].iloc[-1]
        if current_price > sma:  # Price above moving average (bullish)
            score += 10
        else:
            score -= 5
        
        results.append({
            'symbol': symbol,
            'volatility': float(volatility),
            'sma': float(sma),
            'drawdown': float(drawdown.min()),
            'score': score
        })
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('score', ascending=False)
    results_df['risk_category'] = pd.cut(results_df['score'], 
                                      bins=[0, 70, 90, 200], 
                                      labels=['High Risk', 'Medium Risk', 'Low Risk'])
    results_df['Company_name'] = df_filtered['shortName'].values
    results_df['Company_longname'] = df_filtered['longName'].values
    # print(results_df)
    # results_df.to_csv('Risk_Alloted.csv')
    recommendations = {}
    for risk_level in ['Low Risk', 'Medium Risk', 'High Risk']:
        recommendations[risk_level] = results_df[results_df['risk_category'] == risk_level].head(5).to_dict('records')
    return recommendations
    
# stock_analyzer(5000)
