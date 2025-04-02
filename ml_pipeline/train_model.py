import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import tensorflow as tf

# 📌 하이퍼파라미터
SEQ_LENGTH = 24
TEST_SIZE = 1200  # 최근 1200개 샘플을 테스트셋으로 사용

# 📌 데이터 로딩
df = pd.read_csv("data/macro_data_scaled.csv", parse_dates=["date"])
df = df[df["date"].dt.year >= 1980].reset_index(drop=True)
df = df.set_index("date")

# 🎯 타겟 및 피처
target_col = "GDP"
feature_cols = df.columns.drop([target_col, "CCI"])  # 중복 제거
print("Feature 개수:", len(feature_cols))  
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

# 📌 최근 데이터를 테스트셋으로 고정 분할
X_train, X_test = X_seq[:-TEST_SIZE], X_seq[-TEST_SIZE:]
y_train, y_test = y_seq[:-TEST_SIZE], y_seq[-TEST_SIZE:]

# ✅ 모델 정의: 단순 BiLSTM 구조
model = tf.keras.Sequential([
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=False), input_shape=(SEQ_LENGTH, X_seq.shape[2])),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1)
])
model.compile(optimizer="adam", loss="mse")

# 📌 학습
print("🚀 Training model...")
early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=100,
    batch_size=32,
    callbacks=[early_stop],
    verbose=1
)

# 📉 평가
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)
print(f"📉 RMSE: {rmse:.4f}")
print(f"📉 MAPE: {mape:.4f}")

# 📁 저장
model.save("model/model_recent.h5")
print("✅ Model saved to model/gdp_predictor.h5")
