const express = require("express")
const cors = require("cors")

const economyRoutes = require("./routes/economyRoutes") // ✅ 경로 확인!

const app = express()
app.use(cors())
app.use(express.json())

// API 라우트 연결
app.use("/api/economy", economyRoutes) // ✅ 반드시 존재해야 함!

const PORT = process.env.PORT || 5000
app.listen(PORT, () => {
  console.log(`✅ 서버 실행 중: http://localhost:${PORT}`)
})
