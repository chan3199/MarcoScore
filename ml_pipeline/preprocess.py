import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import joblib
import os

# 📌 경로 설정
DATA_PATH = "data/macro_data.csv"
SCALED_PATH = "data/macro_data_scaled.csv"
SCALER_PATH = "models/scaler.pkl"

# 🔧 전처리 함수
def preprocess_macro_data():
    # 📌 데이터 불러오기
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])

    # 📌 1980년 이후 데이터 필터링
    df = df[df["date"].dt.year >= 1980]

    # 📌 결측치 보간 → 완전 제거
    df = df.sort_values("date").reset_index(drop=True)
    df.interpolate(method="linear", inplace=True)
    df.dropna(inplace=True)

    # 📌 스케일링 대상
    feature_cols = df.columns[df.columns != "date"]
    df[feature_cols] = df[feature_cols].astype(float)

    # 📌 스케일링
    scaler = MinMaxScaler()
    df_scaled = df.copy()
    df_scaled[feature_cols] = scaler.fit_transform(df[feature_cols])

    # 🔍 NaN 확인
    if df_scaled[feature_cols].isnull().values.any():
        print("❌ 스케일링 후 NaN이 존재합니다.")
        print(df_scaled[feature_cols].isnull().sum())
        return

    # 📌 저장
    os.makedirs("models", exist_ok=True)
    df_scaled.to_csv(SCALED_PATH, index=False)
    joblib.dump(scaler, SCALER_PATH)

    print("✅ 스케일된 GDP 분포 확인:")
    print(df_scaled["GDP"].describe())
    print("GDP 샘플:", df_scaled["GDP"].values[:20])
    print("✅ 전처리 및 저장 완료!")

    return df_scaled

if __name__ == "__main__":
    preprocess_macro_data()
