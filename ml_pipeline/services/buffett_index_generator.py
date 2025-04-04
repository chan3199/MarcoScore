import pandas as pd

# 1. 데이터 로드
gdp_df = pd.read_csv("data/macro_data_gdp_full.csv", parse_dates=["date"])
pred_df = pd.read_csv("data/recent_gdp_prediction.csv", parse_dates=["date"])
wilshire_df = pd.read_csv("data/wilshire5000_yahoo_api.csv")

# ✅ 컬럼명 통일 및 datetime 변환
for df in [gdp_df, pred_df, wilshire_df]:
    if "Date" in df.columns:
        df.rename(columns={"Date": "date"}, inplace=True)
    if df["date"].dtype == object:
        df["date"] = pd.to_datetime(df["date"])

# 2. 예측 GDP 연결
gdp_cutoff = pd.to_datetime("2025-03-26")
gdp_df = gdp_df[gdp_df["date"] <= gdp_cutoff]
pred_df = pred_df.rename(columns={"gdp_predicted": "GDP"})
gdp_all = pd.concat([gdp_df, pred_df], ignore_index=True)
gdp_all = gdp_all.sort_values("date")

# 3. 일별로 확장 및 보간
gdp_all = gdp_all.set_index("date").resample("D").ffill().reset_index()

# 4. 버핏지수 계산
merged = pd.merge(wilshire_df, gdp_all, on="date", how="inner")
merged["buffett_index"] = merged["MarketCap"] / merged["GDP"]

# 5. 저장
merged[["date", "buffett_index"]].to_csv("data/buffett_index.csv", index=False)
print("✅ 버핏지수 CSV 저장 완료: data/buffett_index.csv")
