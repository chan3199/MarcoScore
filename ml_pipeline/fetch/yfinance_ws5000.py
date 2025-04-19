import yfinance as yf

def yfinanceSaveCsv():
    # Wilshire 5000 데이터 다운로드 (1980년부터)
    ticker = "^FTW5000"
    df = yf.download(ticker, start="1980-01-01", interval="1d")

    # 필요한 컬럼만 정리
    df = df[["Close"]].reset_index()
    df.columns = ["date", "MarketCap"]
    df["MarketCap"] *= 1e9  # 💡 억 단위로 가정 (단위 일치시키기 위해)

    # 저장
    df.to_csv("ml_pipeline/data/wilshire5000_yahoo_api.csv", index=False)

    print("Wilshire 5000 데이터 저장 완료!")
