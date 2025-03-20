import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf

# 📌 데이터 불러오기
data = pd.read_csv("data/macro_data.csv", parse_dates=["date"], index_col="date")

# 📌 결측치 보간
print("🛠 Filling missing values...")
data = data.interpolate(method="linear")

# 📌 데이터 스케일링
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)
df_scaled = pd.DataFrame(data_scaled, columns=data.columns, index=data.index)

# 📌 GDP 타겟 컬럼 인덱스 찾기
target_index = list(data.columns).index("GDP")

# 📌 시계열 데이터셋 생성 함수
def create_sequences(data, target_index, seq_length=12):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length, target_index])  # GDP 데이터만 가져옴
    return np.array(X), np.array(y)

# 🎯 입력 및 타겟 설정
SEQ_LENGTH = 12  # 12개월 데이터 사용
X, y = create_sequences(df_scaled.values, target_index, SEQ_LENGTH)

# 📌 데이터셋 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# 📌 LSTM 모델 구축
print("🔧 Building LSTM model...")
model = tf.keras.models.Sequential([
    tf.keras.layers.LSTM(100, return_sequences=True, input_shape=(SEQ_LENGTH, X.shape[2])),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.LSTM(50, return_sequences=False),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1)
])

model.compile(optimizer='adam', loss='mse')

# 📌 EarlyStopping & ReduceLROnPlateau 추가 (학습 최적화)
early_stopping = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=5, min_lr=1e-5)

# 📌 모델 학습
print("🚀 Training model...")
history = model.fit(
    X_train, y_train, 
    epochs=50, 
    batch_size=16, 
    validation_data=(X_test, y_test),
    callbacks=[early_stopping, reduce_lr]  # 최적화 콜백 추가
)

# 📌 모델 저장
model.save("../model/gdp_predictor.h5")
print("✅ Model training complete!")
