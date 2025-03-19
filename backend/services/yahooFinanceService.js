const axios = require("axios");
const cheerio = require("cheerio");

// 📌 Yahoo Finance에서 Crumb Token 가져오기
const getYahooCrumb = async () => {
    try {
      const response = await axios.get("https://finance.yahoo.com/quote/AAPL", {
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        },
        maxRedirects: 5, // ✅ 리디렉션 제한
      });
  
      const $ = cheerio.load(response.data);
      const scriptContent = $("script").text();
      const crumbMatch = scriptContent.match(/"CrumbStore":\{"crumb":"(.*?)"\}/);
  
      if (crumbMatch && crumbMatch[1]) {
        console.log("🟢 Crumb Token:", crumbMatch[1]);
        return crumbMatch[1];
      } else {
        throw new Error("Crumb을 찾을 수 없음");
      }
    } catch (error) {
      console.error("❌ Crumb 가져오기 실패:", error.message);
      return null;
    }
  };

// 📌 Yahoo Finance에서 Market Cap 가져오기
const fetchMarketCapWithCrumb = async (ticker) => {
  try {
    const crumb = await getYahooCrumb();
    if (!crumb) {
      console.error("❌ Crumb 없음");
      return null;
    }

    const url = `https://query1.finance.yahoo.com/v10/finance/quoteSummary/${ticker}?modules=price&crumb=${crumb}`;
    console.log(`🟢 Fetching Market Cap from: ${url}`);

    const response = await axios.get(url, {
      headers: {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
      }
    });

    console.log("📊 API 응답 데이터:", JSON.stringify(response.data, null, 2)); // ✅ API 응답 확인

    // 📌 데이터 구조 검증
    const result = response.data?.quoteSummary?.result?.[0];
    if (!result) {
      console.warn(`⚠️ ${ticker}에 대한 유효한 데이터가 없습니다.`);
      return null;
    }

    // 📌 marketCap을 `price.marketCap`에서 가져오고, 없을 경우 `summaryDetail.marketCap` 사용
    const marketCap = result.price?.marketCap?.raw || result.summaryDetail?.marketCap?.raw;

    if (!marketCap) {
      console.warn(`⚠️ ${ticker}의 시가총액 데이터를 찾을 수 없습니다.`);
      return null;
    }

    console.log(`🟢 ${ticker} Market Cap:`, marketCap);
    return marketCap;
  } catch (error) {
    console.error(`❌ ${ticker} Market Cap 가져오기 실패:`, error.message);
    return null;
  }
};

module.exports = { fetchMarketCapWithCrumb };
