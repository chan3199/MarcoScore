from ml_pipeline.fetch.fetch_macro_data import run_macro_fetch
from ml_pipeline.processing.preprocess import run_preprocessing
from ml_pipeline.training.long_train_model import run_training
from ml_pipeline.training.long_evaluate_model import run_evaluation
from ml_pipeline.prediction.recent_gdp_prediction import run_prediction
from ml_pipeline.prediction.correct_gdp import run_auto_correction
from ml_pipeline.buffett.buffett_index_generator import run_buffetSaveCsv
from ml_pipeline.utils.wait_for_file import wait_for_file

def main():
    print ("step 1: 데이터 수집 !")
    run_macro_fetch()

    print("Step 2: 데이터 전처리")
    run_preprocessing()

    print("Step 3: 모델 학습")
    run_training()

    print("Step 4: 모델 평가")
    run_evaluation()

    print("Step 5: GDP 예측")
    run_prediction()

    print("Step 6: 예측 자동 보정")
    run_auto_correction()

    print("step 7: 버핏지수 CSV 저장")
    run_buffetSaveCsv()

    print("전체 파이프라인 완료!")

if __name__ == "__main__":
    main()
