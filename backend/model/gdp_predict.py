import joblib
import pandas as pd
from services.fetch_macro_data import merge_macro_data

# 모델 로드
model_path = "backend/models/gdp_model.pkl"
model = joblib.load(model_path)

# 최신 경제 데이터를 기반으로 GDP 예측
def predict_gdp():
    latest_data = merge_macro_data().iloc[-1]  # 최신 데이터 가져오기
    features = ["Retail_Sales", "ISM_PMI", "Unemployment", "SP500"]
    input_data = latest_data[features].values.reshape(1, -1)

    # 예측 수행
    log_gdp_pred = model.predict(input_data)[0]
    gdp_pred = round(np.exp(log_gdp_pred), 2)  # 로그 변환 되돌리기

    return {"date": latest_data["date"], "predicted_gdp": gdp_pred}

if __name__ == "__main__":
    print("📊 GDP 예측 결과:", predict_gdp())
