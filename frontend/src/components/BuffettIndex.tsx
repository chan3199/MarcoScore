import React, { useEffect, useState } from 'react'
import axios from 'axios'

// 📌 API 응답 타입 정의
interface BuffettIndexResponse {
  success: boolean
  data: {
    date: string
    buffettIndex: number
    gdp: number
    sp500: number
  }[]
}

const BuffettIndex: React.FC = () => {
  const [buffettIndex, setBuffettIndex] = useState<number | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    axios.get<BuffettIndexResponse>('http://localhost:5000/api/economy/buffett-index')
      .then(response => {
        console.log("📊 API 응답 데이터:", response.data)

        if (response.data.success && response.data.data.length > 0) {
          const latestBuffett = response.data.data[0].buffettIndex  // 최신 데이터 가져오기
          setBuffettIndex(latestBuffett)
        } else {
          console.warn("⚠️ API 응답은 성공했지만 데이터가 없습니다.")
        }
      })
      .catch(error => {
        console.error("❌ API 요청 실패:", error)
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold text-indigo-700 mb-4">📊 Buffett Index</h2>
      {loading ? (
        <p className="text-gray-500">⏳ Loading...</p>
      ) : buffettIndex !== null ? (
        <p className="text-gray-700 text-lg font-semibold">
          📈 {buffettIndex.toFixed(2)}
        </p>
      ) : (
        <p className="text-red-500">❌ 데이터 없음</p>
      )}
    </div>
  )
}

export default BuffettIndex
