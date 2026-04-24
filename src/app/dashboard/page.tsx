"use client";

import { useState, useRef, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { toast } from "sonner";
import { Play, Loader2, Download, Volume2, RefreshCw } from "lucide-react";
import { api } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { useAuthStore, PLAN_LIMITS } from "@/lib/store";

const OUTPUT_FORMATS = [
  { value: "mp3_44100_128", label: "MP3 128kbps" },
  { value: "mp3_44100_192", label: "MP3 192kbps (high)" },
  { value: "pcm_44100", label: "PCM 44.1kHz" },
  { value: "ulaw_8000", label: "μ-law 8kHz (telephony)" },
];

const SAMPLE_TEXTS = [
  "नमस्ते! स्वर प्लेटफर्ममा स्वागत छ।",
  "नेपाली भाषा विश्वको सुन्दर भाषाहरूमध्ये एक हो।",
  "आजको मौसम राम्रो छ। बाहिर घुम्न जाऔं।",
  "धन्यवाद! तपाईंको सहयोगको लागि हार्दिक आभार।",
];

export default function PlaygroundPage() {
  const user = useAuthStore((s) => s.user);
  const [text, setText] = useState(SAMPLE_TEXTS[0]);
  const [voiceId, setVoiceId] = useState<string>("");
  const [outputFormat, setOutputFormat] = useState("mp3_44100_128");
  const [loading, setLoading] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const audioRef = useRef<HTMLAudioElement>(null);

  const { data: voices = [] } = useQuery({
    queryKey: ["voices"],
    queryFn: async () => {
      const res = await api.get("/tts/voices");
      return res.data as { voice_id: string; name: string }[];
    },
  });

  const { data: health } = useQuery({
    queryKey: ["el-health"],
    queryFn: async () => (await api.get("/tts/health")).data,
    retry: false,
  });

  const { data: summary, refetch: refetchSummary } = useQuery({
    queryKey: ["usage-summary"],
    queryFn: async () => (await api.get("/usage/summary")).data,
  });

  const synthesize = async () => {
    if (!text.trim()) return;
    setLoading(true);
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioUrl(null);
    try {
      const res = await api.post(
        "/tts/synthesize",
        { text, voice_id: voiceId || null, model_id: "eleven_multilingual_v2", output_format: outputFormat },
        { responseType: "blob" }
      );
      const mime = outputFormat.startsWith("mp3") ? "audio/mpeg" : "audio/wav";
      const url = URL.createObjectURL(new Blob([res.data], { type: mime }));
      setAudioUrl(url);
      refetchSummary();
    } catch (err: any) {
      const detail = err.response?.data?.detail ?? "Synthesis failed";
      toast.error(detail);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (audioUrl && audioRef.current) audioRef.current.play().catch(() => {});
  }, [audioUrl]);

  const download = () => {
    if (!audioUrl) return;
    const ext = outputFormat.startsWith("mp3") ? "mp3" : outputFormat.startsWith("pcm") ? "wav" : "au";
    const a = document.createElement("a");
    a.href = audioUrl;
    a.download = `swor-audio.${ext}`;
    a.click();
  };

  const limit = PLAN_LIMITS[user?.plan ?? "free"];
  const used = summary?.chars_used_this_period ?? 0;
  const usedPct = Math.min((used / limit) * 100, 100);

  return (
    <div className="p-8 max-w-3xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">TTS Playground</h1>
          <p className="text-muted-foreground text-sm">Nepali text-to-speech</p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="secondary">{user?.plan?.toUpperCase()}</Badge>
          {health && (
            <Badge variant="outline" className="text-xs">
              EL: {health.character_count?.toLocaleString()} / {health.character_limit?.toLocaleString()}
            </Badge>
          )}
        </div>
      </div>

      {/* Quota bar */}
      <Card>
        <CardContent className="pt-4 pb-4 space-y-1.5">
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>{used.toLocaleString()} / {limit.toLocaleString()} chars this period</span>
            <span>{(limit - used).toLocaleString()} remaining</span>
          </div>
          <div className="h-1.5 rounded-full bg-muted overflow-hidden">
            <div
              className={`h-full transition-all ${usedPct > 90 ? "bg-destructive" : "bg-primary"}`}
              style={{ width: `${usedPct}%` }}
            />
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-2 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Voice</CardTitle>
          </CardHeader>
          <CardContent>
            <Select value={voiceId} onValueChange={setVoiceId}>
              <SelectTrigger>
                <SelectValue placeholder="Default (multilingual)" />
              </SelectTrigger>
              <SelectContent>
                {voices.map((v) => (
                  <SelectItem key={v.voice_id} value={v.voice_id}>{v.name}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">Output format</CardTitle>
          </CardHeader>
          <CardContent>
            <Select value={outputFormat} onValueChange={setOutputFormat}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {OUTPUT_FORMATS.map((f) => (
                  <SelectItem key={f.value} value={f.value}>{f.label}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-sm">Text</CardTitle>
            <div className="flex items-center gap-2">
              <span className="text-xs text-muted-foreground">{text.length} chars</span>
              <Button
                variant="ghost"
                size="sm"
                className="h-7 text-xs gap-1"
                onClick={() => setText(SAMPLE_TEXTS[Math.floor(Math.random() * SAMPLE_TEXTS.length)])}
              >
                <RefreshCw className="h-3 w-3" />
                Sample
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="नेपाली पाठ यहाँ लेख्नुहोस्…"
            className="min-h-[140px] text-base"
          />
          <div className="flex gap-3">
            <Button onClick={synthesize} disabled={loading || !text.trim()} className="gap-2">
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
              {loading ? "Generating…" : "Generate speech"}
            </Button>
            {audioUrl && (
              <Button variant="outline" onClick={download} className="gap-2">
                <Download className="h-4 w-4" />
                Download
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {audioUrl && (
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-2 mb-3">
              <Volume2 className="h-4 w-4 text-muted-foreground" />
              <span className="text-sm font-medium">Output</span>
            </div>
            <audio ref={audioRef} src={audioUrl} controls className="w-full" />
          </CardContent>
        </Card>
      )}
    </div>
  );
}
