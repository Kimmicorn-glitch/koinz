"use client";

import { useEffect, useState } from "react";

import apiClient from "@/lib/api-client";
import { ProfileCard } from "@/components/profile-card";
import { RoleGuard } from "@/components/role-guard";
import {
  BankAccountCreate,
  BankAccountOut,
  CashoutResponse,
  LedgerEntryOut,
  PayoutResponse,
  TransactionList,
  WalletResponse,
} from "@/types/api";

export default function WorkerDashboardPage() {
  const [wallet, setWallet] = useState<WalletResponse | null>(null);
  const [accounts, setAccounts] = useState<BankAccountOut[]>([]);
  const [transactions, setTransactions] = useState<LedgerEntryOut[]>([]);
  const [bankName, setBankName] = useState("");
  const [accountHolder, setAccountHolder] = useState("");
  const [accountLast4, setAccountLast4] = useState("");
  const [payoutAmount, setPayoutAmount] = useState("");
  const [cashoutAmount, setCashoutAmount] = useState("");
  const [selectedAccount, setSelectedAccount] = useState<string>("");
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  useEffect(() => {
    apiClient
      .get<WalletResponse>("/payments/worker/wallet")
      .then((res) => setWallet(res.data))
      .catch(() => setWallet(null));

    apiClient
      .get<TransactionList>("/payments/worker/transactions")
      .then((res) => setTransactions(res.data.items))
      .catch(() => setTransactions([]));

    apiClient
      .get<BankAccountOut[]>("/payments/worker/bank-accounts")
      .then((res) => {
        setAccounts(res.data);
        if (res.data[0]) {
          setSelectedAccount(res.data[0].id);
        }
      })
      .catch(() => setAccounts([]));
  }, []);

  const refreshWallet = () => {
    apiClient
      .get<WalletResponse>("/payments/worker/wallet")
      .then((res) => setWallet(res.data))
      .catch(() => setWallet(null));
  };

  const handleAddBank = async () => {
    setStatusMsg(null);
    if (!bankName || !accountHolder || accountLast4.length !== 4) {
      setStatusMsg("Fill in bank name, account holder, and last 4 digits.");
      return;
    }
    try {
      const payload: BankAccountCreate = {
        bank_name: bankName,
        account_holder: accountHolder,
        account_number_last4: accountLast4,
      };
      const { data } = await apiClient.post<BankAccountOut>("/payments/worker/bank-accounts", payload);
      setAccounts((prev) => [data, ...prev]);
      setSelectedAccount(data.id);
      setBankName("");
      setAccountHolder("");
      setAccountLast4("");
      setStatusMsg("Bank account added.");
    } catch (err) {
      setStatusMsg("Failed to add bank account.");
    }
  };

  const handlePayout = async () => {
    setStatusMsg(null);
    const amount = Number(payoutAmount);
    if (!selectedAccount) {
      setStatusMsg("Select a bank account.");
      return;
    }
    if (!amount || amount <= 0) {
      setStatusMsg("Enter a valid payout amount.");
      return;
    }
    try {
      const { data } = await apiClient.post<PayoutResponse>("/payments/worker/payout", {
        bank_account_id: selectedAccount,
        amount_cents: Math.round(amount * 100),
      });
      setWallet((prev) => (prev ? { ...prev, balance_cents: data.wallet_balance_cents } : prev));
      setPayoutAmount("");
      setStatusMsg(`Payout ${data.status}.`);
    } catch (err) {
      setStatusMsg("Payout failed.");
    }
  };

  const handleCashout = async () => {
    setStatusMsg(null);
    const amount = Number(cashoutAmount);
    if (!amount || amount <= 0) {
      setStatusMsg("Enter a valid cash-out amount.");
      return;
    }
    try {
      const { data } = await apiClient.post<CashoutResponse>("/payments/worker/cashout", {
        amount_cents: Math.round(amount * 100),
      });
      setWallet((prev) => (prev ? { ...prev, balance_cents: data.wallet_balance_cents } : prev));
      setCashoutAmount("");
      setStatusMsg(`Voucher issued: ${data.voucher_code_masked}.`);
    } catch (err) {
      setStatusMsg("Cash-out failed.");
    }
  };

  return (
    <RoleGuard allow={["worker", "admin"]}>
      <main className="min-h-screen p-6 md:p-10">
        <section className="max-w-6xl mx-auto">
          <header className="mb-6">
            <h1 className="text-3xl font-semibold">Worker Dashboard</h1>
            <p className="text-neutral-600">Manage your wallet, payouts, and cash-out options.</p>
          </header>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            <ProfileCard name="Nomsa D." township="Khayelitsha" skills={["Electrical", "Safety", "Maintenance"]} />
            <ProfileCard name="Sipho K." township="Soweto" skills={["Plumbing", "Repairs", "Customer Service"]} />
            <ProfileCard name="Anele M." township="Mamelodi" skills={["Carpentry", "Finishing", "Measurement"]} />
          </div>

          <div className="mt-6 grid lg:grid-cols-3 gap-4">
            <article className="card p-6 animate-slideUp">
              <h3 className="text-base font-semibold">Wallet</h3>
              <p className="text-sm text-neutral-500 mt-2">Available balance</p>
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
              <h3 className="text-base font-semibold">Bank Accounts</h3>
              <input
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Bank name"
                value={bankName}
                onChange={(event) => setBankName(event.target.value)}
              />
              <input
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Account holder"
                value={accountHolder}
                onChange={(event) => setAccountHolder(event.target.value)}
              />
              <input
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Account last 4 digits"
                value={accountLast4}
                onChange={(event) => setAccountLast4(event.target.value)}
              />
              <button
                className="mt-3 w-full py-2 rounded-xl bg-[#B11226] text-white hover:bg-[#8e0d1e] transition-colors"
                onClick={handleAddBank}
              >
                Add Bank Account
              </button>
            </article>

            <article className="card p-6 animate-slideUp">
              <h3 className="text-base font-semibold">Withdraw</h3>
              <select
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                value={selectedAccount}
                onChange={(event) => setSelectedAccount(event.target.value)}
              >
                <option value="">Select bank account</option>
                {accounts.map((account) => (
                  <option key={account.id} value={account.id}>
                    {account.bank_name} •••• {account.account_number_last4}
                  </option>
                ))}
              </select>
              <input
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Payout amount (ZAR)"
                value={payoutAmount}
                onChange={(event) => setPayoutAmount(event.target.value)}
              />
              <button
                className="mt-3 w-full py-2 rounded-xl bg-[#B11226] text-white hover:bg-[#8e0d1e] transition-colors"
                onClick={handlePayout}
              >
                Send to Bank
              </button>
              <input
                className="mt-3 w-full rounded-xl border border-[#f4d5da] px-3 py-2"
                placeholder="Cash-out amount (ZAR)"
                value={cashoutAmount}
                onChange={(event) => setCashoutAmount(event.target.value)}
              />
              <button
                className="mt-3 w-full py-2 rounded-xl bg-[#B11226] text-white hover:bg-[#8e0d1e] transition-colors"
                onClick={handleCashout}
              >
                ATM Cash-out
              </button>
            </article>
          </div>

          <article className="card p-6 animate-slideUp mt-6">
            <h3 className="text-base font-semibold">Recent Transactions</h3>
            <div className="mt-4 space-y-2 text-sm text-neutral-700">
              {transactions.length === 0 ? (
                <p>No transactions yet.</p>
              ) : (
                transactions.slice(0, 6).map((entry) => (
                  <div key={entry.id} className="flex items-center justify-between border-b border-[#f4d5da] pb-2">
                    <div>
                      <p className="font-medium capitalize">{entry.kind}</p>
                      <p className="text-xs text-neutral-500">{new Date(entry.created_at).toLocaleString()}</p>
                    </div>
                    <div className="text-right">
                      <p className={entry.direction === "debit" ? "text-red-600" : "text-emerald-600"}>
                        {entry.direction === "debit" ? "-" : "+"}R {(entry.amount_cents / 100).toFixed(2)}
                      </p>
                      <p className="text-xs text-neutral-500">{entry.status}</p>
                    </div>
                  </div>
                ))
              )}
            </div>
          </article>

          {statusMsg ? <p className="mt-4 text-sm text-neutral-600">{statusMsg}</p> : null}
        </section>
      </main>
    </RoleGuard>
  );
}
