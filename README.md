# MacroScore: 거시경제 기반 투자 도움 서비스 

MacroScore는 미국 증시의 장기 투자 시점을 거시경제 데이터를 통해 판단하는 실험적 투자 보조 플랫폼입니다. 감정적인 매매, 계획없는 적립식 매매 등을 지양하고 데이터를 바탕으로 투자 전략을 세울 수 있도록 돕는 것을 목표로 함.

---

## 1. 프로젝트 개요

### 1.1 기획 배경

- 미국 증시에 대한 적립식 투자 관심 증가
- 단순 DCA 전략을 넘어, 경제 사이클에 따라 투자 비중을 조절할 수 있는 방법 모색
- 거시경제 지표와 시가총액 기반의 평가 지표(예: 버핏 지수)를 통해 데이터 기반의 투자 타이밍 판단 도구 개발

### 1.2 목표

- 주요 경제 지표 시계열화 및 실시간 시각화
- LSTM 기반 GDP 예측 모델 구축 및 실험적 예측
- 예측 GDP와 실시간 시가총액을 활용한 **버핏 지수** 동적 계산

---

## 2. 핵심 기능

### 2.1 거시경제 기반 분석

- FRED API 기반: 금리, 실업률, 통화량, 소비 등 주요 지표 수집
- 경제 데이터 정규화 및 시계열 구성
- 시각화를 통해 지표 흐름 확인 가능

### 2.2 GDP 예측 모델

- LSTM + Bidirectional LSTM 기반 예측 구조
- 시계열 길이 확장 및 중복 변수 제거로 성능 향상
- 최근 데이터 중심으로 보정된 예측값 반영
- 발표되지 않은 미래 GDP 예측값을 활용한 버핏지수 계산 및 다른 지표에 활용

### 2.3 버핏지수 시계열 분석

- Wilshire 5000 시가총액 / 미국 GDP
- 발표된 GDP는 실제 값을 사용하고, 발표되지 않은 구간은 모델 예측값으로 대체
- 일 단위 시계열로 보간 처리하여 시계열 추적 가능
- Plotly.js를 통한 웹 기반 시각화 구현 (React)

### 2.4 버핏지수 및 거시경제 지표 기반 지수 도출
- 여러 거시적 지표를 활용해 신뢰할 수 있는 투자 참고 지수를 도출하는 것이 목표
- 정확성을 높히기 위한 다양한 실험 요
- 위험성이 높은 단기 수익 투자 구조보다는 장기적으로 참고할 수 있는 지수를 도출하는 것

---

## 3. 기술 스택

| 분류        | 기술                                       |
|-------------|--------------------------------------------|
| 프론트엔드  | React (Vite), TypeScript, Plotly.js        |
| 백엔드      | Node.js (Express), SQLite, REST API        |
| 머신러닝    | Python, TensorFlow, Scikit-learn            |
| 데이터 수집 | FRED API, Yahoo Finance (yfinance)         |
| 인프라      | Docker, Netlify, Render, GitHub Actions    |

---

## 4. 프로젝트 구조
```bash
MacroScore/
├── frontend/ # 대시보드 React 프로젝트
│ └── public/data/ # Plotly용 CSV 데이터 (버핏지수 등)
├── backend/ # REST API (향후 확장 예정)
├── ml_pipeline/ # 머신러닝 파이프라인
│ ├── fetch_macro_data.py
│ ├── train_model.py
│ ├── evaluate_model.py
│ ├── correct_gdp.py
│ └── buffett_index_generator.py
├── data/
│ ├── macro_data.csv
│ ├── macro_data_scaled.csv
│ ├── recent_gdp_prediction.csv
│ ├── wilshire5000_yahoo_api.csv
│ └── buffett_index.csv
└── README.md
```

---

## 5. 성능 평가

- **최종 예측 모델 (Long-term)**
  - RMSE: 0.0100
  - MAPE: 5.99%
  - 구조: Bidirectional LSTM, 24개월 시계열, 중복 지표 제거
- 예측 결과는 최근 분기 기준으로 자동 보정
- 실제 GDP와 오차가 크지 않아, 예측값을 활용한 실용적 지표 구성 가능

---

## 6. 현재 구현 현황

- [x] 거시경제 지표 수집 및 정규화
- [x] LSTM 기반 GDP 예측 모델 학습 및 시각화
- [x] 버핏지수 산출 및 React + Plotly.js 시각화
- [x] 실시간 예측값 기반 GDP 확장 및 자동 보정
- [ ] 백엔드 API로 지표 데이터 연동 (계획 중)
- [ ] 알림 기능 및 사용자 설정 기능 (계획 중)

---

## 7. 참고 자료

- [FRED Economic Data](https://fred.stlouisfed.org/)
- [Yahoo Finance - Wilshire 5000](https://finance.yahoo.com/)
- [TensorFlow Documentation](https://www.tensorflow.org/)
- [Financial Modeling Prep API](https://financialmodelingprep.com/)

---

## 8. 개발 개선상황

- 모델 성능 향상을 위해 여러 파라미터 실험 및 보정 기법 시도
- 시계열 예측의 한계를 느끼며 예측 구간 구분 전략(장기/단기)을 도입
- Plotly + React 조합으로 고해상도 대시보드 구현 가능성 확인
- 실제 지표 수집 → 학습 → 예측 → 시각화까지 파이프라인 자동화 완료
- 한계: 실제 자산 가격 예측에는 아직 거리 존재, 설명력 높은 종합지표 도입 필요

