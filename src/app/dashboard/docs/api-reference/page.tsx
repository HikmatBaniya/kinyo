import Link from "next/link";
import { Badge } from "@/components/ui/badge";

const M = ({ method }: { method: string }) => {
  const colors: Record<string, string> = {
    GET: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
    POST: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200",
    DELETE: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
    PATCH: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
  };
  return <span className={`text-xs font-bold px-2 py-1 rounded font-mono ${colors[method]}`}>{method}</span>;
};

const Endpoint = ({ method, path, auth, desc, body, response }: {
  method: string; path: string; auth: string; desc: string; body?: string; response?: string;
}) => (
  <div className="border rounded-lg overflow-hidden">
    <div className="px-4 py-3 bg-muted/50 flex items-center gap-3 flex-wrap">
      <M method={method} />
      <code className="text-sm font-mono">{path}</code>
      <Badge variant="outline" className="text-xs ml-auto">{auth}</Badge>
    </div>
    <div className="px-4 py-3 space-y-3">
      <p className="text-sm text-muted-foreground">{desc}</p>
      {body && (
        <div>
          <p className="text-xs font-semibold uppercase text-muted-foreground mb-1">Body</p>
          <pre className="bg-muted rounded p-3 text-xs overflow-x-auto"><code>{body}</code></pre>
        </div>
      )}
      {response && (
        <div>
          <p className="text-xs font-semibold uppercase text-muted-foreground mb-1">Response</p>
          <pre className="bg-muted rounded p-3 text-xs overflow-x-auto"><code>{response}</code></pre>
        </div>
      )}
    </div>
  </div>
);

export default function ApiReferencePage() {
  return (
    <article className="space-y-10">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">API reference</h1>
        <p className="text-muted-foreground">Complete endpoint documentation.</p>
        <div className="flex gap-2 flex-wrap">
          <Badge>Base URL: https://api.swor.io</Badge>
          <Badge variant="secondary">All responses: application/json (errors) or binary (audio)</Badge>
        </div>
      </div>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">Text-to-Speech</h2>
        <Endpoint
          method="POST"
          path="/api/v1/tts/synthesize/external"
          auth="X-API-Key"
          desc="Synthesize a single text. Returns binary audio."
          body={`{
  "text": "नमस्ते",              // required, max 5000 chars
  "voice_id": null,             // optional, defaults to platform voice
  "model_id": "eleven_multilingual_v2",
  "output_format": "mp3_44100_128",
  "stability": 0.5,
  "similarity_boost": 0.75,
  "style": 0.0,
  "use_speaker_boost": true
}`}
          response={`// Binary audio stream
// Headers:
X-Chars-Used: 6
X-Chars-Remaining: 99994
X-Chars-Limit: 100000
X-Plan: starter`}
        />
        <Endpoint
          method="POST"
          path="/api/v1/tts/batch/external"
          auth="X-API-Key"
          desc="Synthesize up to 10 texts. Returns base64-encoded audio per item."
          body={`{
  "items": [
    { "text": "नमस्ते", "voice_id": null },
    { "text": "धन्यवाद" }
  ],
  "model_id": "eleven_multilingual_v2",
  "output_format": "mp3_44100_128"
}`}
          response={`[
  {
    "index": 0,
    "text": "नमस्ते",
    "success": true,
    "audio_base64": "//NExAAA...",
    "characters_used": 6,
    "error": null
  }
]`}
        />
        <Endpoint
          method="GET"
          path="/api/v1/tts/voices/external"
          auth="X-API-Key"
          desc="List all available ElevenLabs voices."
          response={`[
  {
    "voice_id": "pNInz6obpgDQGcFmaJgB",
    "name": "Adam",
    "preview_url": "https://...",
    "labels": { "accent": "american", "gender": "male" }
  }
]`}
        />
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">Authentication</h2>
        <Endpoint method="POST" path="/api/v1/auth/register" auth="Public" desc="Create a new account."
          body={`{
  "email": "you@example.com",
  "password": "min8chars",
  "full_name": "Ram Sharma",   // optional
  "organization": "Acme Corp"  // optional
}`}
          response={`{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": { "id": "...", "email": "...", "plan": "free", ... }
}`}
        />
        <Endpoint method="POST" path="/api/v1/auth/login" auth="Public" desc="Login with email and password."
          body={`{ "email": "you@example.com", "password": "yourpass" }`}
          response={`{ "access_token": "eyJ...", "token_type": "bearer", "user": { ... } }`}
        />
        <Endpoint method="GET" path="/api/v1/auth/me" auth="Bearer JWT" desc="Get current user profile." />
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">API Keys</h2>
        <Endpoint method="POST" path="/api/v1/keys" auth="Bearer JWT" desc="Create a new API key. Returns full key once — store it immediately."
          body={`{ "name": "production" }`}
          response={`{
  "id": "...",
  "key": "swor_live_...",   // shown once
  "key_prefix": "swor_live",
  "name": "production",
  "is_active": true,
  "requests_count": 0,
  "created_at": "2025-01-01T00:00:00Z"
}`}
        />
        <Endpoint method="GET" path="/api/v1/keys" auth="Bearer JWT" desc="List all API keys (key values are not shown)." />
        <Endpoint method="DELETE" path="/api/v1/keys/{key_id}" auth="Bearer JWT" desc="Revoke an API key. Immediate effect." />
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">Usage</h2>
        <Endpoint method="GET" path="/api/v1/usage/summary" auth="Bearer JWT" desc="Get usage summary for the current billing period."
          response={`{
  "total_requests": 42,
  "total_characters": 15000,
  "chars_used_this_period": 3200,
  "chars_limit_this_period": 100000,
  "chars_remaining": 96800,
  "plan": "starter",
  "period_reset_at": "2025-01-01T00:00:00Z"
}`}
        />
        <Endpoint method="GET" path="/api/v1/usage/breakdown" auth="Bearer JWT" desc="Character usage grouped by source (dashboard, api, api_batch)." />
        <Endpoint method="GET" path="/api/v1/usage/logs?limit=50&source=api" auth="Bearer JWT" desc="Paginated request history. Filter by source." />
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">Billing</h2>
        <Endpoint method="POST" path="/api/v1/billing/checkout" auth="Bearer JWT" desc="Create a Stripe checkout session to upgrade plan."
          body={`{ "plan": "starter" }  // starter | pro | enterprise`}
          response={`{ "url": "https://checkout.stripe.com/..." }`}
        />
        <Endpoint method="POST" path="/api/v1/billing/portal" auth="Bearer JWT" desc="Open Stripe customer portal to manage subscription."
          response={`{ "url": "https://billing.stripe.com/..." }`}
        />
      </section>

      <div className="pt-4 text-sm">
        <Link href="/dashboard/docs/errors" className="underline text-muted-foreground hover:text-foreground">Next: Errors & limits →</Link>
      </div>
    </article>
  );
}
