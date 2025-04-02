import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import tensorflow as tf

# 📌 데이터 불러오기
df = pd.read_csv("data/macro_data_scaled.csv", parse_dates=["date"])
df = df[df["date"].dt.year >= 1980]  # 🔍 1980년 이후만 사용
df = df.set_index("date")

drop_features = ["Consumer_Confidence", "CCI", "Initial_Jobless_Claims", "VIX", "USD_Index"]
# 🎯 타겟 및 피처 설정
target_col = "GDP"
# 👉 중복 지표 제거: "Consumer_Confidence"와 "CCI" 중 하나 제거

feature_cols = df.columns.drop([target_col] + drop_features)
print("Feature 개수:", len(feature_cols))  
# 📌 시계열 데이터셋 생성 함수
SEQ_LENGTH = 24  # ✅ 시계열 길이 증가
def create_sequences(data, target, seq_length=24):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(target[i+seq_length])
    return np.array(X), np.array(y)

X, y = create_sequences(df[feature_cols].values, df[target_col].values, SEQ_LENGTH)

# 📌 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

# ✅ 개선된 모델 정의 (Bidirectional LSTM 도입)
model = tf.keras.Sequential([
    tf.keras.layers.Bidirectional(
        tf.keras.layers.LSTM(128, return_sequences=True),
        input_shape=(SEQ_LENGTH, X.shape[2])
    ),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Bidirectional(
        tf.keras.layers.LSTM(64)
    ),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer="adam", loss="mse")

# 📌 학습
print("🚀 Training model...")
early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
history = model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=150,
    batch_size=32,
    callbacks=[early_stop]
)

# 📌 성능 평가
y_pred = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)
print(f"📉 RMSE: {rmse:.4f}")
print(f"📉 MAPE: {mape:.4f}")

# 📌 모델 저장
model.save("model/model_long.h5")
print("✅ Model saved to model/model_long.h5")
