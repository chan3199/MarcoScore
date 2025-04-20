import Plot from 'react-plotly.js'
import { useEffect, useState } from 'react'
import axios from 'axios'

interface BuffettIndexData {
  date: string
  buffett_index: number
}

export default function BuffettChart() {
  const [data, setData] = useState<BuffettIndexData[]>([])

  useEffect(() => {
    axios
      .get('/api/buffett-index')
      .then((res) => setData(res.data))
      .catch(console.error)
  }, [])

  const dates = data.map((d) => d.date)
  const values = data.map((d) => d.buffett_index * 100) // % 단위

  return (
    <div className="w-full h-[60vh]">
      <Plot
        data={[
          {
            x: dates,
            y: values,
            type: 'scatter',
            mode: 'lines',
            name: 'Buffett Index (%)',
            line: { color: 'royalblue', width: 1 },
          },
        ]}
        layout={{
          title: 'Buffett Index (%) Over Time',
          xaxis: { title: 'Date' },
          yaxis: {
            title: 'Buffett Index (%)',
            tickformat: '.1f',
            ticksuffix: '%',
          },
          margin: { l: 60, r: 30, t: 40, b: 40 },
        }}
        style={{ width: '100%', height: '100%' }}
        useResizeHandler
      />
    </div>
  )
}
