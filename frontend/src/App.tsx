import React from 'react'
import GdpData from './components/GdpData'

const App: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="p-6 bg-white shadow-lg rounded-lg">
        <h1 className="text-2xl font-bold text-center text-indigo-600 mb-4">
          MacroScore - 거시 경제 데이터
        </h1>
        <GdpData />
      </div>
    </div>
  )
}

export default App
