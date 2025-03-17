const express = require('express')
const cors = require('cors')
const economyRoutes = require('./routes/economyRoutes')

require('dotenv').config()

const app = express()
app.use(cors())
app.use(express.json())

// API 라우트 추가
app.use('/api/economy', economyRoutes)

const PORT = process.env.PORT || 5000
app.listen(PORT, () => console.log(`🚀 Server running on port ${PORT}`))
