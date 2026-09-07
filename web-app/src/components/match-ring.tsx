"use client";

interface MatchRingProps {
  percentage: number;
}

export function MatchRing({ percentage }: MatchRingProps) {
  const safe = Math.max(0, Math.min(100, percentage));
  const angle = (safe / 100) * 360;

  return (
    <div
      className="relative h-24 w-24 rounded-full"
      style={{
        background: `conic-gradient(#B11226 ${angle}deg, #F9D9DE ${angle}deg)`,
      }}
    >
      <div className="absolute inset-2 rounded-full bg-white flex items-center justify-center text-sm font-semibold text-[#B11226]">
        {safe}%
      </div>
    </div>
  );
}
