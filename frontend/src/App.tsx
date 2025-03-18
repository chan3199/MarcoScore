import React from 'react'
import BuffettIndex from './components/BuffettIndex'
import EconomicIndicators from './components/EconomicIndicators'
import EconomicChart from './components/EconomicChart'

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-6">
      <h1 className="text-3xl font-bold text-center text-indigo-700 mb-6">
        MacroScore - 거시 경제 데이터
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-6xl w-full">
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <BuffettIndex />
        </div>

        <div className="bg-white p-6 rounded-lg shadow-lg">
          <EconomicIndicators />
        </div>

        {/* 📈 버핏지수 차트 추가 */}
        <div className="col-span-1 md:col-span-2 bg-white p-6 rounded-lg shadow-lg">
          <EconomicChart />
        </div>
      </div>
    </div>
  )
}

export default App
