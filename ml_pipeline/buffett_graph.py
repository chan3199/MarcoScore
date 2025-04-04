import pandas as pd
import matplotlib.pyplot as plt

# 1. 데이터 로딩
gdp_df = pd.read_csv("data/macro_data_gdp_full.csv", parse_dates=["date"])
pred_df = pd.read_csv("data/recent_gdp_prediction.csv", parse_dates=["date"])
wilshire_df = pd.read_csv("data/wilshire5000_yahoo_api.csv", parse_dates=["date"])

# 2. 예측 GDP를 실제 GDP 뒤에 이어붙이기
gdp_cutoff = pd.to_datetime("2025-03-26")
gdp_df = gdp_df[gdp_df["date"] <= gdp_cutoff]
pred_df = pred_df.rename(columns={"gdp_predicted": "GDP"})
gdp_all = pd.concat([gdp_df, pred_df], ignore_index=True)

# 3. 최근 GDP 기준으로 보간 확장
# 가장 마지막 GDP 날짜부터 그 다음 발표 전까지 보간용 값 생성
gdp_all = gdp_all.sort_values("date")
gdp_all = gdp_all.set_index("date").resample("D").ffill().reset_index()  # 일별로 확장

# 4. 버핏지수 계산
merged = pd.merge(wilshire_df, gdp_all, on="date", how="inner")
merged["buffett_index"] = merged["MarketCap"] / merged["GDP"]

# 5. 시각화
plt.figure(figsize=(12, 6))
plt.plot(merged["date"], merged["buffett_index"], color="darkred", label="Buffett Index")
plt.axhline(1.0, color="gray", linestyle="--", label="Fair Value (1.0)")
plt.title("📈 Buffett Index Over Time")
plt.xlabel("Date")
plt.ylabel("Buffett Index")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
