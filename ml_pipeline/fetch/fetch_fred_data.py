import requests
import pandas as pd
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()
FRED_API_KEY = os.getenv("FRED_API_KEY")

# FRED에서 수집할 거시경제 지표 리스트 (불필요한 지표 제거 & 추가)
FRED_SERIES = {
    "GDP": "GDP",
    "Retail_Sales": "RSAFS",
    "Unemployment": "UNRATE",
    "10Y_2Y_Spread": "T10Y2Y",
    "M2_Money_Supply": "M2SL",
    "Industrial_Production": "INDPRO",
    "Fed_Funds_Rate": "FEDFUNDS",
    "Personal_Consumption": "PCE",
    "USD_Index": "DTWEXBGS",
    "VIX": "VIXCLS",
    "Initial_Jobless_Claims": "ICSA",
    "Government_Expenditure": "GCE",
    "Consumer_Confidence": "UMCSENT",
    "Private_Investment": "GPDI",
}


# FRED 데이터 가져오기
def fetch_fred_data(series_id):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if "observations" in data:
        df = pd.DataFrame(data["observations"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"])
        return df[["date", "value"]]
    else:
        print(f"데이터 가져오기 실패: {series_id}")
        return None

# 여러 지표 데이터 가져오기
def fetch_all_fred_data():
    dataframes = {key: fetch_fred_data(series) for key, series in FRED_SERIES.items()}
    return dataframes

if __name__ == "__main__":
    fred_data = fetch_all_fred_data()
    for key, df in fred_data.items():
        if df is not None:
            print(f"{key} 데이터 샘플:\n", df.head(), "\n")