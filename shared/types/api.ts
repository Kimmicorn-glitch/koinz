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

export interface ProfileResponse extends ProfileCreate {
  id: string;
  user_id: string;
}

export interface JobCreate {
  title: string;
  description: string;
  location: string;
  required_skills: string[];
}

export interface JobResponse extends JobCreate {
  id: string;
  employer_id: string;
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
