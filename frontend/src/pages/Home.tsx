// src/pages/Home.tsx
import BuffettChart from '../components/chart/BuffettChart'

export default function Home() {
  return (
    <div className="px-4 py-8 max-w-6xl mx-auto">
      <h1 className="text-2xl font-semibold mb-4">
        📊 Buffett Index Dashboard
      </h1>
      <BuffettChart />
    </div>
  )
}
