import os

# 프로젝트 루트 디렉토리 (run_pipeline.py가 있는 상위 디렉토리 기준)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# 주요 경로
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")
OUTPUT_DIR = os.path.join(BASE_DIR, "backend", "src", "data") 

# 주요 파일 경로
MACRO_DATA_RAW_PATH = os.path.join(DATA_DIR, "macro_data.csv")
MACRO_DATA_SCALED_PATH = os.path.join(DATA_DIR, "macro_data_scaled.csv")
GDP_FULL_PATH = os.path.join(DATA_DIR, "macro_data_gdp_full.csv")
RECENT_PREDICTION_PATH = os.path.join(DATA_DIR, "recent_gdp_prediction.csv")
WILSHIRE_PATH = os.path.join(DATA_DIR, "wilshire5000_yahoo_api.csv")
BUFFETT_INDEX_PATH = os.path.join(OUTPUT_DIR, "buffett_index.csv")

# 모델 저장 경로
MODEL_LONG_PATH = os.path.join(MODEL_DIR, "model_long.h5")
SCALER_PATH = os.path.join(BASE_DIR, "models", "scaler_gdp.pkl")
