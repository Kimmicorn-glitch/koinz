import { UserRole } from "@/types/api";

const TOKEN_KEY = "lh_token";
const ROLE_KEY = "lh_role";

export function storeAuth(token: string, role: UserRole): void {
  if (typeof window === "undefined") return;

  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(ROLE_KEY, role);
  document.cookie = `${TOKEN_KEY}=${token}; path=/`;
  document.cookie = `${ROLE_KEY}=${role}; path=/`;
}

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function getRole(): UserRole | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(ROLE_KEY) as UserRole | null;
}

export function clearAuth(): void {
  if (typeof window === "undefined") return;
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(ROLE_KEY);
  document.cookie = `${TOKEN_KEY}=; Max-Age=0; path=/`;
  document.cookie = `${ROLE_KEY}=; Max-Age=0; path=/`;
}
