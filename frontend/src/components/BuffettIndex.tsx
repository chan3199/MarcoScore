import React, { useEffect, useState } from 'react'
import axios from 'axios'

interface BuffettData {
  buffettIndex: number
  latestGDP: number
  latestSP500: number
}

const BuffettIndex: React.FC = () => {
  const [data, setData] = useState<BuffettData | null>(null)
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    axios.get<{ success: boolean; data: BuffettData }>('http://localhost:5000/api/economy/buffett-index')
      .then(response => {
        setData(response.data.data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching Buffett Index data:', error)
        setLoading(false)
      })
  }, [])

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold text-indigo-700 mb-4">📊 Buffett Index</h2>
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <ul className="space-y-2">
          <li className="flex justify-between border-b pb-1">
            <span>📈 Buffett Index:</span> <span>{data?.buffettIndex.toFixed(2)}%</span>
          </li>
          <li className="flex justify-between border-b pb-1">
            <span>💰 Latest GDP:</span> <span>{data?.latestGDP.toFixed(2)}</span>
          </li>
          <li className="flex justify-between">
            <span>📊 S&P 500:</span> <span>{data?.latestSP500.toFixed(2)}</span>
          </li>
        </ul>
      )}
    </div>
  )
}

export default BuffettIndex
