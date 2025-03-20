import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.fetch_fred_data import fetch_all_fred_data
from services.fetch_yfinance_data import fetch_all_yfinance_data

def merge_macro_data():
    fred_data = fetch_all_fred_data()
    yfinance_data = fetch_all_yfinance_data()
    merged_df = None

    # 📌 FRED 데이터 병합
    for key, df in fred_data.items():
        if df is not None:
            df = df.rename(columns={"value": key})
            merged_df = df if merged_df is None else pd.merge(merged_df, df, on="date", how="outer")

    # 📌 금융시장 데이터 병합
    for key, df in yfinance_data.items():
        if df is not None:
            df = df.rename(columns={"value": key})
            merged_df = pd.merge(merged_df, df, on="date", how="outer")

    # 📌 결측치 해결 (이전 값으로 채우기)
    merged_df = merged_df.sort_values("date").reset_index(drop=True)
    merged_df.fillna(method="ffill", inplace=True)  # 앞선 값으로 채우기
    merged_df.fillna(method="bfill", inplace=True)  # 뒤에서 채우기

    # 📌 결측치 비율 확인
    missing_ratio = merged_df.isnull().sum() / len(merged_df) * 100
    print("📊 결측치 비율 (%):\n", missing_ratio)

    print("✅ 통합된 경제 및 금융 데이터 샘플:")
    print(merged_df.head(10))  # 상위 10개 행 출력
    return merged_df



def preprocess_macro_data(df):
    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None)
    df = df.set_index("date")

    # 🔹 날짜 정렬 및 리샘플링 (월별 데이터로 변환)
    df = df.resample("ME").last()

    # 🔹 특정 결측치 비율이 높은 컬럼 제거 (절반 이상이 NaN이면 삭제)
    df = df.dropna(thresh=len(df) * 0.5, axis=1)

    # 🔹 NaN 값 처리 (앞의 값으로 채우기 + 선형 보간 적용)
    df = df.ffill().bfill()  # 앞뒤로 결측치 채우기
    df = df.interpolate(method="linear", limit_direction="both")  # 선형 보간 적용

    # 🔹 완전히 비어 있는 행 제거
    df = df.dropna(how="all")

    return df.reset_index()


if __name__ == "__main__":
    macro_data = merge_macro_data()
