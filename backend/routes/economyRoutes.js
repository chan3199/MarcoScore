const express = require('express')
const { fetchEconomicData } = require('../services/fredService')

const router = express.Router()

// ✅ 버핏지수 시계열 데이터 API
router.get('/buffett-index', async (req, res) => {
  try {
    // 📌 최근 10년치 GDP 데이터 가져오기
    const gdpData = await fetchEconomicData('GDP')
    // 📌 최근 10년치 S&P 500 데이터 가져오기
    const sp500Data = await fetchEconomicData('SP500')

    if (!gdpData || !sp500Data) {
      return res.status(500).json({ success: false, message: 'Failed to fetch data' })
    }

    // 📌 버핏지수 시계열 데이터 계산
    let buffettIndexData = []
    for (let i = 0; i < Math.min(gdpData.length, sp500Data.length); i++) {
      const gdpValue = parseFloat(gdpData[i].value)
      const sp500Value = parseFloat(sp500Data[i].value)

      if (gdpValue > 0 && sp500Value > 0) {
        buffettIndexData.push({
          date: gdpData[i].date,  // YYYY-MM-DD 형식
          buffettIndex: (sp500Value / gdpValue) * 100,
          gdp: gdpValue,
          sp500: sp500Value
        })
      }
    }

    res.json({
      success: true,
      data: buffettIndexData.reverse() // 최신 데이터가 앞에 오도록 정렬
    })
  } catch (error) {
    console.error('Error calculating Buffett Index:', error)
    res.status(500).json({ success: false, message: 'Server error' })
  }
})

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
