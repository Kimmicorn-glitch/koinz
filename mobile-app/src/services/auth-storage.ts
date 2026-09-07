import * as SecureStore from "expo-secure-store";

import { UserRole } from "@/types/api";

const TOKEN_KEY = "lh_token";
const ROLE_KEY = "lh_role";

export async function saveAuth(token: string, role: UserRole): Promise<void> {
  await SecureStore.setItemAsync(TOKEN_KEY, token);
  await SecureStore.setItemAsync(ROLE_KEY, role);
}

export async function getToken(): Promise<string | null> {
  return SecureStore.getItemAsync(TOKEN_KEY);
}

export async function getRole(): Promise<UserRole | null> {
  const role = await SecureStore.getItemAsync(ROLE_KEY);
  return role as UserRole | null;
}

export async function clearAuth(): Promise<void> {
  await SecureStore.deleteItemAsync(TOKEN_KEY);
  await SecureStore.deleteItemAsync(ROLE_KEY);
}
