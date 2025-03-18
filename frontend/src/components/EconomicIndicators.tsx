import React, { useEffect, useState } from 'react'
import axios from 'axios'

interface Indicator {
  date: string
  value: string
}

const EconomicIndicators: React.FC = () => {
  const [unemployment, setUnemployment] = useState<Indicator[]>([])
  const [inflation, setInflation] = useState<Indicator[]>([])
  const [interestRate, setInterestRate] = useState<Indicator[]>([])
  const [sp500, setSp500] = useState<Indicator[]>([])
  

  useEffect(() => {
    axios.get<{ success: boolean; data: Indicator[] }>('http://localhost:5000/api/economy/unemployment')
      .then(res => setUnemployment(res.data.data))

    axios.get<{ success: boolean; data: Indicator[] }>('http://localhost:5000/api/economy/inflation')
      .then(res => setInflation(res.data.data))

    axios.get<{ success: boolean; data: Indicator[] }>('http://localhost:5000/api/economy/interest-rate')
      .then(res => setInterestRate(res.data.data))

    axios.get<{ success: boolean; data: Indicator[] }>('http://localhost:5000/api/economy/sp500')
      .then(res => setSp500(res.data.data))
      
  }, [])

  return (
    <div>
      <h2>Economic Indicators</h2>
      <p>Unemployment: {unemployment.length > 0 && unemployment[0].value}</p>
      <p>Inflation: {inflation.length > 0 && inflation[0].value}</p>
      <p>Interest Rate: {interestRate.length > 0 && interestRate[0].value}</p>
      <p>S&P 500: {sp500.length > 0 && sp500[0].value}</p>
    </div>
  )
}

export default EconomicIndicators
