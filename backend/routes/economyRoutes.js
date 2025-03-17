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

// ✅ 금리 데이터 가져오기 API
router.get('/interest-rate', async (req, res) => {
  const data = await fetchEconomicData('DFF') // 연방기금 금리
  if (data) {
    res.json({ success: true, data })
  } else {
    res.status(500).json({ success: false, message: 'Failed to fetch interest rate data' })
  }
})

module.exports = router
