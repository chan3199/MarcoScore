import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { ChartOptions } from 'chart.js'
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
  Filler // ✅ Filler 추가
} from "chart.js"

ChartJS.register(
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
  Legend,
  Filler // ✅ Filler 플러그인 등록
)

// 📌 API 응답 데이터 타입 정의
interface BuffettData {
  date: string
  buffettIndex: number
  sp500: number
  interestRate: number
}

// 📌 기간 옵션 정의
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
  const [selectedRange, setSelectedRange] = useState<keyof typeof timeRanges>('10년')

  useEffect(() => {
    setLoading(true)

    axios.get<{ success: boolean; data: BuffettData[] }>('http://localhost:5000/api/economy/buffett-index')
      .then(response => {
        console.log("📊 API 응답 데이터:", response.data)

        if (response.data.success && response.data.data.length > 0) {
          const formattedData = response.data.data
            .map((item, index) => ({
              date: `${dayjs(item.date).format('YYYY')}-Q${(index % 4) + 1}`, // ✅ 연도 + 분기 형식
              buffettIndex: item.buffettIndex,
              sp500: item.sp500,
              interestRate: item.interestRate,
            }))
            .sort((a, b) => dayjs(b.date, 'YYYY-Q').valueOf() - dayjs(a.date, 'YYYY-Q').valueOf()) // ✅ 최신 연도부터 정렬 (내림차순)


          setChartData(formattedData)
        } else {
          console.warn("⚠️ API 응답은 성공했지만 데이터가 없습니다.")
        }
      })
      .catch(error => {
        console.error("❌ API 요청 실패:", error)
      })
      .finally(() => setLoading(false))
  }, [])

  // ✅ 선택한 기간만큼 데이터 필터링
  const filteredData = chartData.length > 0 
  ? chartData.slice(0, timeRanges[selectedRange]).reverse()  // ✅ 최신 데이터만 가져와 X축 정렬
  : []

  // ✅ X축(연도별 분기) 및 Y축(지표 값) 설정
  const labels = filteredData.map(item => item.date)
  const buffettValues = filteredData.map(item => item.buffettIndex)
  const sp500Values = filteredData.map(item => item.sp500)
  const interestRates = filteredData.map(item => item.interestRate)

  // ✅ Chart.js 데이터 설정
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

  // ✅ Chart.js 옵션 설정 (X축 날짜 간격 조정)
  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    aspectRatio: 2.5,  // ✅ 가로 대비 세로 비율 조정
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
      title: { display: true, text: 'Buffett Index Chart' },
    },
  }

  return (
    <div className="bg-white p-6 rounded-lg shadow-lg w-full">
      <h2 className="text-2xl font-bold text-indigo-700 mb-4 text-center">📈 Buffett Index Chart</h2>
  
      {/* ✅ 기간 선택 버튼 UI */}
      <div className="mb-4 flex flex-wrap justify-center gap-2">
        {Object.keys(timeRanges).map(range => (
          <button
            key={range}
            onClick={() => {
              setLoading(true)
              setSelectedRange(range)
              setTimeout(() => setLoading(false), 500)
            }}
            className={`px-4 py-2 rounded-md ${
              selectedRange === range ? 'bg-indigo-600 text-white' : 'bg-gray-200'
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
        <p className="text-gray-500 text-center">📌 해당 기간에 데이터가 없습니다.</p>
      ) : (
        // ✅ 차트 중앙 정렬 및 최대 너비 설정
      <div className="w-full flex justify-center">
        <div className="w-full max-w-[1200px]">  {/* ✅ 최대 너비 증가 */}
          <Line data={data} options={options} />
        </div>
      </div>
      )}
    </div>
  )
  
  
}

export default EconomicChart
