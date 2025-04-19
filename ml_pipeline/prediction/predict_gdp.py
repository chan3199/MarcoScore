import pandas as pd
import numpy as np
import joblib
import tensorflow as tf

# 경로
DATA_PATH = "data/macro_data_scaled.csv"
SCALER_PATH = "models/scaler.pkl"
MODEL_PATH = "model/model_long.h5"
SEQ_LENGTH = 24
TARGET_COL = "GDP"

# 데이터 로드
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df[df["date"].dt.year >= 1980].reset_index(drop=True)

# 스케일러 로드
scaler = joblib.load(SCALER_PATH)

# 입력 피처 선택
drop_cols = ["Consumer_Confidence", "CCI", "Initial_Jobless_Claims", "M2_Money_Supply", "VIX", "USD_Index"]
feature_cols = df.columns.drop(["date", TARGET_COL] + drop_cols)

# 입력 시퀀스 구성
X_input = df[feature_cols].values[-SEQ_LENGTH:].reshape(1, SEQ_LENGTH, len(feature_cols))

# 모델 로드
model = tf.keras.models.load_model(MODEL_PATH)

# 예측
scaled_pred = model.predict(X_input)[0][0]

# 역변환 (GDP 스케일 복원)
# -> MinMaxScaler는 전체 feature에 대해 학습되었기 때문에, GDP 하나만 복원해야 할 때는 아래처럼 처리했음
gdp_index = list(df.columns.drop("date")).index(TARGET_COL)
gdp_min = scaler.data_min_[gdp_index]
gdp_max = scaler.data_max_[gdp_index]
gdp_pred = scaled_pred * (gdp_max - gdp_min) + gdp_min

# 이전 GDP 값 추출
last_scaled_gdp = df[TARGET_COL].values[-1]
last_gdp = last_scaled_gdp * (gdp_max - gdp_min) + gdp_min

# 비교 및 출력
change = gdp_pred - last_gdp
percent_change = (change / last_gdp) * 100

print(f"다음 분기 예측 GDP: {gdp_pred:,.2f} (단위: 억 달러)")
print(f"이전 분기 실제 GDP: {last_gdp:,.2f} (단위: 억 달러)")
print(f"증감: {change:,.2f}억 달러 ({percent_change:.2f}%)")
