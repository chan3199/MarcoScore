import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# 📌 데이터 불러오기
data = pd.read_csv("data/macro_data.csv", parse_dates=["date"], index_col="date")

# 📌 최근 30년 데이터만 사용 (1990년 이후)
data = data.loc["1990-01-01":]

# 📌 NaN 데이터 확인
print("🔍 결측치 개수:\n", data.isna().sum())

# 📌 결측치 보간 (선형 보간 + 마지막 값으로 채우기)
data = data.interpolate(method="linear")
data = data.fillna(method="bfill").fillna(method="ffill")

# 📌 스케일링 (확인용)
print("📊 정규화 전 GDP 통계:\n", data["GDP"].describe())

# 📌 MinMaxScaler (-1 ~ 1 범위로 조정)
scaler = MinMaxScaler(feature_range=(-1, 1))
data_scaled = scaler.fit_transform(data)
df_scaled = pd.DataFrame(data_scaled, columns=data.columns, index=data.index)

# 📌 정규화 확인
print("📊 정규화 후 GDP 통계:\n", df_scaled["GDP"].describe())

# 📌 저장
df_scaled.to_csv("data/macro_data_scaled.csv")
print("✅ Preprocessing complete. Data saved.")
