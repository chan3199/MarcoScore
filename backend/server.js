const express = require("express");
const dotenv = require("dotenv");
const economyRoutes = require("./routes/economyRoutes");

dotenv.config();
const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());
app.use("/api/economy", economyRoutes);

app.listen(PORT, () => {
  console.log(`✅ 서버 실행 중: http://localhost:${PORT}`);
});
