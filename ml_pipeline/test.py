import pandas as pd

df = pd.read_csv("data/macro_data_scaled.csv")
print("🔍 결측값 존재 여부:\n", df.isnull().sum())
print("\n📊 데이터 요약:\n", df.describe())