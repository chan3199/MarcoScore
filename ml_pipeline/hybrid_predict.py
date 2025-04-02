# hybrid_predict.py

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# 📌 설정
DATA_PATH = "data/macro_data_scaled.csv"
LONG_MODEL_PATH = "model/model_long.h5"
RECENT_MODEL_PATH = "model/model_recent.h5"
SEQ_LENGTH = 24
RECENT_RATIO = 0.5  # 마지막 50%는 recent 모델로 예측

# 📌 drop feature 정의 (학습 기준)
drop_long = ["Consumer_Confidence", "CCI", "Initial_Jobless_Claims", "VIX", "USD_Index"]
drop_recent = ["CCI"]

# 📌 시계열 생성 함수
def create_sequences(data, target, seq_length=24):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(target[i+seq_length])
    return np.array(X), np.array(y)

# 📌 데이터 로딩 및 전처리
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df[df["date"].dt.year >= 1980].reset_index(drop=True)
target = df["GDP"].values

# 📌 feature 준비
df_long = df.drop(columns=["date","GDP"] + drop_long)
df_recent = df.drop(columns=["date","GDP"] + drop_recent)

X_long, y_long = create_sequences(df_long.values, target, SEQ_LENGTH)
X_recent, y_recent = create_sequences(df_recent.values, target, SEQ_LENGTH)

# 📌 모델 불러오기
model_long = tf.keras.models.load_model(LONG_MODEL_PATH)
model_recent = tf.keras.models.load_model(RECENT_MODEL_PATH)

# 📌 하이브리드 분할 기준
switch_index = int(len(X_long) * (1 - RECENT_RATIO))

# 📌 예측
y_pred_long = model_long.predict(X_long[:switch_index]).flatten()
y_pred_recent = model_recent.predict(X_recent[switch_index:]).flatten()

# 📌 실제 y값 동일하게 분리
y_true_long = y_long[:switch_index]
y_true_recent = y_recent[switch_index:]

# 📌 병합
y_pred_hybrid = np.concatenate([y_pred_long, y_pred_recent])
y_true = np.concatenate([y_true_long, y_true_recent])

# 📊 시각화
plt.figure(figsize=(10, 6))
plt.plot(y_true, label="Actual GDP", color="blue")
plt.plot(y_pred_hybrid, label="Hybrid Predicted GDP", linestyle="--", color="red")
plt.title("Hybrid GDP Prediction (Switching Strategy)")
plt.xlabel("Time")
plt.ylabel("GDP (Scaled)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
