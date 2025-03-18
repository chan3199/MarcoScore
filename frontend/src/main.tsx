import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

// ✅ React.StrictMode 제거 (테스트용)
ReactDOM.createRoot(document.getElementById('root')!).render(
  <App />
)
