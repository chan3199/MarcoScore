import React, { useEffect, useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api"; // ✅ API 주소 설정

const BuffettIndex: React.FC = () => {
  const [buffettIndex, setBuffettIndex] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // ✅ API에서 Buffett Index 데이터 가져오기
  const fetchData = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await axios.get(`${API_BASE_URL}/economy/buffett-index`);
      console.log("📌 API 응답 데이터:", response.data);

      if (!response.data.success || response.data.data.length === 0) {
        setError("데이터가 없습니다.");
        return;
      }

      // ✅ 최신 데이터 가져오기
      const latestBuffett = response.data.data[0].buffettIndex;
      setBuffettIndex(latestBuffett);
    } catch (error) {
      console.error("❌ Buffett Index 데이터 로딩 실패:", error);
      setError("데이터를 불러오는 중 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // ✅ 컴포넌트가 처음 마운트될 때 데이터 가져오기
  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="bg-white shadow-md rounded-lg p-4">
      <h2 className="text-xl font-bold text-indigo-700 flex items-center">
        📊 Buffett Index
      </h2>

      {/* ✅ 로딩 중 */}
      {loading && <p className="text-gray-500">📡 데이터 로딩 중...</p>}

      {/* ✅ 오류 발생 */}
      {error && <p className="text-red-500">{error}</p>}

      {/* ✅ 데이터 표시 */}
      {!loading && !error && buffettIndex !== null && (
        <p className="text-3xl font-semibold text-gray-800">{buffettIndex.toFixed(2)}</p>
      )}

      {/* ✅ 수동 데이터 갱신 버튼 */}
      <button
        onClick={fetchData}
        className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-500"
      >
        🔄 데이터 새로고침
      </button>
    </div>
  );
};

export default BuffettIndex;
