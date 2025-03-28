import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import tensorflow as tf

# 설정
SEQ_LENGTH = 24
TARGET_COL = "GDP"
REMOVE_COLS = ["Consumer_Confidence", "CCI", "Initial_Jobless_Claims", "VIX", "USD_Index"]  # ❗ train_model.py와 동일하게 제거
MODEL_PATH = "model/gdp_predictor.h5"
DATA_PATH = "data/macro_data_scaled.csv"

# 📌 데이터 불러오기
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df[df["date"].dt.year >= 1980].set_index("date")

# 🎯 타겟 및 피처 설정
feature_cols = df.columns.drop([TARGET_COL] + REMOVE_COLS)

# 📌 시계열 데이터셋 생성
def create_sequences(data, target, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(target[i+seq_length])
    return np.array(X), np.array(y)

X, y = create_sequences(df[feature_cols].values, df[TARGET_COL].values, SEQ_LENGTH)

# 📌 모델 로드 및 예측
model = tf.keras.models.load_model(MODEL_PATH)
y_pred = model.predict(X).flatten()

# 📊 성능 평가
rmse = np.sqrt(mean_squared_error(y, y_pred))
mape = mean_absolute_percentage_error(y, y_pred)
print(f"📉 RMSE: {rmse:.4f}")
print(f"📉 MAPE: {mape:.4f}")

# 📈 시각화
plt.figure(figsize=(10, 6))
plt.plot(y, label="Actual GDP", color="blue")
plt.plot(y_pred, label="Predicted GDP", color="red", linestyle="--")
plt.title("GDP Prediction: Actual vs Predicted (Scaled)")
plt.xlabel("Time")
plt.ylabel("GDP (Scaled)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
