const express = require('express')
const router = express.Router()
const { getBuffettIndex } = require('../controllers/buffettController')

router.get('/', getBuffettIndex)

module.exports = router
