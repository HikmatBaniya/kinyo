"use client";

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { Plus, Trash2, Copy, Eye, EyeOff } from "lucide-react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface ApiKey {
  id: string;
  key_prefix: string;
  name: string | null;
  is_active: boolean;
  requests_count: number;
  created_at: string;
  last_used_at: string | null;
}

export default function KeysPage() {
  const qc = useQueryClient();
  const [name, setName] = useState("");
  const [newKey, setNewKey] = useState<string | null>(null);
  const [showKey, setShowKey] = useState(false);

  const { data: keys = [], isLoading } = useQuery<ApiKey[]>({
    queryKey: ["api-keys"],
    queryFn: async () => (await api.get("/keys")).data,
  });

  const createMutation = useMutation({
    mutationFn: async () => (await api.post("/keys", { name: name || null })).data,
    onSuccess: (data) => {
      setNewKey(data.key);
      setName("");
      qc.invalidateQueries({ queryKey: ["api-keys"] });
      toast.success("API key created — copy it now, won't be shown again");
    },
    onError: (err: any) => toast.error(err.response?.data?.detail ?? "Failed to create key"),
  });

  const revokeMutation = useMutation({
    mutationFn: async (id: string) => api.delete(`/keys/${id}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["api-keys"] });
      toast.success("Key revoked");
    },
    onError: (err: any) => toast.error(err.response?.data?.detail ?? "Failed to revoke"),
  });

  const copy = (val: string) => {
    navigator.clipboard.writeText(val);
    toast.success("Copied to clipboard");
  };

  return (
    <div className="p-8 max-w-3xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold">API Keys</h1>
        <p className="text-muted-foreground text-sm">Keys for external integrations via X-API-Key header</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">New key</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="space-y-1">
            <Label>Name (optional)</Label>
            <Input
              placeholder="e.g. production-app"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <Button onClick={() => createMutation.mutate()} disabled={createMutation.isPending} className="gap-2">
            <Plus className="h-4 w-4" />
            {createMutation.isPending ? "Creating…" : "Create key"}
          </Button>
        </CardContent>
      </Card>

      {newKey && (
        <Card className="border-emerald-200 bg-emerald-50">
          <CardHeader>
            <CardTitle className="text-base text-emerald-800">New key — copy now</CardTitle>
            <CardDescription className="text-emerald-700">This is shown once. Store it securely.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-2">
            <div className="flex items-center gap-2">
              <code className="flex-1 text-xs bg-white border rounded px-3 py-2 font-mono break-all">
                {showKey ? newKey : "swor_live_••••••••••••••••••••••••••••••••••••••"}
              </code>
              <Button variant="ghost" size="icon" onClick={() => setShowKey((s) => !s)}>
                {showKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </Button>
              <Button variant="ghost" size="icon" onClick={() => copy(newKey)}>
                <Copy className="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Active keys</CardTitle>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <p className="text-sm text-muted-foreground">Loading…</p>
          ) : keys.length === 0 ? (
            <p className="text-sm text-muted-foreground">No keys yet.</p>
          ) : (
            <div className="space-y-3">
              {keys.map((k) => (
                <div key={k.id} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <code className="text-sm font-mono">{k.key_prefix}…</code>
                      {k.name && <Badge variant="secondary">{k.name}</Badge>}
                      {k.is_active ? <Badge variant="success">active</Badge> : <Badge variant="destructive">revoked</Badge>}
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {k.requests_count} requests · created {new Date(k.created_at).toLocaleDateString()}
                      {k.last_used_at && ` · last used ${new Date(k.last_used_at).toLocaleDateString()}`}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="text-destructive hover:text-destructive"
                    onClick={() => revokeMutation.mutate(k.id)}
                    disabled={!k.is_active}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
