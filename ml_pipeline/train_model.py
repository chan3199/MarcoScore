import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler

# 📌 데이터 불러오기 (스케일링된 데이터 사용)
data = pd.read_csv("data/macro_data_scaled.csv", parse_dates=["date"], index_col="date")

# 🎯 시계열 데이터셋 생성 함수
def create_sequences(data, target, seq_length=24):  # 👈 12 → 24개월로 증가
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(target[i + seq_length])
    return np.array(X), np.array(y)

# 🎯 입력 및 타겟 설정
SEQ_LENGTH = 24  # 👈 12개월 → 24개월로 변경
X, y = create_sequences(data.values, data["GDP"].values, SEQ_LENGTH)

# 📌 데이터셋 분할 (시계열 데이터이므로 shuffle=False)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 📌 LSTM 모델 구축 (레이어 수 증가 및 학습률 변경)
print("🔧 Building LSTM model...")
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(128, return_sequences=True, input_shape=(SEQ_LENGTH, X.shape[2])),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.LSTM(64, return_sequences=True),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.LSTM(32, return_sequences=False),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.2),
    
    tf.keras.layers.Dense(1)
])

# 📌 Adam Optimizer 개선 (학습률 조정)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.002)  # 👈 0.001 → 0.002 로 증가
model.compile(optimizer=optimizer, loss="mse")

# 📌 Early Stopping 추가
early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=20, restore_best_weights=True)

# 📌 모델 학습
print("🚀 Training model...")
history = model.fit(
    X_train, y_train,
    epochs=500, batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[early_stopping]
)

# 📌 모델 저장
model.save("model/gdp_predictor.h5")
print("✅ Model training complete!")


# 📌 원래 단위로 역변환 (데이터 복원)
scaler = RobustScaler()
scaler.fit(X_train)
# 🎯 예측 수행
y_pred = model.predict(X_test)

# 🎯 예측값을 원래 단위(GDP 값)로 변환
y_pred_rescaled = scaler.inverse_transform(np.concatenate([np.zeros((y_pred.shape[0], data.shape[1] - 1)), y_pred], axis=1))[:, -1]

# 🎯 저장
np.save("data/y_test.npy", y_test)
np.save("data/y_pred.npy", y_pred_rescaled)  # ✅ 변환된 값 저장

