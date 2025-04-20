const path = require('path')
const fs = require('fs')

const getBuffettIndex = (req, res) => {
  const filePath = path.join(__dirname, '../data/buffett_index.csv')
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('❌ Error reading CSV:', err)
      return res.status(500).json({ error: 'Failed to read CSV' })
    }
    res.type('text/csv').send(data)
  })
}

module.exports = { getBuffettIndex }
