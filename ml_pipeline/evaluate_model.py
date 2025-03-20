import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import matplotlib.pyplot as plt

# 📌 데이터 불러오기
df_scaled = pd.read_csv("data/macro_data_scaled.csv", parse_dates=["date"], index_col="date")

# 📌 모델 불러오기
model = tf.keras.models.load_model("model/gdp_predictor.h5")

# 📌 입력 데이터 준비
SEQ_LENGTH = 12
X = []
y = df_scaled["GDP"].values

for i in range(len(y) - SEQ_LENGTH):
    X.append(df_scaled.values[i:i+SEQ_LENGTH])

X = np.array(X)

# 📌 예측 수행
y_pred = model.predict(X)

# 📌 성능 평가
rmse = np.sqrt(mean_squared_error(y[SEQ_LENGTH:], y_pred))
mape = mean_absolute_percentage_error(y[SEQ_LENGTH:], y_pred) * 100

print(f"📉 RMSE: {rmse:.5f}")
print(f"📉 MAPE: {mape:.2f}%")

# 📌 예측 결과 시각화
plt.figure(figsize=(10, 6))
plt.plot(y[SEQ_LENGTH:], label="Actual GDP", color="blue")
plt.plot(y_pred, label="Predicted GDP", linestyle="dashed", color="red")
plt.xlabel("Time")
plt.ylabel("GDP (scaled)")
plt.title("GDP Prediction: Actual vs Predicted")
plt.legend()
plt.show()
