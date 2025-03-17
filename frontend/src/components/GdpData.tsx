import React, { useEffect, useState } from 'react'
import axios from 'axios'

interface GDPData {
  date: string
  value: string
}

const GdpData: React.FC = () => {
  const [data, setData] = useState<GDPData[]>([])
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    axios.get<{ success: boolean; data: GDPData[] }>('http://localhost:5000/api/economy/gdp')
      .then(response => {
        console.log('API 응답 데이터:', response.data) // ✅ 응답 데이터 콘솔 출력
        setData(response.data.data) // ✅ 데이터 상태 업데이트
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching GDP data:', error)
        setLoading(false)
      })
  }, [])
  

  return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-bold mb-4 text-indigo-600">GDP Data</h2>
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <ul>
          {data.slice(-5).map((item, index) => (
            <li key={index} className="border-b py-2 text-blue-600">
              {item.date}: {item.value}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default GdpData
