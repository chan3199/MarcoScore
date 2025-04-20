import pandas as pd
import os
from ml_pipeline.fetch.fetch_fred_data import fetch_all_fred_data
from ml_pipeline.fetch.yfinance_ws5000 import yfinanceSaveCsv

# 저장 경로 설정
DATA_DIR = "ml_pipeline/data"
CSV_PATH = os.path.join(DATA_DIR, "macro_data.csv")

# 데이터 통합 함수
def merge_macro_data():
    fred_data = fetch_all_fred_data()
    merged_df = None

    for key, df in fred_data.items():
        if df is not None:
            df = df.rename(columns={"value": key})
            merged_df = df if merged_df is None else pd.merge(merged_df, df, on="date", how="outer")

    # 정렬 및 결측치 처리
    merged_df = merged_df.sort_values("date").reset_index(drop=True)
    merged_df = merged_df.interpolate(method="linear")
    merged_df = merged_df.dropna(thresh=5)  # 5개 이상 결측치 있는 행 제거 (선택)
    return merged_df

# 실행용 함수 (통합 + 저장)
def run_macro_fetch():
    macro_data = merge_macro_data()
    os.makedirs(DATA_DIR, exist_ok=True)
    macro_data.to_csv(CSV_PATH, index=False)
    print(f"macro_data.csv 저장 완료: {CSV_PATH}")

    # 윌셔 5000도 저장
    yfinanceSaveCsv()

# 단독 실행 시
if __name__ == "__main__":
    run_macro_fetch()
