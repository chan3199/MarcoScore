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
        setData(response.data.data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching GDP data:', error)
        setLoading(false)
      })
  }, [])

  return (
    <div>
      <h2 className="text-xl font-bold text-indigo-700 mb-4">📊 GDP Data</h2>
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <ul className="space-y-2">
          {data.slice(-5).map((item, index) => (
            <li key={index} className="bg-gray-100 p-2 rounded-md shadow">
              <span className="font-semibold">{item.date}:</span> {item.value}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

export default GdpData
