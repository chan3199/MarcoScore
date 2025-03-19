const yahooFinance = require("yahoo-finance2").default; 

// ✅ SPY ETF의 시가총액 가져오기
const fetchSPYMarketCap = async () => {
  try {
    const data = await yahooFinance.quoteSummary("SPY", { modules: ["summaryDetail"] });
    const spyMarketCap = data.summaryDetail.marketCap.raw;

    if (!spyMarketCap) {
      throw new Error("SPY 시가총액 데이터를 가져올 수 없음");
    }

    console.log(`📊 SPY Market Cap: ${spyMarketCap.toLocaleString()} USD`);
    return spyMarketCap;
  } catch (error) {
    console.error("❌ SPY 시가총액 가져오기 실패:", error.message);
    return null;
  }
};

// ✅ S&P 500 전체 시가총액 추정 (SPY 기반)
const estimateSP500MarketCap = async () => {
  const spyMarketCap = await fetchSPYMarketCap();
  if (!spyMarketCap) return null;

  // 🔹 SPY ETF는 S&P 500의 약 99.5%를 추종하므로 1.005배 보정
  const estimatedSP500MarketCap = spyMarketCap * 1.005;
  console.log(`📈 Estimated S&P 500 Market Cap: ${estimatedSP500MarketCap.toLocaleString()} USD`);

  return estimatedSP500MarketCap;
};

module.exports = { estimateSP500MarketCap };
