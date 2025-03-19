import yfinance as yf
import pandas as pd

# ✅ 불필요한 결측치가 많은 자산 제거
ASSETS = {
    "S&P 500": "^GSPC",
    "Gold": "GC=F",
    "Crude Oil": "CL=F",
    "Nasdaq 100": "^NDX",
}

# Yahoo Finance 데이터 가져오기
def fetch_yfinance_data(symbol):
    asset = yf.Ticker(symbol)
    df = asset.history(period="max")
    df = df.reset_index()[["Date", "Close"]]
    df.columns = ["date", "value"]
    df["date"] = pd.to_datetime(df["date"])
    return df

# 여러 자산 데이터 가져오기
def fetch_all_yfinance_data():
    dataframes = {key: fetch_yfinance_data(symbol) for key, symbol in ASSETS.items()}
    return dataframes

if __name__ == "__main__":
    yfinance_data = fetch_all_yfinance_data()
    for key, df in yfinance_data.items():
        if df is not None:
            print(f"📊 {key} 데이터 샘플:\n", df.head(), "\n")
