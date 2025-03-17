require('dotenv').config()
const axios = require('axios')

const FRED_API_KEY = process.env.FRED_API_KEY
const BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

/**
 * 특정 경제 지표 데이터를 가져오는 함수
 * @param {string} seriesId - FRED에서 제공하는 데이터 시리즈 ID (예: GDP, 금리 등)
 */
async function fetchEconomicData(seriesId) {
  try {
    const response = await axios.get(BASE_URL, {
      params: {
        series_id: seriesId,
        api_key: FRED_API_KEY,
        file_type: 'json'
      }
    })
    return response.data.observations
  } catch (error) {
    console.error(`Error fetching data for ${seriesId}:`, error)
    return null
  }
}

// ✅ 모듈 내보내기 수정
module.exports = { fetchEconomicData }
