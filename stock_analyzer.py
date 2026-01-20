import yfinance as yf
from yfinance import EquityQuery
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed


def analyze_single_stock(symbol):
    try:
        hist_data = yf.Ticker(symbol).history(period="20d")

        if hist_data.empty or len(hist_data) < 2:
            return None

        daily_return = hist_data["Close"].pct_change()
        volatility = daily_return.std()
        sma = hist_data["Close"].rolling(window=20).mean().iloc[-1]
        running_max = hist_data["Close"].cummax()
        drawdown = (hist_data["Close"] - running_max) / running_max

        score = 100
        if volatility < 0.015:
            score += 10
        elif volatility > 0.025:
            score -= 10

        if drawdown.min() > -0.03:
            score += 15
        elif drawdown.min() < -0.05:
            score -= 15

        current_price = hist_data["Close"].iloc[-1]
        if current_price > sma:
            score += 10
        else:
            score -= 5

        # Trade type classification
        if volatility < 0.018:
            trade_type = "Delivery"
        else:
            trade_type = "Intraday"

        return {
            "symbol": symbol,
            "volatility": float(volatility),
            "sma": float(sma),
            "drawdown": float(drawdown.min()),
            "score": score,
            "trade type": trade_type,
        }
    except Exception as e:
        print(f"Error analyzing {symbol}: {e}")
        return None


def stock_analyzer(user_budget):
    High_q = EquityQuery(
        "and",
        [
            EquityQuery("is-in", ["exchange", "NSI"]),
            EquityQuery("eq", ["region", "in"]),
        ],
    )
    response = yf.screen(High_q, sortField="intradaymarketcap", sortAsc=False, size=250)

    stock_list = response.get("quotes", [])
    df = pd.DataFrame(stock_list)
    df_filtered = df[df["regularMarketPreviousClose"] <= float(user_budget) * 0.85]

    results = []
    symbols = df_filtered["symbol"].tolist()

    print(f"Analyzing {len(symbols)} stocks...")

    with ThreadPoolExecutor(max_workers=20) as executor:
        future_to_symbol = {
            executor.submit(analyze_single_stock, symbol): symbol for symbol in symbols
        }

        for future in as_completed(future_to_symbol):
            result = future.result()
            if result:
                results.append(result)

    if not results:
        return {}

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("score", ascending=False)
    results_df["risk_category"] = pd.cut(
        results_df["score"],
        bins=[-50, 70, 90, 200],
        labels=["High Risk", "Medium Risk", "Low Risk"],
    )

    symbol_to_shortname = df_filtered.set_index("symbol")["shortName"].to_dict()
    symbol_to_longname = df_filtered.set_index("symbol")["longName"].to_dict()

    results_df["Company_name"] = results_df["symbol"].map(symbol_to_shortname)
    results_df["Company_longname"] = results_df["symbol"].map(symbol_to_longname)

    # results_df.to_csv("Risk_Alloted.csv")

    recommendations = {}
    for risk_level in ["Low Risk", "Medium Risk", "High Risk"]:
        df_risk = results_df[results_df["risk_category"] == risk_level]
        recommendations[risk_level] = df_risk.head(5).to_dict("records")

    return recommendations


# stock_analyzer(5000)
