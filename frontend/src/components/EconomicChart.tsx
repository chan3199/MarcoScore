import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { Line } from 'react-chartjs-2'
import dayjs from 'dayjs'
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from 'chart.js'

// ✅ Chart.js 기본 설정
ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
  Filler,
)

// 📌 API 응답 데이터 타입 정의
interface BuffettData {
  date: string
  buffettIndex: number
  sp500: number
}

// 📌 기간 옵션 정의
const timeRanges: Record<string, number> = {
  '10년': 40,
  '5년': 20,
  '3년': 12,
  '1년': 12, // ✅ 1개월 단위
}

const EconomicChart: React.FC = () => {
  const [chartData, setChartData] = useState<BuffettData[]>([])
  const [loading, setLoading] = useState<boolean>(true)
  const [selectedRange, setSelectedRange] =
    useState<keyof typeof timeRanges>('10년')

  useEffect(() => {
    setLoading(true)

    axios
      .get<{ success: boolean; data: BuffettData[] }>(
        'http://localhost:5000/api/economy/buffett-index',
      )
      .then((response) => {
        console.log('📊 API 응답 데이터:', response.data)

        if (response.data.success && response.data.data.length > 0) {
          const formattedData = response.data.data
            .map((item) => ({
              date: dayjs(item.date).format('YYYY-MM'),
              buffettIndex: item.buffettIndex,
              sp500: item.sp500,
            }))
            .reverse() // 최신 데이터가 오른쪽으로 정렬되도록 reverse()

          setChartData(formattedData)
        } else {
          console.warn('⚠️ API 응답은 성공했지만 데이터가 없습니다.')
        }
      })
      .catch((error) => {
        console.error('❌ API 요청 실패:', error)
      })
      .finally(() => setLoading(false))
  }, [])

  // ✅ 선택한 기간만큼 데이터 필터링
  const filteredData =
    chartData.length > 0 ? chartData.slice(-timeRanges[selectedRange]) : []

  // ✅ X축(연도별 표시) 및 Y축(지표 값) 설정
  const labels = filteredData.map((item) => item.date)
  const buffettValues = filteredData.map((item) => item.buffettIndex)
  const sp500Values = filteredData.map((item) => item.sp500)

  // ✅ Buffett Index 차트 데이터
  const buffettChartData = {
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
    ],
  }

  // ✅ S&P 500 차트 데이터
  const sp500ChartData = {
    labels,
    datasets: [
      {
        label: 'S&P 500',
        data: sp500Values,
        borderColor: 'rgba(54, 162, 235, 1)',
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderWidth: 2,
        fill: false,
      },
    ],
  }

  // ✅ Chart.js 옵션 설정 (X축 날짜 간격 조정)
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        ticks: {
          autoSkip: true,
          maxTicksLimit: 6,
        },
      },
    },
    plugins: {
      legend: { position: 'top' as const },
      title: { display: false },
    },
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg w-full">
      <h2 className="text-2xl font-bold text-indigo-700 mb-4 text-center">
        📈 Buffett Index & S&P 500 차트
      </h2>

      {/* ✅ 기간 선택 버튼 UI */}
      <div className="mb-4 flex flex-wrap justify-center gap-2">
        {Object.keys(timeRanges).map((range) => (
          <button
            key={range}
            onClick={() => {
              setLoading(true)
              setSelectedRange(range)
              setTimeout(() => setLoading(false), 500)
            }}
            className={`px-4 py-2 rounded-md ${
              selectedRange === range
                ? 'bg-indigo-600 text-white'
                : 'bg-gray-200'
            }`}
          >
            {range}
          </button>
        ))}
      </div>

      {/* ✅ 데이터 로딩 중 UI */}
      {loading ? (
        <p className="text-gray-500 text-center">⏳ 데이터 로딩 중...</p>
      ) : filteredData.length === 0 ? (
        <p className="text-gray-500 text-center">
          해당 기간에 데이터가 없습니다.
        </p>
      ) : (
        // ✅ 차트 2개 나란히 배치하여 화면 활용
        <div className="w-full flex flex-col md:flex-row gap-6">
          {/* ✅ Buffett Index 차트 */}
          <div className="w-full md:w-1/2">
            <h3 className="text-center font-semibold text-red-500">
              Buffett Index (%)
            </h3>
            <div className="w-full max-w-[600px] mx-auto">
              <Line data={buffettChartData} options={chartOptions} />
            </div>
          </div>

          {/* ✅ S&P 500 차트 */}
          <div className="w-full md:w-1/2">
            <h3 className="text-center font-semibold text-blue-500">S&P 500</h3>
            <div className="w-full max-w-[600px] mx-auto">
              <Line data={sp500ChartData} options={chartOptions} />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default EconomicChart
