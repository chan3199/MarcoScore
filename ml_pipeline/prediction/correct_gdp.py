import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import matplotlib.pyplot as plt

# 설정
SEQ_LENGTH = 24
N_RECENT = 4
MODEL_PATH = "model/model_long.h5"
SCALER_PATH = "models/scaler_gdp.pkl"
DATA_PATH = "data/macro_data_scaled.csv"
TARGET_COL = "GDP"
DROP_FEATURES = ["Consumer_Confidence", "CCI", "Initial_Jobless_Claims", "M2_Money_Supply", "VIX", "USD_Index"]

# 데이터 로드
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df[df["date"].dt.year >= 1980].reset_index(drop=True).set_index("date")

# 피처 추출
feature_cols = df.columns.drop([TARGET_COL] + DROP_FEATURES)
X_data = df[feature_cols].values
y_data = df[TARGET_COL].values

# 시계열 시퀀스 생성
def create_sequences(data, target, seq_length):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(target[i + seq_length])
    return np.array(X), np.array(y)

X, y = create_sequences(X_data, y_data, SEQ_LENGTH)

# 모델 및 스케일러 불러오기
model = tf.keras.models.load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# 전체 예측
y_pred_raw = model.predict(X).flatten()

# 보정: 최근 n개 기준
correction_factor = np.mean(y[-N_RECENT:] / y_pred_raw[-N_RECENT:])
y_pred_adjusted = y_pred_raw * correction_factor

# ✅ 최종 예측: 평균 기반
y_pred_final = (y_pred_raw + y_pred_adjusted) / 2

# 다음 분기 예측
prediction_dates = df.index[SEQ_LENGTH:]
recent_date = prediction_dates[-1]
next_quarter_date = recent_date + pd.DateOffset(months=3)
next_input = X[-1].reshape(1, SEQ_LENGTH, -1)

next_pred_raw = model.predict(next_input).flatten()[0]
next_pred_adjusted = next_pred_raw * correction_factor
next_pred_final = (next_pred_raw + next_pred_adjusted) / 2
next_pred_real = scaler.inverse_transform([[next_pred_final]])[0][0]

# CSV 저장
recent_df = pd.DataFrame({
    "date": [next_quarter_date],
    "gdp_predicted": [next_pred_real]
})
recent_df.to_csv("data/recent_gdp_prediction.csv", index=False)
print("✅ 다음 분기 예측값이 저장되었습니다:", next_pred_real)

# 시각화
plt.figure(figsize=(10, 6))
plt.plot(y, label="Actual GDP", color="blue")
plt.plot(y_pred_raw, label="Predicted GDP (Raw)", linestyle="--", color="red")
plt.plot(y_pred_adjusted, label="Predicted GDP (Adjusted)", linestyle="--", color="green")
plt.plot(y_pred_final, label="Predicted GDP (Final Avg)", linestyle=":", color="purple")
plt.title("GDP Prediction with Auto-Correction (Final Avg)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
