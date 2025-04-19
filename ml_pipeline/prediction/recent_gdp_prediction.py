import pandas as pd
import numpy as np
import tensorflow as tf
import joblib

# 경로
MODEL_PATH = "ml_pipeline/model/model_long.h5"
SCALE_PATH = "ml_pipeline/models/scaler.pkl"
DATA_PATH = "ml_pipeline/data/macro_data_scaled.csv"

# 파라미터
SEQ_LENGTH = 24
drop_features = ["Consumer_Confidence","Initial_Jobless_Claims", "VIX", "USD_Index", "M2_Money_Supply"]

# 시퀀스 생성 함수
def create_sequences(data, seq_length=24):
    X = []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
    return np.array(X)

def run_prediction():
    # 데이터 불러오기
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df = df[df["date"].dt.year >= 1980].reset_index(drop=True)
    dates = df["date"]
    # 모델 학습 당시 사용한 drop 컬럼 (예시)

    # feature 설정
    feature_cols = df.columns.drop(["date", "GDP"] + drop_features)
    X_all = create_sequences(df[feature_cols].values, SEQ_LENGTH)
    last_sequence = X_all[-1:]
    print("📦 마지막 입력 시퀀스 shape:", last_sequence.shape)

    # 모델 & 스케일러 로드
    model = tf.keras.models.load_model(MODEL_PATH)
    scaler = joblib.load(SCALE_PATH)

    # 예측
    scaled_pred = model.predict(last_sequence).flatten()[0]

    # 역변환 (GDP만)
    gdp_index = list(df.columns).index("GDP") - 1  # date 제거로 -1
    gdp_min = scaler.data_min_[gdp_index]
    gdp_max = scaler.data_max_[gdp_index]
    predicted_gdp = scaled_pred * (gdp_max - gdp_min) + gdp_min

    # 예측 날짜 추론: 마지막 날짜의 다음 분기 시작일
    last_date = df["date"].iloc[-1]
    next_quarter = pd.to_datetime(f"{last_date.year}-{(last_date.month-1)//3*3 + 4}-01") + pd.offsets.QuarterBegin()

    # 저장
    df_result = pd.DataFrame({
        "date": [next_quarter.strftime("%Y-%m-%d")],
        "predicted_gdp": [predicted_gdp]
    })
    df_result.to_csv("ml_pipeline/data/recent_gdp_prediction.csv", index=False)
    print("recent_gdp_prediction.csv 저장 완료!")
    print(df_result)
