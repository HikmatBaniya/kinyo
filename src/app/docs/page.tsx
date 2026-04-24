import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";
import { ArrowRight } from "lucide-react";

export default function DocsIntro() {
  return (
    <article className="prose-neutral max-w-none space-y-8">
      <div className="space-y-3">
        <Badge variant="secondary">v0.1</Badge>
        <h1 className="text-4xl font-bold">Swor Documentation</h1>
        <p className="text-lg text-muted-foreground leading-relaxed">
          Swor is a Nepali text-to-speech API platform. You get an API key, send Nepali text, receive audio. That's it.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {[
          { href: "/docs/quickstart", title: "Quick start", desc: "Go from zero to playing Nepali audio in 5 minutes" },
          { href: "/docs/api-keys", title: "API keys", desc: "Create, manage, and revoke your API keys" },
          { href: "/docs/synthesize", title: "Synthesize speech", desc: "Convert Nepali text to audio with one API call" },
          { href: "/docs/api-reference", title: "API reference", desc: "Full endpoint documentation with request/response schemas" },
        ].map(({ href, title, desc }) => (
          <Link key={href} href={href}>
            <Card className="hover:border-primary transition-colors cursor-pointer h-full">
              <CardContent className="pt-5 pb-5 flex items-start justify-between gap-2">
                <div>
                  <p className="font-semibold">{title}</p>
                  <p className="text-sm text-muted-foreground mt-1">{desc}</p>
                </div>
                <ArrowRight className="h-4 w-4 text-muted-foreground mt-0.5 shrink-0" />
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">How Swor works</h2>
        <ol className="space-y-3 text-sm text-muted-foreground">
          <li className="flex gap-3">
            <span className="font-bold text-foreground w-5 shrink-0">1.</span>
            <span><strong className="text-foreground">Register</strong> at <Link href="/register" className="underline">swor.io/register</Link> and choose a plan. Free plan gives you 10,000 chars/month immediately.</span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-foreground w-5 shrink-0">2.</span>
            <span><strong className="text-foreground">Create an API key</strong> from your dashboard. The key starts with <code className="bg-muted px-1 rounded">swor_live_</code> and is shown only once.</span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-foreground w-5 shrink-0">3.</span>
            <span><strong className="text-foreground">Send a POST request</strong> to <code className="bg-muted px-1 rounded">/api/v1/tts/synthesize/external</code> with your text in the body and the key in the <code className="bg-muted px-1 rounded">X-API-Key</code> header.</span>
          </li>
          <li className="flex gap-3">
            <span className="font-bold text-foreground w-5 shrink-0">4.</span>
            <span><strong className="text-foreground">Receive audio</strong> as an <code className="bg-muted px-1 rounded">audio/mpeg</code> binary stream. Save it, stream it, or play it directly.</span>
          </li>
        </ol>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Base URL</h2>
        <pre className="bg-muted rounded-lg p-4 text-sm"><code>https://api.swor.io</code></pre>
        <p className="text-sm text-muted-foreground">All endpoints are versioned under <code className="bg-muted px-1 rounded">/api/v1</code>.</p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Supported language</h2>
        <p className="text-sm text-muted-foreground">
          Swor uses ElevenLabs' <code className="bg-muted px-1 rounded">eleven_multilingual_v2</code> model which natively supports Nepali (नेपाली).
          Send Devanagari script text directly — no transliteration needed.
        </p>
        <pre className="bg-muted rounded-lg p-4 text-sm"><code>{`"text": "नमस्ते, यो नेपाली भाषण हो।"  ✓
"text": "Namaste, this is Nepali speech."  ✗ (use Devanagari)`}</code></pre>
      </section>
    </article>
  );
}
