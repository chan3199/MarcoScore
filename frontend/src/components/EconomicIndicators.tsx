import React, { useEffect, useState } from 'react'
import axios from 'axios'

interface Indicator {
  unemployment: number
  inflation: number
  interestRate: number
  sp500: number
}

const EconomicIndicators: React.FC = () => {
  const [data, setData] = useState<Indicator | null>(null)

  useEffect(() => {
    Promise.all([
      axios.get<{ success: boolean; data: [{ value: string }] }>('http://localhost:5000/api/economy/unemployment'),
      axios.get<{ success: boolean; data: [{ value: string }] }>('http://localhost:5000/api/economy/inflation'),
      axios.get<{ success: boolean; data: [{ value: string }] }>('http://localhost:5000/api/economy/interest-rate'),
      axios.get<{ success: boolean; data: [{ value: string }] }>('http://localhost:5000/api/economy/sp500'),
    ])
      .then(([unemploymentRes, inflationRes, interestRateRes, sp500Res]) => {
        setData({
          unemployment: parseFloat(unemploymentRes.data.data[0].value),
          inflation: parseFloat(inflationRes.data.data[0].value),
          interestRate: parseFloat(interestRateRes.data.data[0].value),
          sp500: parseFloat(sp500Res.data.data[0].value),
        })
      })
      .catch(error => console.error('Error fetching economic indicators:', error))
  }, [])

  return (
    <div>
      <h2 className="text-xl font-bold text-indigo-700 mb-4">📌 Economic Indicators</h2>
      {data ? (
        <ul className="space-y-2">
          <li className="flex justify-between border-b pb-1">
            <span>📉 Unemployment:</span> <span>{data.unemployment}%</span>
          </li>
          <li className="flex justify-between border-b pb-1">
            <span>📈 Inflation:</span> <span>{data.inflation}%</span>
          </li>
          <li className="flex justify-between border-b pb-1">
            <span>💰 Interest Rate:</span> <span>{data.interestRate}%</span>
          </li>
          <li className="flex justify-between">
            <span>📊 S&P 500:</span> <span>{data.sp500}</span>
          </li>
        </ul>
      ) : (
        <p className="text-gray-500">Loading...</p>
      )}
    </div>
  )
}

export default EconomicIndicators
