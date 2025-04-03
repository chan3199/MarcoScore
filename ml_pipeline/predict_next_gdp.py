import pandas as pd
import numpy as np
import tensorflow as tf
from datetime import datetime

# 설정
MODEL_PATH = "model/model_long.h5"
DATA_PATH = "data/macro_data_scaled.csv"
SEQ_LENGTH = 24
DROP_FEATURES = ["Consumer_Confidence", "CCI", "Initial_Jobless_Claims","M2_Money_Supply", "VIX", "USD_Index"]
TARGET_COL = "GDP"

# 데이터 불러오기
df = pd.read_csv(DATA_PATH, parse_dates=["date"])
df = df[df["date"].dt.year >= 1980]
df = df.set_index("date")

# 피처 컬럼 설정
feature_cols = df.columns.drop([TARGET_COL] + DROP_FEATURES)

# 가장 최신 시계열 구간 추출
latest_seq = df[feature_cols].values[-SEQ_LENGTH:]
X_input = np.expand_dims(latest_seq, axis=0)  # (1, 24, num_features)

# 모델 불러오기
model = tf.keras.models.load_model(MODEL_PATH)

# 예측
predicted_gdp = model.predict(X_input).flatten()[0]

# 결과 출력
latest_date = df.index[-1]
next_quarter = latest_date + pd.DateOffset(months=3)
print("📈 Latest Data:", latest_date.date())
print("📅 Predicted Next GDP Date:", next_quarter.date())
print("🔮 Predicted Next Quarter GDP (Scaled):", round(predicted_gdp, 4))
