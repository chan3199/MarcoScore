import pandas as pd

def gdpExtract():
    # 원본 macro_data.csv 로드
    df = pd.read_csv("ml_pipeline/data/macro_data.csv", parse_dates=["date"])

    # GDP만 추출해서 저장
    df_gdp = df[["date", "GDP"]].dropna().copy()

    # 1980년 이후만 사용
    df_gdp = df_gdp[df_gdp["date"].dt.year >= 1980]

    # 정렬 보장
    df_gdp = df_gdp.sort_values("date").reset_index(drop=True)

    # 저장
    df_gdp.to_csv("ml_pipeline/data/macro_data_gdp_full.csv", index=False)

    print("gdp 추출 !")

if __name__ == "__main__":
    gdpExtract()
