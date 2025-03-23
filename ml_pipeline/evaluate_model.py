import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

# 📌 저장된 테스트 데이터 및 예측값 불러오기
y_test = np.load("data/y_test.npy")
y_pred = np.load("data/y_pred.npy")

# 📌 성능 평가 (RMSE, MAPE)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = mean_absolute_percentage_error(y_test, y_pred)

print(f"📊 RMSE: {rmse:.5f}")
print(f"📊 MAPE: {mape:.5f}")

# 📊 결과 시각화 (예측값과 실제값 비교)
plt.figure(figsize=(10, 6))
plt.plot(y_test, label="Actual GDP", color="blue")
plt.plot(y_pred, label="Predicted GDP", color="red", linestyle="dashed")
plt.xlabel("Time")
plt.ylabel("GDP")
plt.title("GDP Prediction: Actual vs Predicted")
plt.legend()
plt.show()
