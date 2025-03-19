import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.fetch_fred_data import fetch_all_fred_data
from services.fetch_yfinance_data import fetch_all_yfinance_data

def merge_macro_data():
    print("📡 경제 데이터 가져오는 중...")

    # ✅ 1. 데이터 수집
    fred_data = fetch_all_fred_data()
    yfinance_data = fetch_all_yfinance_data()

    # ✅ 2. 빈 데이터 필터링
    merged_df = None

    # 🔹 3. FRED 데이터 추가
    for key, df in fred_data.items():
        if df is not None and not df.empty:
            df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
            df = df.rename(columns={"value": key})
            merged_df = df if merged_df is None else pd.merge(merged_df, df, on="date", how="outer")

    # 🔹 4. Yahoo Finance 데이터 추가
    for key, df in yfinance_data.items():
        if df is not None and not df.empty:
            df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
            df = df.rename(columns={"value": key})
            merged_df = pd.merge(merged_df, df, on="date", how="outer")

    # ✅ 5. 결측값 처리
    merged_df = preprocess_macro_data(merged_df)

    print("✅ 통합된 경제 데이터 샘플:")
    print(merged_df.head(10))

    return merged_df


def preprocess_macro_data(df):
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df = df.set_index("date")

    # 🔹 불필요한 지표 제거 (결측치가 지나치게 많은 컬럼 삭제)
    df = df.dropna(thresh=10, axis=1)

    # 🔹 리샘플링 (월별 데이터로 변환)
    df = df.resample("ME").last()

    # 🔹 결측값 처리 (보간)
    df = df.interpolate(method="linear")  # 선형 보간
    df = df.fillna(method="ffill")  # 앞의 값으로 결측치 채우기

    # 🔹 완전히 비어 있는 행 제거
    df = df.dropna(how="all")

    return df.reset_index()


if __name__ == "__main__":
    macro_data = merge_macro_data()
