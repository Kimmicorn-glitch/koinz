interface AnalyticsChartProps {
  points: number[];
}

export function AnalyticsChart({ points }: AnalyticsChartProps) {
  const max = Math.max(...points, 1);

  return (
    <div className="card p-6 animate-slideUp">
      <h3 className="text-base font-semibold">Monthly Placements</h3>
      <div className="mt-6 grid grid-cols-6 gap-3 items-end h-40">
        {points.map((point, idx) => (
          <div
            key={`${point}-${idx}`}
            className="rounded-t-xl bg-gradient-to-t from-[#B11226] to-[#EE425E] transition-all duration-500"
            style={{ height: `${Math.max((point / max) * 100, 10)}%` }}
            title={`Month ${idx + 1}: ${point}`}
          />
        ))}
      </div>
    </div>
  );
}
