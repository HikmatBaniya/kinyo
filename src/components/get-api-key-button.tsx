"use client";

import Link from "next/link";
import { useAuthStore } from "@/lib/store";

export function GetApiKeyButton() {
  const { token, _hydrated } = useAuthStore();

  const href = _hydrated && token ? "/dashboard/keys" : "/register";

  return (
    <Link href={href} className="text-sm text-muted-foreground hover:text-foreground">
      Get API key →
    </Link>
  );
}
