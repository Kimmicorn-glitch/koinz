export type UserRole = "worker" | "employer" | "admin";

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: "bearer";
  role: UserRole;
}

export interface JobCreate {
  title: string;
  description: string;
  location: string;
  required_skills: string[];
}

export interface MatchItem {
  profile_id: string;
  score: number;
  matched_skills: string[];
  missing_skills: string[];
}

export interface MatchResponse {
  job_id: string;
  matches: MatchItem[];
}

export interface WalletResponse {
  id: string;
  user_id: string;
  currency: string;
  balance_cents: number;
}

export interface FundEmployerRequest {
  amount_cents: number;
  reference?: string | null;
}

export interface FundEmployerResponse {
  funding_id: string;
  status: string;
  wallet_balance_cents: number;
}

export interface PayWorkerRequest {
  worker_id: string;
  amount_cents: number;
  reference?: string | null;
}

export interface PayWorkerResponse {
  transfer_id: string;
  employer_balance_cents: number;
}

export interface BankAccountCreate {
  bank_name: string;
  account_holder: string;
  account_number_last4: string;
}

export interface BankAccountOut {
  id: string;
  bank_name: string;
  account_holder: string;
  account_number_last4: string;
  verified: boolean;
}

export interface PayoutResponse {
  payout_id: string;
  status: string;
  provider_ref?: string | null;
  wallet_balance_cents: number;
}

export interface CashoutResponse {
  cashout_id: string;
  status: string;
  voucher_code_masked: string;
  expires_at: string;
  wallet_balance_cents: number;
}
