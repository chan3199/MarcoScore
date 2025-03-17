const express = require('express')
const { fetchEconomicData } = require('../services/fredService') // ✅ 올바른 경로 확인!

const router = express.Router()

// GDP 데이터 가져오기
router.get('/gdp', async (req, res) => {
  try {
    const data = await fetchEconomicData('GDP') // ✅ 함수 호출 확인
    if (data) {
      res.json({ success: true, data })
    } else {
      res.status(500).json({ success: false, message: 'Failed to fetch GDP data' })
    }
  } catch (error) {
    res.status(500).json({ success: false, message: 'Server error', error })
  }
})

module.exports = router
