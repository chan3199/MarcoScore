import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import joblib

# 📌 하이퍼파라미터
SEQ_LENGTH = 24
TEST_SIZE = 1200

# 📌 데이터 로딩
df = pd.read_csv("data/macro_data_scaled.csv", parse_dates=["date"])
df = df[df["date"].dt.year >= 1980].reset_index(drop=True)
df = df.set_index("date")

target_col = "GDP"
feature_cols = df.columns.drop([target_col, "CCI"])  # 중복 제거
X_raw = df[feature_cols].values
y_raw = df[target_col].values

# 📌 시계열 데이터 생성
def create_sequences(X, y, seq_length):
    X_seq, y_seq = [], []
    for i in range(len(X) - seq_length):
        X_seq.append(X[i:i+seq_length])
        y_seq.append(y[i+seq_length])
    return np.array(X_seq), np.array(y_seq)

X_seq, y_seq = create_sequences(X_raw, y_raw, SEQ_LENGTH)

# 📌 최근 구간을 테스트셋으로 고정
X_test = X_seq[-TEST_SIZE:]
y_test = y_seq[-TEST_SIZE:]

# 📌 모델 로딩
model = tf.keras.models.load_model("model/model_recent.h5")

# 📌 예측
y_pred = model.predict(X_test).flatten()

# 📌 시각화
plt.figure(figsize=(10, 6))
plt.plot(y_test, label="Actual GDP", color="blue")
plt.plot(y_pred, label="Predicted GDP", linestyle="--", color="red")
plt.title("Recent GDP Prediction (Fixed Test Set)")
plt.xlabel("Time")
plt.ylabel("GDP (Scaled)")
plt.legend()
plt.grid(True)
plt.show()

# 📉 평가 지표 출력
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)
print(f"📉 RMSE: {rmse:.4f}")
print(f"📉 MAPE: {mape:.4f}")
