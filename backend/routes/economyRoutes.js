const express = require('express')
const { calculateBuffettIndex } = require("../services/fetchBuffettIndex");
const router = express.Router()

// 📌 버핏지수 API 엔드포인트 (1970년 이후 데이터 제공)
router.get("/buffett-index", async (req, res) => {
  try {
    const result = await calculateBuffettIndex();
    if (!result) {
      return res.status(500).json({ success: false, message: "데이터를 가져오는 데 실패했습니다." });
    }
    res.json({ success: true, data: result });
  } catch (error) {
    console.error("❌ 버핏지수 API 오류:", error.message);
    res.status(500).json({ success: false, message: "서버 오류 발생" });
  }
});

router.get("/indicators", async (req, res) => {
  try {
    const economicData = {
      unemployment: 3.4,
      inflation: 21.48,
      interestRate: 1.13,
      sp500: 2099.5
    }

    res.json({ success: true, data: economicData })
  } catch (error) {
    console.error("❌ 경제 지표 데이터 가져오기 실패:", error)
    res.status(500).json({ success: false, message: "서버 오류 발생" })
  }
})


router.get("/api/economy/indicators", async (req, res) => {
  try {
    const economicData = await fetchEconomicData() // 여기에 실제 데이터를 가져오는 함수 추가
    if (!economicData) {
      return res.status(404).json({ success: false, message: "데이터가 없습니다." })
    }
    res.json({ success: true, data: economicData })
  } catch (error) {
    console.error("❌ 경제 데이터 불러오기 실패:", error)
    res.status(500).json({ success: false, message: "서버 오류 발생" })
  }
})

// ✅ 실업률 데이터
router.get('/unemployment', async (req, res) => {
  const data = await fetchEconomicData('UNRATE')
  if (data) {
    res.json({ success: true, data })
  } else {
    res.status(500).json({ success: false, message: 'Failed to fetch unemployment data' })
  }
})

// ✅ 소비자물가지수 (CPI, 인플레이션) 데이터
router.get('/inflation', async (req, res) => {
  const data = await fetchEconomicData('CPIAUCSL')
  if (data) {
    res.json({ success: true, data })
  } else {
    res.status(500).json({ success: false, message: 'Failed to fetch inflation data' })
  }
})

// ✅ 기준금리 데이터
router.get('/interest-rate', async (req, res) => {
  const data = await fetchEconomicData('DFF')
  if (data) {
    res.json({ success: true, data })
  } else {
    res.status(500).json({ success: false, message: 'Failed to fetch interest rate data' })
  }
})

// ✅ 10년-2년 국채금리 차이 (경기 침체 신호)
router.get('/yield-curve', async (req, res) => {
  const data = await fetchEconomicData('T10Y2Y')
  if (data) {
    res.json({ success: true, data })
  } else {
    res.status(500).json({ success: false, message: 'Failed to fetch yield curve data' })
  }
})

// ✅ S&P 500 지수
router.get('/sp500', async (req, res) => {
  const data = await fetchEconomicData('SP500')
  if (data) {
    res.json({ success: true, data })
  } else {
    res.status(500).json({ success: false, message: 'Failed to fetch S&P 500 data' })
  }
})


module.exports = router
