"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { api } from "@/lib/api";
import { useAuthStore } from "@/lib/store";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Users, Activity, FileText, TrendingUp } from "lucide-react";

interface Stats {
  total_users: number;
  total_requests: number;
  total_chars_processed: number;
  users_by_plan: Record<string, number>;
}

interface AdminUser {
  id: string;
  email: string;
  full_name: string | null;
  organization: string | null;
  plan: string;
  role: string;
  is_active: boolean;
  chars_used_this_period: number;
  created_at: string;
}

const PLANS = ["free", "starter", "pro", "enterprise"];

export default function AdminPage() {
  const router = useRouter();
  const user = useAuthStore((s) => s.user);
  const qc = useQueryClient();

  useEffect(() => {
    if (user && user.role !== "admin") router.replace("/dashboard");
  }, [user, router]);

  const { data: stats } = useQuery<Stats>({
    queryKey: ["admin-stats"],
    queryFn: async () => (await api.get("/admin/stats")).data,
  });

  const { data: users = [] } = useQuery<AdminUser[]>({
    queryKey: ["admin-users"],
    queryFn: async () => (await api.get("/admin/users?limit=100")).data,
  });

  const planMutation = useMutation({
    mutationFn: async ({ userId, plan }: { userId: string; plan: string }) =>
      api.patch(`/admin/users/${userId}/plan`, { plan }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-users"] });
      qc.invalidateQueries({ queryKey: ["admin-stats"] });
      toast.success("Plan updated");
    },
    onError: (err: any) => toast.error(err.response?.data?.detail ?? "Failed"),
  });

  const toggleMutation = useMutation({
    mutationFn: async (userId: string) => api.patch(`/admin/users/${userId}/toggle-active`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["admin-users"] });
      toast.success("User status updated");
    },
  });

  const STAT_CARDS = [
    { label: "Total users", value: stats?.total_users, icon: Users },
    { label: "Total requests", value: stats?.total_requests, icon: Activity },
    { label: "Chars processed", value: stats?.total_chars_processed?.toLocaleString(), icon: FileText },
    { label: "Paid users", value: (stats?.users_by_plan?.starter ?? 0) + (stats?.users_by_plan?.pro ?? 0) + (stats?.users_by_plan?.enterprise ?? 0), icon: TrendingUp },
  ];

  return (
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-2xl font-bold">Admin Dashboard</h1>
        <p className="text-muted-foreground text-sm">Platform overview and user management</p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {STAT_CARDS.map(({ label, value, icon: Icon }) => (
          <Card key={label}>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-muted-foreground">{label}</span>
                <Icon className="h-4 w-4 text-muted-foreground" />
              </div>
              <p className="text-2xl font-bold">{value ?? "—"}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {stats && (
        <Card>
          <CardHeader><CardTitle className="text-base">Users by plan</CardTitle></CardHeader>
          <CardContent>
            <div className="flex gap-6">
              {PLANS.map((p) => (
                <div key={p}>
                  <p className="text-xs text-muted-foreground uppercase">{p}</p>
                  <p className="text-xl font-bold">{stats.users_by_plan[p] ?? 0}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader><CardTitle className="text-base">Users</CardTitle></CardHeader>
        <CardContent>
          <div className="space-y-2">
            {users.map((u) => (
              <div key={u.id} className="flex items-center gap-4 p-3 border rounded-lg">
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{u.email}</p>
                  <p className="text-xs text-muted-foreground">
                    {u.organization ?? "No org"} · {u.chars_used_this_period.toLocaleString()} chars used
                  </p>
                </div>
                <Badge variant={u.is_active ? "success" : "destructive"}>
                  {u.is_active ? "active" : "disabled"}
                </Badge>
                <Select
                  value={u.plan}
                  onValueChange={(plan) => planMutation.mutate({ userId: u.id, plan })}
                >
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {PLANS.map((p) => (
                      <SelectItem key={p} value={p}>{p}</SelectItem>
                    ))}
                  </SelectContent>
                </Select>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => toggleMutation.mutate(u.id)}
                  disabled={u.id === user?.id}
                >
                  {u.is_active ? "Disable" : "Enable"}
                </Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
