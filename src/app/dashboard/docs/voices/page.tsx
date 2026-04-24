import Link from "next/link";

const Code = ({ children }: { children: string }) => (
  <pre className="bg-muted rounded-lg p-4 text-sm overflow-x-auto"><code>{children}</code></pre>
);

export default function VoicesPage() {
  return (
    <article className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Voices</h1>
        <p className="text-muted-foreground">List available voices and select one for your requests.</p>
      </div>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">List voices</h2>
        <div className="flex items-center gap-3">
          <span className="bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 text-xs font-bold px-2 py-1 rounded font-mono">GET</span>
          <code className="text-sm">/api/v1/tts/voices/external</code>
        </div>
        <Code>{`curl https://api.swor.io/api/v1/tts/voices/external \\
  -H "X-API-Key: swor_live_YOUR_KEY"`}</Code>
        <Code>{`[
  {
    "voice_id": "pNInz6obpgDQGcFmaJgB",
    "name": "Adam",
    "preview_url": "https://storage.googleapis.com/...",
    "labels": {
      "accent": "american",
      "description": "deep",
      "age": "middle-aged",
      "gender": "male",
      "use_case": "narration"
    }
  },
  ...
]`}</Code>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Using a specific voice</h2>
        <p className="text-sm text-muted-foreground">
          Pass the <code className="bg-muted px-1 rounded">voice_id</code> in your synthesis request.
          If omitted, the platform default voice is used.
        </p>
        <Code>{`{
  "text": "नमस्ते",
  "voice_id": "pNInz6obpgDQGcFmaJgB"
}`}</Code>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Choosing a voice for Nepali</h2>
        <p className="text-sm text-muted-foreground leading-relaxed">
          Not all voices perform equally in Nepali. The <code className="bg-muted px-1 rounded">eleven_multilingual_v2</code> model supports Nepali across all voices,
          but results vary. Recommendations:
        </p>
        <ul className="text-sm text-muted-foreground space-y-2">
          <li>• Test a few voices using the <Link href="/dashboard" className="underline text-foreground">Playground</Link> before committing to one</li>
          <li>• Voices with lower <strong className="text-foreground">stability</strong> may sound more natural in Nepali</li>
          <li>• Narration-style voices generally work best for long-form Nepali text</li>
          <li>• Use the <code className="bg-muted px-1 rounded">preview_url</code> in the voices list to hear each voice in English first</li>
        </ul>
      </section>

      <div className="pt-4 text-sm">
        <Link href="/dashboard/docs/api-reference" className="underline text-muted-foreground hover:text-foreground">Next: API reference →</Link>
      </div>
    </article>
  );
}
