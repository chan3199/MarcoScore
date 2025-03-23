import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler

# 📌 데이터 불러오기
data = pd.read_csv("data/macro_data.csv", parse_dates=["date"], index_col="date")

# 📌 NaN 및 Inf 값 처리
data = data.replace([np.inf, -np.inf], np.nan)  # 무한대 값 제거
data = data.dropna()  # 남은 결측값 제거

# 📌 결측치 보간
data = data.interpolate(method="linear")

# 📌 데이터 스케일링 (RobustScaler 사용)
scaler = RobustScaler()
data_scaled = scaler.fit_transform(data)

# 📌 스케일링된 데이터 저장
df_scaled = pd.DataFrame(data_scaled, columns=data.columns, index=data.index)
df_scaled.to_csv("data/macro_data_scaled.csv")
print("✅ Scaled data saved as macro_data_scaled.csv")
