# 📊 MacroScore: 거시 경제 기반 투자 적절성 분석 플랫폼

![MacroScore Logo](./public/logo.png)

**MacroScore**는 거시경제 지표와 예측 모델을 기반으로 미국 증시에 대한 투자 판단을 도와주는 시각화 플랫폼입니다. 감정적인 매매를 줄이고, 데이터 기반으로 시장을 이해하여 전략적 투자를 실현할 수 있도록 돕습니다.

---

## 🧠 프로젝트 개요

### 🔍 기획 배경
- S&P500 등 미국 증시 장기 투자에 대한 관심 증가
- 단순 적립식 투자 → 경제 사이클을 반영한 **유연한 투자 전략** 필요
- 거시지표(GDP, 금리, 실업률 등)를 바탕으로 투자 적절성 지수 제공

### 🎯 목표
- 경제지표 및 밸류에이션 지표를 종합하여 투자 타이밍 분석
- **GDP 예측 모델**을 기반으로 선행지표 활용
- 직관적인 대시보드로 누구나 쉽게 투자 환경 파악 가능

---

## 🚀 핵심 기능

### ✅ 거시경제 기반 투자 분석
- GDP, 금리, 실업률, 소비지출, 통화량 등 핵심 지표 제공
- SPY 시가총액 기반 **버핏지수** 시계열 차트 구현
- FRED API 기반 실시간 지표 자동 업데이트

### ✅ GDP 예측 모델 탑재
- LSTM + Bidirectional LSTM 기반 **딥러닝 시계열 예측 모델**
- FRED와 Yahoo Finance 데이터를 활용한 실험적 GDP 예측
- RMSE / MAPE 평가 지표 기반 성능 검증

### ✅ 대시보드 UI
- 차트 기반 시각화 (Chart.js)
- 기간 선택 (1년, 3년, 10년 등)
- 지표별 변화 추세 비교 가능

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| 프론트엔드 | React (Vite) + TypeScript + Tailwind CSS + Chart.js |
| 백엔드 | Node.js (Express) + SQLite + REST API |
| 머신러닝 | Python, TensorFlow, Scikit-learn |
| 데이터 수집 | FRED API, FMP API |
| 배포 | Netlify (FE) + Render (BE), Docker (개발 환경) |
| CI/CD | GitHub Actions, Webhook, Docker Compose |

---

## 📂 프로젝트 구조

```bash
MacroScore/ ├── frontend/ # React 기반 대시보드 ├── backend/ # Node.js API 서버 ├── ml_pipeline/ # GDP 예측 모델 및 전처리 │ ├── fetch_fred_data.py │ ├── fetch_macro_data.py │ ├── preprocess.py │ ├── train_model.py │ ├── evaluate_model.py │ └── model/ │ └── gdp_predictor.h5 ├── data/ │ └── macro_data.csv ├── .env └── README.md
```

---

## 📈 모델 평가 결과

- **LSTM 기반 예측 RMSE**: 약 *0.014*
- **MAPE**: 약 *1.1%*
- 주요 개선점:
  - CCI/중복 변수 제거
  - 시계열 길이 확대 (12 → 24개월)
  - Bidirectional LSTM 구조로 성능 향상

> 향후 Prophet, XGBoost, LightGBM 등 추가 적용 가능

---

## 📌 향후 개발 계획

- ✅ GDP 예측 성능 고도화 (Ensemble, Feature Selection 등)
- ✅ 종합 투자지수 계산 (예측 기반)
- ⏳ 자동 리밸런싱 시뮬레이션 기능 개발
- ⏳ 브로커 API 연동 (매수 자동화)
- ⏳ 유저 커스터마이징 기능 (이메일 알림, 자산 설정 등)

---

## 📎 참고 및 데이터 출처

- [FRED Economic Data](https://fred.stlouisfed.org/)
- [Financial Modeling Prep API](https://financialmodelingprep.com/)
- [Yahoo Finance](https://finance.yahoo.com/)
- [TensorFlow Documentation](https://www.tensorflow.org/)

---

## 🧑‍💻 개발자 메모

> MacroScore는 단순히 지표를 나열하는 서비스가 아니라, 경제 데이터의 흐름을 해석하고 **데이터 기반 투자 사고**를 도와주는 프로젝트입니다.  
실험적인 시도가 많았지만, 실제로 예측 모델을 학습시키고 평가까지 진행한 의미 있는 도전이었습니다.

---
