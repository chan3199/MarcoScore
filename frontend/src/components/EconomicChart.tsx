import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Line } from 'react-chartjs-2'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

// Chart.js 요소 등록
Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

// 데이터 타입 정의
interface BuffettData {
  date: string
  buffettIndex: number
  sp500: number
  interestRate: number
}

const EconomicChart: React.FC = () => {
  const [chartData, setChartData] = useState<BuffettData[]>([])
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    axios.get<{ success: boolean; data: BuffettData[] }>('http://localhost:5000/api/economy/buffett-index')
      .then(response => {
        const formattedData = response.data.data.map((item, index) => ({
          date: `Q${(index % 4) + 1} ${item.date.split('-')[0]}`, // YYYY-MM-DD → Q1 2024 형식 변환
          buffettIndex: item.buffettIndex,
          sp500: item.sp500,
          interestRate: item.interestRate,
        }))
        setChartData(formattedData)
        setLoading(false)
      })
      .catch(error => {
        console.error('Error fetching Buffett Index data:', error)
        setLoading(false)
      })
  }, [])

  // X축(연도별 분기)과 Y축(지표 값) 설정
  const labels = chartData.map(item => item.date)
  const buffettValues = chartData.map(item => item.buffettIndex)
  const sp500Values = chartData.map(item => item.sp500)
  const interestRates = chartData.map(item => item.interestRate)

  // Chart.js 데이터 설정
  const data = {
    labels,
    datasets: [
      {
        label: 'Buffett Index (%)',
        data: buffettValues,
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderWidth: 2,
        fill: true,
      },
      {
        label: 'S&P 500',
        data: sp500Values,
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderWidth: 2,
        fill: false,
      },
      {
        label: 'Interest Rate (%)',
        data: interestRates,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderWidth: 2,
        fill: false,
      }
    ]
  }

  // Chart.js 옵션 설정
  const options = {
    responsive: true,
    plugins: {
      legend: { position: 'top' as const },
      title: { display: true, text: 'Buffett Index & Economic Indicators' }
    }
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold text-indigo-700 mb-4">📈 Buffett Index Chart</h2>
      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <Line data={data} options={options} />
      )}
    </div>
  )
}

export default EconomicChart
