import pandas as pd
from services.fetch_macro_data import merge_macro_data

# 데이터 불러오기
macro_data = merge_macro_data()

# 결측치 처리 (보간법 사용)
macro_data = macro_data.interpolate(method="linear")

# 로그 변환 (GDP, 소매판매 등 비율 변화가 중요한 데이터에 적용)
macro_data["GDP"] = macro_data["GDP"].apply(lambda x: x if x > 0 else None).dropna()
macro_data["log_GDP"] = macro_data["GDP"].apply(lambda x: np.log(x))

# 데이터 저장
macro_data.to_csv("ml_pipeline/processed_macro_data.csv", index=False)
print("✅ 데이터 전처리 완료. 저장됨: `ml_pipeline/processed_macro_data.csv`")
