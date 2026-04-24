"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import { useQuery, useMutation } from "@tanstack/react-query";
import { toast } from "sonner";
import { Check, ExternalLink, Zap } from "lucide-react";
import { api } from "@/lib/api";
import { useAuthStore, PLAN_LIMITS, PLAN_MAX_KEYS, PLAN_PRICE } from "@/lib/store";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

const PLANS = [
  {
    key: "free",
    name: "Free",
    features: [`${(10_000).toLocaleString()} chars/month`, "1 API key"],
  },
  {
    key: "starter",
    name: "Starter",
    features: [`${(100_000).toLocaleString()} chars/month`, "3 API keys", "Email support"],
  },
  {
    key: "pro",
    name: "Pro",
    features: [`${(500_000).toLocaleString()} chars/month`, "10 API keys", "Priority support"],
  },
  {
    key: "enterprise",
    name: "Enterprise",
    features: [`${(10_000_000).toLocaleString()} chars/month`, "50 API keys", "SLA + dedicated support"],
  },
];

export default function BillingPage() {
  const user = useAuthStore((s) => s.user);
  const searchParams = useSearchParams();
  const [checkoutLoading, setCheckoutLoading] = useState<string | null>(null);

  useEffect(() => {
    if (searchParams.get("success") === "1") toast.success("Subscription activated!");
    if (searchParams.get("canceled") === "1") toast.info("Checkout canceled");
  }, [searchParams]);

  const checkout = async (plan: string) => {
    setCheckoutLoading(plan);
    try {
      const res = await api.post("/billing/checkout", { plan });
      window.location.href = res.data.url;
    } catch (err: any) {
      toast.error(err.response?.data?.detail ?? "Checkout failed");
      setCheckoutLoading(null);
    }
  };

  const portal = async () => {
    try {
      const res = await api.post("/billing/portal");
      window.location.href = res.data.url;
    } catch (err: any) {
      toast.error(err.response?.data?.detail ?? "Could not open billing portal");
    }
  };

  const limit = PLAN_LIMITS[user?.plan ?? "free"];
  const usedPct = user ? Math.min((user.chars_used_this_period / limit) * 100, 100) : 0;

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Billing & Plan</h1>
        <p className="text-muted-foreground text-sm">Manage your subscription and usage</p>
      </div>

      {/* Current plan */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-base">Current plan</CardTitle>
            <Badge>{user?.plan?.toUpperCase()}</Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <p className="text-muted-foreground">Characters used</p>
              <p className="font-semibold text-lg">{user?.chars_used_this_period?.toLocaleString() ?? 0}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Monthly limit</p>
              <p className="font-semibold text-lg">{limit.toLocaleString()}</p>
            </div>
            <div>
              <p className="text-muted-foreground">API keys allowed</p>
              <p className="font-semibold text-lg">{PLAN_MAX_KEYS[user?.plan ?? "free"]}</p>
            </div>
          </div>
          <div className="space-y-1">
            <div className="h-2 rounded-full bg-muted overflow-hidden">
              <div className="h-full bg-primary transition-all" style={{ width: `${usedPct}%` }} />
            </div>
            <p className="text-xs text-muted-foreground">{usedPct.toFixed(1)}% of monthly limit used</p>
          </div>
          {user?.plan !== "free" && (
            <Button variant="outline" size="sm" onClick={portal} className="gap-2">
              <ExternalLink className="h-4 w-4" />
              Manage billing in Stripe
            </Button>
          )}
        </CardContent>
      </Card>

      {/* Upgrade */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {PLANS.filter((p) => p.key !== user?.plan).map((plan) => (
          <Card key={plan.key} className={plan.key === "pro" ? "border-primary" : ""}>
            <CardHeader>
              {plan.key === "pro" && <Badge className="w-fit mb-1">Recommended</Badge>}
              <CardTitle className="text-base">{plan.name}</CardTitle>
              <CardDescription>
                <span className="text-2xl font-bold text-foreground">${PLAN_PRICE[plan.key]}</span>
                {PLAN_PRICE[plan.key] > 0 && <span>/month</span>}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <ul className="space-y-1.5">
                {plan.features.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-sm">
                    <Check className="h-3.5 w-3.5 text-primary" />
                    {f}
                  </li>
                ))}
              </ul>
              {plan.key === "enterprise" ? (
                <Button variant="outline" className="w-full" asChild>
                  <a href="mailto:dev@nepawholesale.com">Contact us</a>
                </Button>
              ) : (
                <Button
                  className="w-full gap-2"
                  variant={plan.key === "pro" ? "default" : "outline"}
                  onClick={() => checkout(plan.key)}
                  disabled={checkoutLoading === plan.key}
                >
                  <Zap className="h-4 w-4" />
                  {checkoutLoading === plan.key ? "Redirecting…" : `Upgrade to ${plan.name}`}
                </Button>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
