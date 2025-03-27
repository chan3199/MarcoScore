import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

# 📌 설정
SEQ_LENGTH = 24
target_col = "GDP"

# 📌 데이터 불러오기
df = pd.read_csv("data/macro_data_scaled.csv", parse_dates=["date"])
df = df[df["date"].dt.year >= 1980]
df = df.set_index("date")

# 📌 중복 지표 제거 (train_model.py와 동일하게!)
feature_cols = df.columns.drop([target_col, "CCI"])

# 📌 시계열 데이터셋 생성 함수
def create_sequences(data, target, seq_length=24):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(target[i+seq_length])
    return np.array(X), np.array(y)

X, y = create_sequences(df[feature_cols].values, df[target_col].values, SEQ_LENGTH)

# 📌 훈련/테스트 분리
split_idx = int(len(X) * 0.8)
X_train, X_test = X[:split_idx], X[split_idx:]
y_train, y_test = y[:split_idx], y[split_idx:]

# 📌 모델 불러오기
model = tf.keras.models.load_model("model/gdp_predictor.h5")

# 📌 예측
y_pred = model.predict(X_test).flatten()

# 📌 평가
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)
print(f"✅ RMSE: {rmse:.4f}")
print(f"✅ MAPE: {mape:.4f}")

# 📊 시각화
plt.figure(figsize=(10, 6))
plt.plot(y_test, label="Actual GDP", color="blue")
plt.plot(y_pred, label="Predicted GDP", color="red", linestyle="--")
plt.title("GDP Prediction: Actual vs Predicted (Scaled)")
plt.xlabel("Time")
plt.ylabel("GDP (Scaled)")
plt.legend()
plt.grid(True)
plt.show()
