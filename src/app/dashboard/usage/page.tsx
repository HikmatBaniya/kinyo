"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { useAuthStore } from "@/lib/store";

interface UsageSummary {
  total_requests: number;
  total_characters: number;
  chars_used_this_period: number;
  chars_limit_this_period: number;
  chars_remaining: number;
  plan: string;
  period_reset_at: string | null;
}

interface SourceBreakdown {
  source: string;
  requests: number;
  characters: number;
}

interface UsageLog {
  id: string;
  characters_used: number;
  voice_id: string | null;
  model_id: string | null;
  output_format: string | null;
  source: string;
  status: string;
  created_at: string;
}

const SOURCE_LABEL: Record<string, string> = {
  dashboard: "Dashboard",
  api: "API key",
  api_batch: "API batch",
};

export default function UsagePage() {
  const user = useAuthStore((s) => s.user);

  const { data: summary } = useQuery<UsageSummary>({
    queryKey: ["usage-summary"],
    queryFn: async () => (await api.get("/usage/summary")).data,
  });

  const { data: breakdown = [] } = useQuery<SourceBreakdown[]>({
    queryKey: ["usage-breakdown"],
    queryFn: async () => (await api.get("/usage/breakdown")).data,
  });

  const { data: logs = [] } = useQuery<UsageLog[]>({
    queryKey: ["usage-logs"],
    queryFn: async () => (await api.get("/usage/logs?limit=100")).data,
  });

  const usedPct = summary
    ? Math.min((summary.chars_used_this_period / summary.chars_limit_this_period) * 100, 100)
    : 0;

  return (
    <div className="p-8 max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Usage</h1>
        <p className="text-muted-foreground text-sm">Character usage for current billing period</p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardContent className="pt-6">
            <p className="text-xs text-muted-foreground mb-1">Used this period</p>
            <p className="text-2xl font-bold">{summary?.chars_used_this_period?.toLocaleString() ?? "—"}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-xs text-muted-foreground mb-1">Remaining</p>
            <p className="text-2xl font-bold text-emerald-600">{summary?.chars_remaining?.toLocaleString() ?? "—"}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-xs text-muted-foreground mb-1">Total requests</p>
            <p className="text-2xl font-bold">{summary?.total_requests?.toLocaleString() ?? "—"}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <p className="text-xs text-muted-foreground mb-1">All-time chars</p>
            <p className="text-2xl font-bold">{summary?.total_characters?.toLocaleString() ?? "—"}</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Period usage</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex justify-between text-sm">
            <span>{summary?.chars_used_this_period?.toLocaleString() ?? 0} used</span>
            <span className="text-muted-foreground">{summary?.chars_limit_this_period?.toLocaleString()} limit</span>
          </div>
          <div className="h-3 rounded-full bg-muted overflow-hidden">
            <div
              className={`h-full transition-all ${usedPct > 90 ? "bg-destructive" : "bg-primary"}`}
              style={{ width: `${usedPct}%` }}
            />
          </div>
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>{usedPct.toFixed(1)}% used</span>
            {summary?.period_reset_at && (
              <span>Period started {new Date(summary.period_reset_at).toLocaleDateString()}</span>
            )}
          </div>
        </CardContent>
      </Card>

      {breakdown.length > 0 && (
        <Card>
          <CardHeader><CardTitle className="text-base">By source</CardTitle></CardHeader>
          <CardContent>
            <div className="space-y-3">
              {breakdown.map((b) => (
                <div key={b.source} className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge variant="outline">{SOURCE_LABEL[b.source] ?? b.source}</Badge>
                    <span className="text-sm text-muted-foreground">{b.requests} requests</span>
                  </div>
                  <span className="text-sm font-medium">{b.characters.toLocaleString()} chars</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader><CardTitle className="text-base">Request log</CardTitle></CardHeader>
        <CardContent>
          {logs.length === 0 ? (
            <p className="text-sm text-muted-foreground">No requests yet.</p>
          ) : (
            <div className="space-y-2">
              {logs.map((log) => (
                <div key={log.id} className="flex items-center justify-between py-2 border-b last:border-0 text-sm">
                  <div>
                    <span className="font-medium">{log.characters_used} chars</span>
                    <span className="text-muted-foreground ml-2">
                      {SOURCE_LABEL[log.source] ?? log.source}
                      {log.output_format && ` · ${log.output_format}`}
                    </span>
                    <p className="text-xs text-muted-foreground">{new Date(log.created_at).toLocaleString()}</p>
                  </div>
                  <Badge variant={log.status === "success" ? "success" : "destructive"}>
                    {log.status}
                  </Badge>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
