import React, { useEffect, useState } from "react"
import axios from "axios"

interface EconomicIndicatorsProps {
  className?: string
}

const EconomicIndicators: React.FC<EconomicIndicatorsProps> = ({ className }) => {
  const [indicators, setIndicators] = useState<{
    unemployment: number | null
    inflation: number | null
    interestRate: number | null
    sp500: number | null
  }>({
    unemployment: null,
    inflation: null,
    interestRate: null,
    sp500: null
  })

  const [loading, setLoading] = useState<boolean>(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/economy/indicators")
        console.log("📌 API 응답 데이터:", response.data)

        if (response.data.success && response.data.data) {
          setIndicators({
            unemployment: response.data.data.unemployment,
            inflation: response.data.data.inflation,
            interestRate: response.data.data.interestRate,
            sp500: response.data.data.sp500
          })
        } else {
          throw new Error("⚠️ API 응답은 성공했지만 데이터가 없습니다.")
        }
      } catch (err) {
        console.error("❌ API 요청 실패:", err)
        setError("데이터를 불러오는 중 오류가 발생했습니다.")
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  return (
    <div className={`bg-white p-6 rounded-lg shadow-lg ${className || ""}`}>
      <h2 className="text-xl font-bold text-red-600 flex items-center">📌 Economic Indicators</h2>

      {loading ? (
        <p className="text-gray-500">⏳ 로딩 중...</p>
      ) : error ? (
        <p className="text-red-500">{error}</p>
      ) : (
        <ul className="mt-4 space-y-2">
          <li>📉 Unemployment: {indicators.unemployment !== null ? `${indicators.unemployment}%` : "❌ 데이터 없음"}</li>
          <li>📊 Inflation: {indicators.inflation !== null ? `${indicators.inflation}%` : "❌ 데이터 없음"}</li>
          <li>💰 Interest Rate: {indicators.interestRate !== null ? `${indicators.interestRate}%` : "❌ 데이터 없음"}</li>
          <li>📈 S&P 500: {indicators.sp500 !== null ? indicators.sp500.toFixed(2) : "❌ 데이터 없음"}</li>
        </ul>
      )}
    </div>
  )
}

export default EconomicIndicators
