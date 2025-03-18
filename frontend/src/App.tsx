import React, { Suspense, lazy } from "react";

// ✅ 동적 임포트 (React Lazy 사용)
const BuffettIndex = lazy(() => import("./components/BuffettIndex"));
const EconomicIndicators = lazy(() => import("./components/EconomicIndicators"));
const EconomicChart = lazy(() => import("./components/EconomicChart"));

const App: React.FC = () => {
  return (
    <div className="w-full min-h-screen flex flex-col items-center bg-gray-100">
      {/* ✅ 컨텐츠 영역 */}
      <div className="w-full max-w-[1400px] px-8 py-6 flex flex-col items-center">
        
        {/* ✅ 제목 */}
        <h1 className="text-4xl font-bold text-indigo-700 text-center mb-10 w-full">
          MacroScore - 거시 경제 데이터
        </h1>

        {/* ✅ 주요 지표 */}
        <div className="w-full grid grid-cols-1 md:grid-cols-2 gap-6">
          <Suspense fallback={<p>📊 Buffett Index 로딩 중...</p>}>
            <div className="w-full">
              <BuffettIndex />
            </div>
          </Suspense>

          <Suspense fallback={<p>📌 경제 지표 로딩 중...</p>}>
            <div className="w-full">
              <EconomicIndicators />
            </div>
          </Suspense>
        </div>

        {/* ✅ 차트 전체 너비 활용 */}
        <div className="w-full flex justify-center mt-12">
          <Suspense fallback={<p>📈 차트 로딩 중...</p>}>
            <EconomicChart />
          </Suspense>
        </div>

      </div>
    </div>
  );
};

export default App;
