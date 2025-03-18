const express = require('express')
const { fetchEconomicData } = require('../services/fredService')

const router = express.Router()

// ✅ GDP 데이터 가져오기 API
router.get('/gdp', async (req, res) => {
  const data = await fetchEconomicData('GDP')
  if (data) {
    res.json({ success: true, data })
  } else {
    res.status(500).json({ success: false, message: 'Failed to fetch GDP data' })
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

// ✅ 버핏지수 계산 API
router.get('/buffett-index', async (req, res) => {
  try {
    // 최근 GDP 데이터 가져오기
    const gdpData = await fetchEconomicData('GDP')
    // 최근 S&P 500 데이터 가져오기
    const sp500Data = await fetchEconomicData('SP500')

    if (!gdpData || !sp500Data) {
      return res.status(500).json({ success: false, message: 'Failed to fetch data' })
    }

    // 최신 GDP 및 S&P 500 값 가져오기
    const latestGDP = parseFloat(gdpData[gdpData.length - 1].value)
    const latestSP500 = parseFloat(sp500Data[sp500Data.length - 1].value)

    // 버핏지수 계산
    const buffettIndex = (latestSP500 / latestGDP) * 100

    res.json({
      success: true,
      data: { buffettIndex, latestGDP, latestSP500 }
    })
  } catch (error) {
    console.error('Error calculating Buffett Index:', error)
    res.status(500).json({ success: false, message: 'Server error' })
  }
})

module.exports = router
