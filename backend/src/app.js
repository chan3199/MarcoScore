const express = require('express')
const cors = require('cors')
const buffettRoutes = require('./routes/buffettRoutes')

const app = express()

app.use(cors())
app.use(express.json())
app.use('/api/buffett', buffettRoutes) // 버핏지수 관련 API

module.exports = app
