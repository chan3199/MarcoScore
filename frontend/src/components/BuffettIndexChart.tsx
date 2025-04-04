import Plot from 'react-plotly.js';
import { useEffect, useState } from 'react';
import Papa from 'papaparse';

interface BuffettData {
  date: string;
  buffett_index: number;
}

export default function BuffettIndexChart() {
  const [data, setData] = useState<BuffettData[]>([]);

  useEffect(() => {
    fetch('/data/buffett_index.csv')
      .then(res => res.text())
      .then(text => {
        const parsed = Papa.parse(text, { header: true });
        setData(parsed.data as BuffettData[]);
      });
  }, []);

  const dates = data.map(d => d.date);
  const values = data.map(d => (d.buffett_index * 100)); 

  return (
    <div style={{ width: "90vw", height: "60vh", margin: '0 auto' }}>
      <Plot
        data={[
          {
            x: dates,
            y: values,
            type: 'scatter',
            mode: 'lines',
            name: 'Buffett Index',
            line: { color: 'royalblue', width: 1 }, // 선 두께 조정
            hovertemplate: '%{x|%Y-%m-%d}<br>%{y:.1f}%',
          }
        ]}
        layout={{
          title: '📈 Buffett Index Over Time',
          autosize: true,
          xaxis: { title: 'Date' },
          yaxis: {
            title: 'Buffett Index (%)',
            tickformat: '.1f', 
            ticksuffix: '%',
          },
          margin: { l: 60, r: 30, t: 50, b: 40 },
        }}
        useResizeHandler
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}
