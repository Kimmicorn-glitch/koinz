import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <section className="w-full max-w-4xl card p-8 md:p-12 grid md:grid-cols-2 gap-8 animate-slideUp">
        <div>
          <p className="text-xs tracking-[0.2em] text-[#B11226]">LOCAL HANDS 2.0</p>
          <h1 className="text-4xl font-semibold mt-3">AI-Powered Township Employment Intelligence</h1>
          <p className="mt-4 text-neutral-600">
            Production-grade platform for worker-employer matching across web and mobile.
          </p>
          <div className="mt-8 flex gap-3">
            <Link href="/login" className="px-5 py-3 rounded-2xl bg-[#B11226] text-white hover:bg-[#8e0d1e] transition-colors">
              Sign In
            </Link>
            <Link href="/employer/dashboard" className="px-5 py-3 rounded-2xl border border-[#f3c4cd] hover:border-[#B11226] transition-colors">
              View Dashboard
            </Link>
          </div>
        </div>
        <div className="rounded-2xl bg-gradient-to-br from-[#B11226] to-[#EE425E] p-8 text-white">
          <div className="grid grid-cols-2 gap-4">
            <div className="rounded-xl border border-white/30 p-4">
              <p className="text-xs">Workers</p>
              <p className="text-2xl font-semibold">3,480</p>
            </div>
            <div className="rounded-xl border border-white/30 p-4">
              <p className="text-xs">Active Jobs</p>
              <p className="text-2xl font-semibold">247</p>
            </div>
            <div className="rounded-xl border border-white/30 p-4 col-span-2">
              <p className="text-xs">Placement Efficiency</p>
              <p className="text-2xl font-semibold">82%</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
