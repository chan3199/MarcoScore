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

// 기간 옵션 정의
const timeRanges: Record<string, number> = {
    '10년': 40,
    '5년': 20,
    '3년': 12,
    '1년': 4,
    '6개월': 2,
    '3개월': 1
  }

const EconomicChart: React.FC = () => {
  const [chartData, setChartData] = useState<BuffettData[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [selectedRange, setSelectedRange] = useState<string>('10년')

  useEffect(() => {
    axios.get<{ success: boolean; data: BuffettData[] }>('http://localhost:5000/api/economy/buffett-index')
      .then(response => {
        const formattedData = response.data.data.map((item, index) => ({
          date: `Q${(index % 4) + 1} ${item.date.split('-')[0]}`,
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

  // 선택한 기간만큼 데이터 필터링
  const filteredData = chartData.slice(-timeRanges[selectedRange])

  // X축(연도별 분기)과 Y축(지표 값) 설정
  const labels = filteredData.map(item => item.date)
  const buffettValues = filteredData.map(item => item.buffettIndex)
  const sp500Values = filteredData.map(item => item.sp500)
  const interestRates = filteredData.map(item => item.interestRate)

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
      title: { display: true, text: `Buffett Index (${selectedRange})` }
    }
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg">
      <h2 className="text-xl font-bold text-indigo-700 mb-4">📈 Buffett Index Chart</h2>

      {/* 기간 선택 버튼 */}
      <div className="mb-4 flex flex-wrap gap-2">
        {Object.keys(timeRanges).map(range => (
          <button
            key={range}
            onClick={() => setSelectedRange(range)}
            className={`px-3 py-1 rounded-md ${
              selectedRange === range ? 'bg-indigo-600 text-white' : 'bg-gray-200'
            }`}
          >
            {range}
          </button>
        ))}
      </div>

      {loading ? (
        <p className="text-gray-500">Loading...</p>
      ) : (
        <Line data={data} options={options} />
      )}
    </div>
  )
}

export default EconomicChart
