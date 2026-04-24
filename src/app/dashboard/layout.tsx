"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ThemeToggle } from "@/components/theme-toggle";
import { SworLogo } from "@/components/logo";
import { Mic, Key, BarChart2, LogOut, CreditCard, ShieldCheck, BookOpen } from "lucide-react";

const NAV = [
  { href: "/dashboard", label: "Playground", icon: Mic },
  { href: "/dashboard/keys", label: "API Keys", icon: Key },
  { href: "/dashboard/usage", label: "Usage", icon: BarChart2 },
  { href: "/dashboard/billing", label: "Billing", icon: CreditCard },
  { href: "/dashboard/docs", label: "Docs", icon: BookOpen },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const { token, user, clearAuth, _hydrated } = useAuthStore();

  useEffect(() => {
    if (_hydrated && !token) router.replace("/login");
  }, [token, _hydrated, router]);

  if (!_hydrated) return null;

  return (
    <div className="flex min-h-screen">
      <aside className="w-56 border-r bg-card flex flex-col">
        <div className="px-4 py-4 border-b space-y-2">
          <SworLogo size="sm" />
          <p className="text-xs text-muted-foreground truncate">{user?.email}</p>
          <Badge variant="secondary" className="text-xs">{user?.plan?.toUpperCase()}</Badge>
        </div>
        <nav className="flex-1 px-3 py-4 space-y-1">
          {NAV.map(({ href, label, icon: Icon }) => (
            <Link key={href} href={href}>
              <Button
                variant={pathname === href ? "secondary" : "ghost"}
                className="w-full justify-start gap-2"
              >
                <Icon className="h-4 w-4" />
                {label}
              </Button>
            </Link>
          ))}
          {user?.role === "admin" && (
            <Link href="/admin">
              <Button
                variant={pathname.startsWith("/admin") ? "secondary" : "ghost"}
                className="w-full justify-start gap-2 text-orange-600"
              >
                <ShieldCheck className="h-4 w-4" />
                Admin
              </Button>
            </Link>
          )}
        </nav>
        <div className="px-3 py-4 border-t space-y-1">
          <div className="flex items-center justify-between px-2">
            <span className="text-xs text-muted-foreground">Theme</span>
            <ThemeToggle />
          </div>
          <Button
            variant="ghost"
            className="w-full justify-start gap-2 text-muted-foreground"
            onClick={() => { clearAuth(); router.push("/login"); }}
          >
            <LogOut className="h-4 w-4" />
            Sign out
          </Button>
        </div>
      </aside>
      <main className="flex-1 overflow-auto bg-muted/20">{children}</main>
    </div>
  );
}
