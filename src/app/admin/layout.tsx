"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuthStore } from "@/lib/store";
import { Button } from "@/components/ui/button";
import { ArrowLeft } from "lucide-react";

export default function AdminLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const { token, user, _hydrated } = useAuthStore();

  useEffect(() => {
    if (!_hydrated) return;
    if (!token) router.replace("/login");
    else if (user && user.role !== "admin") router.replace("/dashboard");
  }, [token, user, _hydrated, router]);

  if (!_hydrated || !token || user?.role !== "admin") return null;

  return (
    <div className="min-h-screen bg-muted/20">
      <header className="border-b bg-card px-6 py-3 flex items-center gap-4">
        <Link href="/dashboard">
          <Button variant="ghost" size="sm" className="gap-2">
            <ArrowLeft className="h-4 w-4" />
            Dashboard
          </Button>
        </Link>
        <span className="font-semibold text-orange-600">Admin Panel</span>
      </header>
      <main>{children}</main>
    </div>
  );
}
