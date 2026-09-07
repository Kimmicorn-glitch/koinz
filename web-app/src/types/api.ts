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

export interface ProfileCreate {
  full_name: string;
  phone: string;
  township: string;
  skills: string[];
  resume_obs_key?: string | null;
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

export interface AnalyticsOverview {
  total_profiles: number;
  total_jobs: number;
  match_success_rate: number;
  monthly_placements: number[];
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

export interface PayoutRequest {
  bank_account_id: string;
  amount_cents: number;
}

export interface PayoutResponse {
  payout_id: string;
  status: string;
  provider_ref?: string | null;
  wallet_balance_cents: number;
}

export interface CashoutRequest {
  amount_cents: number;
}

export interface CashoutResponse {
  cashout_id: string;
  status: string;
  voucher_code_masked: string;
  expires_at: string;
  wallet_balance_cents: number;
}

export interface LedgerEntryOut {
  id: string;
  wallet_id: string;
  direction: string;
  kind: string;
  amount_cents: number;
  status: string;
  reference?: string | null;
  created_at: string;
}

export interface TransactionList {
  items: LedgerEntryOut[];
}
