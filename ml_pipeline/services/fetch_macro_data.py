import pandas as pd
import os
from fetch_fred_data import fetch_all_fred_data
from fetch_yfinance_data import fetch_all_yfinance_data

# 📌 저장 경로 설정
DATA_DIR = "..\data"
CSV_PATH = os.path.join(DATA_DIR, "macro_data.csv")

# 📌 데이터 통합 함수
def merge_macro_data():
    print("📥 경제 데이터 가져오는 중...")

    # 🔹 FRED 및 Yahoo Finance 데이터 수집
    fred_data = fetch_all_fred_data()
    yfinance_data = fetch_all_yfinance_data()

    # 🔹 데이터프레임 초기화
    merged_df = None

    # 🔹 FRED 데이터 합치기
    for key, df in fred_data.items():
        if df is not None:
            df = df.rename(columns={"value": key})
            merged_df = df if merged_df is None else pd.merge(merged_df, df, on="date", how="outer")

    # 🔹 Yahoo Finance 데이터 합치기
    for key, df in yfinance_data.items():
        if df is not None:
            df = df.rename(columns={"value": key})
            merged_df = pd.merge(merged_df, df, on="date", how="outer")

    # 📌 결측치 처리 (선형 보간법 적용)
    merged_df = merged_df.sort_values("date").reset_index(drop=True)
    merged_df = merged_df.interpolate(method="linear")

    return merged_df

# 📌 데이터 저장 함수
def save_macro_data():
    # 데이터 통합
    macro_data = merge_macro_data()

    # 🔹 데이터 폴더 생성 (존재하지 않으면)
    os.makedirs(DATA_DIR, exist_ok=True)

    # 🔹 CSV로 저장
    macro_data.to_csv(CSV_PATH, index=False)
    print(f"✅ 데이터 저장 완료: {CSV_PATH}")

if __name__ == "__main__":
    save_macro_data()
