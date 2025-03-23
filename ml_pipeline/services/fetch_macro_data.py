import pandas as pd
import os
from fetch_fred_data import fetch_all_fred_data

# 📌 저장 경로 설정
DATA_DIR = "..\data"
CSV_PATH = os.path.join(DATA_DIR, "macro_data.csv")

# 📌 데이터 통합 함수
def merge_macro_data():
    fred_data = fetch_all_fred_data()
    merged_df = None

    for key, df in fred_data.items():
        if df is not None:
            df = df.rename(columns={"value": key})
            merged_df = df if merged_df is None else pd.merge(merged_df, df, on="date", how="outer")

    # 📌 결측치 보간
    merged_df = merged_df.sort_values("date").reset_index(drop=True)
    merged_df = merged_df.interpolate(method="linear")  # 선형 보간 적용

    # 📌 데이터 저장
    merged_df.to_csv("data/macro_data.csv", index=False)
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
