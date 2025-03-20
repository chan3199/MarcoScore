import yfinance as yf
import pandas as pd

# 📌 가져올 금융시장 데이터 심볼 리스트
YFINANCE_TICKERS = {
    "S&P_500": "^GSPC",
    "Nasdaq_100": "^NDX",
    "Russell_2000": "^RUT",
    "VIX": "^VIX",
    "USD_Index": "DX-Y.NYB",
}

# 📌 금융시장 데이터 가져오기 (Yahoo Finance)
def fetch_yfinance_data(ticker):
    try:
        df = yf.download(ticker, start="1990-01-01", end="2025-12-31", progress=False)
        df = df[["Adj Close"]].reset_index()
        df.columns = ["date", "value"]
        return df
    except Exception as e:
        print(f"❌ {ticker} 데이터 가져오기 실패:", e)
        return None

# 📌 전체 금융시장 데이터 가져오기
def fetch_all_yfinance_data():
    dataframes = {key: fetch_yfinance_data(ticker) for key, ticker in YFINANCE_TICKERS.items()}
    return dataframes

if __name__ == "__main__":
    yfinance_data = fetch_all_yfinance_data()
    for key, df in yfinance_data.items():
        if df is not None:
            print(f"📊 {key} 데이터 샘플:\n", df.head(), "\n")
