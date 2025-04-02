import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import tensorflow as tf
import os
import matplotlib.pyplot as plt

# 📌 경로 설정
DATA_PATH = "data/macro_data_scaled.csv"
SAVE_PATH = "model/model_recent_v2.h5"
SEQ_LENGTH = 24

# 📌 데이터 불러오기 (최근 데이터 위주)
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df[df["date"] >= "2005-01-01"].reset_index(drop=True)

# 📌 Feature 설정
target_col = "GDP"
REMOVE_COLS = ["USD_Index", "CCI","M2_Money_Supply"]
feature_cols = df.columns.drop(["date", target_col] + REMOVE_COLS)

# 📌 시계열 시퀀스 생성 함수
def create_sequences(data, target, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(target[i+seq_length])
    return np.array(X), np.array(y)

X, y = create_sequences(df[feature_cols].values, df[target_col].values, SEQ_LENGTH)
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

# 📌 모델 정의 (최근 데이터에 맞춘 소형 모델)
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, return_sequences=True, input_shape=(SEQ_LENGTH, X.shape[2])),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(32),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer="adam", loss="mse")

# 📌 학습
early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
model.fit(X_train, y_train,
          validation_data=(X_test, y_test),
          epochs=150,
          batch_size=16,
          callbacks=[early_stop],
          verbose=1)

# 📌 예측 및 성능 출력
y_pred = model.predict(X_test).flatten()
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)
print(f"📉 RMSE: {rmse:.4f}")
print(f"📉 MAPE: {mape:.4f}")

# 📌 모델 저장
os.makedirs("model", exist_ok=True)
model.save(SAVE_PATH)
print(f"✅ Saved to {SAVE_PATH}")

# 📈 시각화
plt.figure(figsize=(10, 6))
plt.plot(y_test, label="Actual GDP", color="blue")
plt.plot(y_pred, label="Predicted GDP (Recent v2)", linestyle="--", color="red")
plt.title("Recent GDP Prediction (Recent v2 Model)")
plt.xlabel("Time")
plt.ylabel("GDP (scaled)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
