import Link from "next/link";

const Code = ({ lang, children }: { lang?: string; children: string }) => (
  <div className="space-y-1">
    {lang && <p className="text-xs font-semibold text-muted-foreground uppercase">{lang}</p>}
    <pre className="bg-muted rounded-lg p-4 text-sm overflow-x-auto"><code>{children}</code></pre>
  </div>
);

export default function BatchPage() {
  return (
    <article className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Batch requests</h1>
        <p className="text-muted-foreground">Synthesize up to 10 texts in a single HTTP call.</p>
      </div>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">When to use batch</h2>
        <ul className="text-sm text-muted-foreground space-y-2">
          <li>• Generating audio for multiple UI strings at once (menus, labels, prompts)</li>
          <li>• Processing a list of sentences without making 10 separate HTTP calls</li>
          <li>• Reducing latency overhead when order matters but parallelism is hard</li>
        </ul>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Endpoint</h2>
        <div className="flex items-center gap-3">
          <span className="bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200 text-xs font-bold px-2 py-1 rounded font-mono">POST</span>
          <code className="text-sm">/api/v1/tts/batch/external</code>
        </div>
        <p className="text-sm text-muted-foreground">
          All characters across all items count toward your monthly quota. The total char count is checked <strong>before</strong> any synthesis begins — if it exceeds your remaining quota the whole batch is rejected.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Request</h2>
        <Code>{`{
  "items": [
    { "text": "नमस्ते" },
    { "text": "धन्यवाद", "voice_id": "custom_voice_id" },
    { "text": "फेरि भेटौंला" }
  ],
  "model_id": "eleven_multilingual_v2",
  "output_format": "mp3_44100_128"
}`}</Code>
        <p className="text-sm text-muted-foreground">
          Each item can have its own <code className="bg-muted px-1 rounded">voice_id</code>. If omitted, the platform default is used.
          Max 10 items per request.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Response</h2>
        <p className="text-sm text-muted-foreground">
          Returns a JSON array. Each item includes base64-encoded audio if successful.
        </p>
        <Code>{`[
  {
    "index": 0,
    "text": "नमस्ते",
    "success": true,
    "audio_base64": "//NExAAA...",
    "characters_used": 6,
    "error": null
  },
  {
    "index": 1,
    "text": "धन्यवाद",
    "success": true,
    "audio_base64": "//NExAAA...",
    "characters_used": 8,
    "error": null
  }
]`}</Code>
        <p className="text-sm text-muted-foreground">
          Individual items can fail (e.g. ElevenLabs error) while others succeed — check <code className="bg-muted px-1 rounded">success</code> per item.
        </p>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">Code examples</h2>

        <Code lang="Python">{`import requests, os, base64

def batch_synthesize(texts: list[str]) -> list[bytes]:
    items = [{"text": t} for t in texts]
    resp = requests.post(
        "https://api.swor.io/api/v1/tts/batch/external",
        headers={
            "X-API-Key": os.environ["SWOR_API_KEY"],
            "Content-Type": "application/json",
        },
        json={"items": items, "output_format": "mp3_44100_128"},
    )
    resp.raise_for_status()

    results = []
    for item in resp.json():
        if item["success"]:
            results.append(base64.b64decode(item["audio_base64"]))
        else:
            print(f"Item {item['index']} failed: {item['error']}")
            results.append(None)
    return results

audios = batch_synthesize(["नमस्ते", "धन्यवाद", "फेरि भेटौंला"])
for i, audio in enumerate(audios):
    if audio:
        with open(f"out_{i}.mp3", "wb") as f:
            f.write(audio)`}</Code>

        <Code lang="Node.js">{`import fs from "fs";

const batchSynthesize = async (texts) => {
  const res = await fetch(
    "https://api.swor.io/api/v1/tts/batch/external",
    {
      method: "POST",
      headers: {
        "X-API-Key": process.env.SWOR_API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        items: texts.map((text) => ({ text })),
        output_format: "mp3_44100_128",
      }),
    }
  );

  if (!res.ok) throw new Error(await res.text());
  const results = await res.json();

  results.forEach((item, i) => {
    if (item.success) {
      const buf = Buffer.from(item.audio_base64, "base64");
      fs.writeFileSync(\`out_\${i}.mp3\`, buf);
    } else {
      console.error(\`Item \${i} failed:\`, item.error);
    }
  });
};

await batchSynthesize(["नमस्ते", "धन्यवाद", "फेरि भेटौंला"]);`}</Code>
      </section>

      <div className="pt-4 flex gap-4 text-sm">
        <Link href="/dashboard/docs/formats" className="underline text-muted-foreground hover:text-foreground">Next: Audio formats →</Link>
      </div>
    </article>
  );
}
