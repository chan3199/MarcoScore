import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Line } from 'react-chartjs-2'
import { Chart, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ChartData } from 'chart.js'

// Chart.js에 필요한 요소 등록
Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

// 데이터 인터페이스 정의
interface Indicator {
  date: string
  value: string
}

const EconomicChart: React.FC = () => {
  const [gdpData, setGdpData] = useState<Indicator[]>([])
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    axios.get<{ success: boolean; data: Indicator[] }>('http://localhost:5000/api/economy/gdp')
      .then(response => {
        setGdpData(response.data.data)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching GDP data:', error)
        setLoading(false)
      })
  }, [])

  // 날짜와 값 데이터 추출
  const labels = gdpData.map(item => item.date)
  const values = gdpData.map(item => parseFloat(item.value))

  // 차트 데이터 구성
  const chartData: ChartData<'line'> = {
    labels,
    datasets: [
      {
        label: 'GDP 변화',
        data: values,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderWidth: 2,
        fill: true,
      }
    ]
  }

  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: true, text: 'GDP 변화 추이' },
    },
  }

  return (
    <div className="p-6 bg-white shadow-lg rounded-lg">
      <h2 className="text-xl font-bold mb-4 text-indigo-600">GDP 시각화</h2>
      {loading ? <p className="text-gray-500">Loading...</p> : <Line data={chartData} options={options} />}
    </div>
  )
}

export default EconomicChart
