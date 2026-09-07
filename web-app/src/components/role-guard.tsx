"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import { getRole, getToken } from "@/lib/auth";
import { UserRole } from "@/types/api";

export function RoleGuard({ children, allow }: { children: React.ReactNode; allow: UserRole[] }) {
  const router = useRouter();

  useEffect(() => {
    const token = getToken();
    const role = getRole();

    if (!token || !role || !allow.includes(role)) {
      router.replace("/login");
    }
  }, [allow, router]);

  return <>{children}</>;
}
