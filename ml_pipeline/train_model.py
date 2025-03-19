import pandas as pd
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# 데이터 불러오기
data = pd.read_csv("ml_pipeline/processed_macro_data.csv")

# 특징(Feature)과 타겟 변수 정의
features = ["Retail_Sales", "ISM_PMI", "Unemployment", "SP500"]
target = "log_GDP"

X = data[features]
y = data[target]

# 훈련 및 테스트 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost 모델 학습
model = xgb.XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5)
model.fit(X_train, y_train)

# 예측 및 성능 평가
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
print(f"📉 모델 평가 - MAE: {mae:.4f}")

# 모델 저장
joblib.dump(model, "backend/models/gdp_model.pkl")
print("✅ 모델 저장 완료: `backend/models/gdp_model.pkl`")
