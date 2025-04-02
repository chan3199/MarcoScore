import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# 📌 파일 경로
DATA_PATH = "data/macro_data_scaled.csv"
MODEL_LONG_PATH = "model/model_long.h5"
MODEL_RECENT_PATH = "model/model_recent.h5"

# 📌 파라미터
SEQ_LENGTH = 24
RECENT_RATIO = 0.2

# 📌 Feature 제거 기준
drop_long = ["CCI"]
drop_recent = ["Consumer_Confidence", "CCI", "Initial_Jobless_Claims", "VIX", "USD_Index"]
target_col = "GDP"

# 📌 시계열 변환 함수
def create_sequences(data, target, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(target[i+seq_length])
    return np.array(X), np.array(y)

# 📌 데이터 로드 및 분리
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df[df["date"].dt.year >= 1980].reset_index(drop=True)

target = df[target_col].values

# Long-term input
df_long = df.drop(columns=["date"] + drop_long)
X_long, y_long = create_sequences(df_long.values, target, SEQ_LENGTH)

# Recent input
df_recent = df.drop(columns=["date"] + drop_recent)
X_recent, y_recent = create_sequences(df_recent.values, target, SEQ_LENGTH)

# 최근 구간 테스트셋 분리
test_size = int(len(X_long) * RECENT_RATIO)
X_long_test, y_test = X_long[-test_size:], y_long[-test_size:]
X_recent_test = X_recent[-test_size:]

# 모델 로드
model_long = tf.keras.models.load_model(MODEL_LONG_PATH)
model_recent = tf.keras.models.load_model(MODEL_RECENT_PATH)

# 예측 수행
y_pred_long = model_long.predict(X_long_test).flatten()
y_pred_recent = model_recent.predict(X_recent_test).flatten()

# 하이브리드 예측
y_pred_hybrid = (y_pred_long + y_pred_recent) / 2

# 📊 시각화
plt.figure(figsize=(10, 6))
plt.plot(y_test, label="Actual GDP", color="blue")
plt.plot(y_pred_hybrid, label="Hybrid Predicted GDP", linestyle="--", color="red")
plt.title("Hybrid GDP Prediction (Fixed Test Set)")
plt.xlabel("Time")
plt.ylabel("GDP (Scaled)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
