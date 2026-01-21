# **STOCK WISE**
## **StockWise : Risk-Aware Stock Decision Support System**

## Team Details:

### Team Name: **IT WORKS**





### TEAM MEMBERS:

[MIHIR KUMAR]

[SATYAM RAO]

[RAKESH SHRIVASTAVA]

## **DOMAIN OF PROJECT:**

Artificial Intelligence (AI) / Financial Technology (FinTech)

### IDEA:

The project aims to build a **risk-aware stock market decision support system for small and cautious investors**.

Instead of focusing on **real-time trading execution**, the system helps users make **pre-investment decisions** by analyzing historical market data.

Users input their investment budget and risk appetite, and the system evaluates stocks based on **volatility, trend strength, and market capitalization, categorizing them into low, medium, and high risk groups**.

## ACHIEVEMENTS THUS FAR:


1) Integrated Yahoo Finance (yFinance) API for stock market data collection.

2) Implemented budget-based stock filtering.

3) Built rule-based logic for

       *Risk classification:

       *Trend analysis (SMA & EMA)

       *Volatility calculation

       *Categorized stocks into Large-cap, Mid-cap, and Small-cap.

       *Developed a Flask-based backend for data processing and routing.

       *Designed a clean frontend UI for displaying insights.

## OVERVIEW:

This project uses Python, Flask, and Pandas to analyze historical stock market data and generate clear, investor-friendly insights.

The system focuses on:

Helping users understand risk before investing

Filtering stocks based on budget constraints

Providing explainable analytics, not predictions

The platform is especially targeted at beginner and amateur investors who lack deep market knowledge but wish to invest responsibly.

## **HOW TO EXECUTE:**

1.Clone the Repository:

 Clone the repository to your local system:

git clone https://github.com/your-username/stockwise

2.Navigate to the Project Directory
cd stockwise

3.Create a Virtual Environment (Optional but Recommended)
python -m venv venv


###   Activate it: venv\Scripts\activate

4.Install Dependencies: 
pip install -r requirements.txt

5.Run the Flask Application: 
python app.py

6.Open in Browser
http://127.0.0.1:5000/

## **KEY FILES:**

## 1.**app.py**

 Main Flask application file that:

Handles routing

Accepts user input

Calls stock analysis logic

Renders results to frontend templates

## 2.**stock_analyzer.py**

Contains the core logic for:

     *Data filtering

     *Volatility calculation

     *Trend detection

     *Risk scoring and categorization

## 3.**templates/**

HTML files for rendering the frontend UI.


##  **FEATURES**:

 ## 1) Stock Filtering:

  ### Filters stocks based on user-defined investment budget.Only affordable stocks are considered for further analysis.

--------------------------------------------------------------------------------------------------

## 2)Risk-Aware Categorization:

 ### Classifies stocks into Low, Medium, and High risk categories.Uses volatility, drawdown, and trend behavior.
--------------------------------------------------------------------------------------------------

## 3)Trend-Based Analysis:
### Uses Simple Moving Average (SMA) and Exponential Moving Average (EMA).Identifies Bullish, Bearish, or Sideways trends.
--------------------------------------------------------------------------------------------------

## 4)Volatility Assessment:
### Measures daily price fluctuations. Helps users judge stability vs opportunity.
--------------------------------------------------------------------------------------------------
## 5)Market Capitalization Classification:

### Stocks grouped into:

*Large-cap

*Mid-cap

*Small-cap

# FUTURE SCOPE:

## News sentiment analysis

## Volatility spike detection

## Portfolio-level recommendations

## Personalized investor profiles

## Improved data visualization and UI/UX

 # **DISCLAIMER:**

###  This project is developed solely for academic and IEEE evaluation purposes. It does not provide financial advice and should not be used for actual trading decisions.