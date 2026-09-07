import { NextRequest, NextResponse } from "next/server";

const protectedRoutes = ["/employer", "/worker"];

export function middleware(request: NextRequest) {
  const path = request.nextUrl.pathname;

  if (!protectedRoutes.some((prefix) => path.startsWith(prefix))) {
    return NextResponse.next();
  }

  const token = request.cookies.get("lh_token")?.value;
  const role = request.cookies.get("lh_role")?.value;

  if (!token || !role) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  if (path.startsWith("/employer") && !["employer", "admin"].includes(role)) {
    return NextResponse.redirect(new URL("/worker/dashboard", request.url));
  }

  if (path.startsWith("/worker") && !["worker", "admin"].includes(role)) {
    return NextResponse.redirect(new URL("/employer/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/employer/:path*", "/worker/:path*"],
};
