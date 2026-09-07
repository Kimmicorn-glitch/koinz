"use client";

import { useEffect, useState } from "react";

import { AnalyticsChart } from "@/components/analytics-chart";
import { MatchRing } from "@/components/match-ring";
import { RoleGuard } from "@/components/role-guard";
import apiClient from "@/lib/api-client";
import { AnalyticsOverview, FundEmployerRequest, FundEmployerResponse, PayWorkerResponse, WalletResponse } from "@/types/api";

const fallback: AnalyticsOverview = {
  total_profiles: 3480,
  total_jobs: 247,
  match_success_rate: 0.82,
  monthly_placements: [12, 17, 21, 23, 26, 31],
};

export default function EmployerDashboardPage() {
  const [overview, setOverview] = useState<AnalyticsOverview>(fallback);
  const [wallet, setWallet] = useState<WalletResponse | null>(null);
  const [fundAmount, setFundAmount] = useState("");
  const [payWorkerId, setPayWorkerId] = useState("");
  const [payAmount, setPayAmount] = useState("");
  const [payNote, setPayNote] = useState("");
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .get<AnalyticsOverview>("/analytics/overview")
      .then((res) => setOverview(res.data))
      .catch(() => setOverview(fallback));

    apiClient
      .get<WalletResponse>("/payments/employer/wallet")
      .then((res) => setWallet(res.data))
      .catch(() => setWallet(null));
  }, []);

  const refreshWallet = () => {
    apiClient
      .get<WalletResponse>("/payments/employer/wallet")
      .then((res) => setWallet(res.data))
      .catch(() => setWallet(null));
  };

  const handleFund = async () => {
    setStatusMsg(null);
    const amount = Number(fundAmount);
    if (!amount || amount <= 0) {
      setStatusMsg("Enter a valid funding amount.");
      return;
    }
    try {
      const payload: FundEmployerRequest = { amount_cents: Math.round(amount * 100) };
      const { data } = await apiClient.post<FundEmployerResponse>("/payments/employer/fund", payload);
      setWallet((prev) => (prev ? { ...prev, balance_cents: data.wallet_balance_cents } : prev));
      setFundAmount("");
      setStatusMsg(`Funding ${data.status}.`);
    } catch (err) {
      setStatusMsg("Funding failed.");
    }
  };

  const handlePayWorker = async () => {
    setStatusMsg(null);
    const amount = Number(payAmount);
    if (!payWorkerId) {
      setStatusMsg("Enter a worker ID.");
      return;
    }
    if (!amount || amount <= 0) {
      setStatusMsg("Enter a valid payment amount.");
      return;
    }
    try {
      const { data } = await apiClient.post<PayWorkerResponse>("/payments/employer/pay-worker", {
        worker_id: payWorkerId,
        amount_cents: Math.round(amount * 100),
        reference: payNote || null,
      });
      setWallet((prev) => (prev ? { ...prev, balance_cents: data.employer_balance_cents } : prev));
      setPayWorkerId("");
      setPayAmount("");
      setPayNote("");
      setStatusMsg("Worker paid successfully.");
    } catch (err) {
      setStatusMsg("Worker payment failed.");
    }
  };

  return (
    <RoleGuard allow={["employer", "admin"]}>
      <main className="min-h-screen p-6 md:p-10">
        <section className="max-w-6xl mx-auto">
          <header className="mb-6">
            <h1 className="text-3xl font-semibold">Employer Dashboard</h1>
            <p className="text-neutral-600">Track job fill velocity and candidate quality across township regions.</p>
          </header>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <article className="card p-5 animate-slideUp">
              <p className="text-sm text-neutral-500">Worker Profiles</p>
              <p className="text-3xl font-semibold mt-2">{overview.total_profiles}</p>
            </article>
            <article className="card p-5 animate-slideUp">
              <p className="text-sm text-neutral-500">Active Jobs</p>
              <p className="text-3xl font-semibold mt-2">{overview.total_jobs}</p>
            </article>
            <article className="card p-5 animate-slideUp">
              <p className="text-sm text-neutral-500">Match Success</p>
              <p className="text-3xl font-semibold mt-2">{Math.round(overview.match_success_rate * 100)}%</p>
            </article>
            <article className="card p-5 animate-slideUp flex items-center justify-between">
              <div>
                <p className="text-sm text-neutral-500">Top Job Match</p>
                <p className="text-lg font-semibold mt-2">Electrical Assistant</p>
              </div>
              <MatchRing percentage={92} />
            </article>
          </div>

          <div className="mt-6 grid lg:grid-cols-3 gap-4">
            <div className="lg:col-span-2">
              <AnalyticsChart points={overview.monthly_placements} />
            </div>
            <article className="card p-6 animate-slideUp">
              <h3 className="text-base font-semibold">Priority Actions</h3>
              <ul className="mt-4 space-y-3 text-sm text-neutral-700">
                <li className="p-3 rounded-xl border border-[#f4d5da]">Post 4 urgent maintenance roles in Khayelitsha</li>
                <li className="p-3 rounded-xl border border-[#f4d5da]">Review 11 candidates with 80%+ match</li>
                <li className="p-3 rounded-xl border border-[#f4d5da]">Export weekly analytics for HR leadership</li>
              </ul>
            </article>
          </div>

          <div className="mt-6 grid lg:grid-cols-3 gap-4">
            <article className="card p-6 animate-slideUp">
              <h3 className="text-base font-semibold">Employer Wallet</h3>
              <p className="text-sm text-neutral-500 mt-2">Balance</p>
              <p className="text-3xl font-semibold mt-1">
                {wallet ? `R ${(wallet.balance_cents / 100).toFixed(2)}` : "R 0.00"}
              </p>
              <button
                className="mt-4 w-full py-2 rounded-xl bg-[#B11226] text-white hover:bg-[#8e0d1e] transition-colors"
                onClick={refreshWallet}
              >
                Refresh
              </button>
            </article>

            <article className="card p-6 animate-slideUp">
              <h3 className="text-base font-semibold">Fund Wallet</h3>
              <p className="text-sm text-neutral-500 mt-2">Top up with card or PayShap (mock).</p>
              <input
                className="mt-4 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Amount (ZAR)"
                value={fundAmount}
                onChange={(event) => setFundAmount(event.target.value)}
              />
              <button
                className="mt-3 w-full py-2 rounded-xl bg-[#B11226] text-white hover:bg-[#8e0d1e] transition-colors"
                onClick={handleFund}
              >
                Fund
              </button>
            </article>

            <article className="card p-6 animate-slideUp">
              <h3 className="text-base font-semibold">Pay Worker</h3>
              <p className="text-sm text-neutral-500 mt-2">Transfer from wallet to worker balance.</p>
              <input
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Worker ID"
                value={payWorkerId}
                onChange={(event) => setPayWorkerId(event.target.value)}
              />
              <input
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Amount (ZAR)"
                value={payAmount}
                onChange={(event) => setPayAmount(event.target.value)}
              />
              <input
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Reference (optional)"
                value={payNote}
                onChange={(event) => setPayNote(event.target.value)}
              />
              <button
                className="mt-3 w-full py-2 rounded-xl bg-[#B11226] text-white hover:bg-[#8e0d1e] transition-colors"
                onClick={handlePayWorker}
              >
                Pay Worker
              </button>
            </article>
          </div>

          {statusMsg ? <p className="mt-4 text-sm text-neutral-600">{statusMsg}</p> : null}
        </section>
      </main>
    </RoleGuard>
  );
}
