import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

# 📌 데이터 불러오기
data = pd.read_csv("data/macro_data_scaled.csv", parse_dates=["date"], index_col="date")

# 📌 NaN 값이 있는지 확인
print("🔍 데이터 결측치 확인:\n", data.isna().sum())

# 📌 시계열 데이터셋 생성
def create_sequences(data, target, seq_length=12):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(target[i+seq_length])
    return np.array(X), np.array(y)

# 🎯 입력 및 타겟 설정
SEQ_LENGTH = 12
X, y = create_sequences(data.values, data["GDP"].values, SEQ_LENGTH)

# 📌 NaN 또는 Inf 값 제거
X = np.nan_to_num(X, nan=0.0, posinf=1.0, neginf=-1.0)
y = np.nan_to_num(y, nan=0.0, posinf=1.0, neginf=-1.0)

# 📌 데이터셋 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 📌 LSTM 모델 구축 (학습 안정화)
print("🔧 Building LSTM model...")
model = tf.keras.models.Sequential([
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True, input_shape=(SEQ_LENGTH, X.shape[2]), recurrent_dropout=0.2)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True, recurrent_dropout=0.2)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32, return_sequences=False, recurrent_dropout=0.2)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(1, activation='linear', kernel_regularizer=tf.keras.regularizers.l2(0.01))
])

# 📌 Adam Optimizer (학습률 감소)
optimizer = tf.keras.optimizers.Adam(learning_rate=0.0005)
model.compile(optimizer=optimizer, loss='mse')

# 📌 Early Stopping 추가
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=15,  # 더 오래 기다리기
    restore_best_weights=True
)

# 📌 모델 학습
print("🚀 Training model...")
history = model.fit(
    X_train, y_train,
    epochs=200, batch_size=32,
    validation_data=(X_test, y_test),
    callbacks=[early_stopping]
)

# 📌 모델 저장
model.save("model/gdp_predictor.h5")
print("✅ Model training complete!")
