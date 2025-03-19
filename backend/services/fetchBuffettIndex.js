const axios = require("axios");
require("dotenv").config();

const FMP_API_KEY = process.env.FMP_API_KEY;
const FRED_API_KEY = process.env.FRED_API_KEY;

// 📌 SPY의 시가총액을 가져와서 일별 데이터 저장
const fetchSPYMarketCapHistory = async () => {
  try {
    const url = `https://financialmodelingprep.com/api/v3/historical-market-capitalization/SPY?apikey=${FMP_API_KEY}`;
    const response = await axios.get(url);

    if (!response.data || response.data.length === 0) {
      throw new Error("SPY 시가총액 데이터를 찾을 수 없습니다.");
    }

    // 📌 일별 시가총액 데이터 저장
    const marketCapByDate = {};
    response.data.forEach(entry => {
      marketCapByDate[entry.date] = entry.marketCap;
    });

    return marketCapByDate;
  } catch (error) {
    console.error("❌ SPY 시가총액 가져오기 실패:", error.message);
    return null;
  }
};

// 📌 GDP 데이터를 가져와서 일별 데이터 저장
const fetchGDPHistory = async () => {
  try {
    const url = `https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key=${FRED_API_KEY}&file_type=json`;
    const response = await axios.get(url);

    if (!response.data.observations || response.data.observations.length === 0) {
      throw new Error("GDP 데이터가 없습니다.");
    }

    // 📌 일별 GDP 데이터 저장
    const gdpByDate = {};
    response.data.observations.forEach(entry => {
      if (entry.value !== ".") { // 빈 값 제외
        gdpByDate[entry.date] = parseFloat(entry.value);
      }
    });

    return gdpByDate;
  } catch (error) {
    console.error("❌ GDP 데이터 가져오기 실패:", error.message);
    return null;
  }
};

// 📌 버핏지수 계산 및 버튼 선택별 데이터 필터링
const calculateBuffettIndex = async (selectedRange) => {
    const spyMarketCapHistory = await fetchSPYMarketCapHistory();
    const gdpHistory = await fetchGDPHistory();

    if (!spyMarketCapHistory || !gdpHistory) {
        console.error("🚨 데이터 부족으로 버핏지수를 계산할 수 없습니다.");
        return null;
    }

    console.log("✅ SPY 데이터 개수:", Object.keys(spyMarketCapHistory).length);
    console.log("✅ GDP 데이터 개수:", Object.keys(gdpHistory).length);

    if (Object.keys(spyMarketCapHistory).length === 0 || Object.keys(gdpHistory).length === 0) {
        console.error("🚨 데이터가 비어있음. API 응답 확인 필요");
        return null;
    }
    const buffettIndexHistory = [];

    // 📌 선택한 기간(예: 1년, 5년)에 따라 필터링
    const today = new Date();
    const dateRanges = {
        "5년": new Date(today.setFullYear(today.getFullYear() - 5)),
        "3년": new Date(today.setFullYear(today.getFullYear() - 3)),
        "1년": new Date(today.setFullYear(today.getFullYear() - 1)),
        "6개월": new Date(today.setMonth(today.getMonth() - 6)),
        "3개월": new Date(today.setMonth(today.getMonth() - 3)),
    };

    const selectedDateThreshold = dateRanges[selectedRange];

  // 📌 데이터 필터링 (선택한 기간 내의 데이터만 포함)
    for (const date of Object.keys(spyMarketCapHistory)) {
    const recordDate = new Date(date);
    if (recordDate >= selectedDateThreshold) {
        if (gdpHistory[date]) {
        const spyMarketCap = spyMarketCapHistory[date];
        const estimatedSP500MarketCap = spyMarketCap * 11;
        const buffettIndex = (estimatedSP500MarketCap / gdpHistory[date]) * 100;

        buffettIndexHistory.push({
            date,
            buffettIndex,
            estimatedSP500MarketCap,
            gdp: gdpHistory[date],
        });
        }
    }
    }

    console.log(`📊 ${selectedRange} 기간의 버핏지수 데이터 계산 완료!`, buffettIndexHistory.slice(-5)); // 최근 5개 데이터 확인
    return buffettIndexHistory;
};

module.exports = { calculateBuffettIndex };
