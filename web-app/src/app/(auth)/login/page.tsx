"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import apiClient from "@/lib/api-client";
import { storeAuth } from "@/lib/auth";
import { TokenResponse } from "@/types/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("employer@localhands.com");
  const [password, setPassword] = useState("ChangeMe123!");
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);

    try {
      const { data } = await apiClient.post<TokenResponse>("/auth/login", { email, password });
      storeAuth(data.access_token, data.role);
      if (data.role === "employer" || data.role === "admin") {
        router.push("/employer/dashboard");
        return;
      }
      router.push("/worker/dashboard");
    } catch {
      setError("Login failed. Check credentials.");
    }
  }

  return (
    <main className="min-h-screen grid place-items-center p-6">
      <form onSubmit={onSubmit} className="card w-full max-w-md p-8 animate-slideUp">
        <h1 className="text-2xl font-semibold">Sign In</h1>
        <p className="text-sm text-neutral-600 mt-1">Use role-aware access for worker and employer portals.</p>
        <label className="block mt-6 text-sm">Email</label>
        <input className="mt-1 w-full border border-[#f2ccd3] rounded-2xl px-4 py-3" value={email} onChange={(e) => setEmail(e.target.value)} />
        <label className="block mt-4 text-sm">Password</label>
        <input
          type="password"
          className="mt-1 w-full border border-[#f2ccd3] rounded-2xl px-4 py-3"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error ? <p className="text-sm text-[#B11226] mt-4">{error}</p> : null}
        <button className="w-full mt-6 bg-[#B11226] text-white rounded-2xl py-3 hover:bg-[#8e0d1e] transition-colors">Continue</button>
      </form>
    </main>
  );
}
