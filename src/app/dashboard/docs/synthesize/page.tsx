import Link from "next/link";

const Code = ({ lang, children }: { lang?: string; children: string }) => (
  <div className="space-y-1">
    {lang && <p className="text-xs font-semibold text-muted-foreground uppercase">{lang}</p>}
    <pre className="bg-muted rounded-lg p-4 text-sm overflow-x-auto"><code>{children}</code></pre>
  </div>
);

const Field = ({ name, type, required, def, desc }: { name: string; type: string; required?: boolean; def?: string; desc: string }) => (
  <div className="py-3 border-b last:border-0">
    <div className="flex items-center gap-2 mb-1">
      <code className="text-sm font-mono font-bold">{name}</code>
      <span className="text-xs text-muted-foreground">{type}</span>
      {required ? <span className="text-xs text-red-500 font-medium">required</span> : <span className="text-xs text-muted-foreground">optional</span>}
      {def && <span className="text-xs text-muted-foreground">default: <code className="bg-muted px-1 rounded">{def}</code></span>}
    </div>
    <p className="text-sm text-muted-foreground">{desc}</p>
  </div>
);

export default function SynthesizePage() {
  return (
    <article className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Synthesize speech</h1>
        <p className="text-muted-foreground">Convert Nepali text to audio with a single API call.</p>
      </div>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Endpoint</h2>
        <div className="flex items-center gap-3">
          <span className="bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-200 text-xs font-bold px-2 py-1 rounded font-mono">POST</span>
          <code className="text-sm">/api/v1/tts/synthesize/external</code>
        </div>
        <p className="text-sm text-muted-foreground">Requires <code className="bg-muted px-1 rounded">X-API-Key</code> header. Returns binary audio.</p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Request fields</h2>
        <div>
          <Field name="text" type="string" required desc="The Nepali text to synthesize. Send Devanagari script. Max 5,000 characters per request." />
          <Field name="voice_id" type="string" def="default voice" desc="ElevenLabs voice ID. Leave null to use the platform default. See /docs/voices to list available IDs." />
          <Field name="model_id" type="string" def="eleven_multilingual_v2" desc="ElevenLabs model. eleven_multilingual_v2 is recommended for Nepali — do not change unless you have a reason." />
          <Field name="output_format" type="string" def="mp3_44100_128" desc="Audio format. Options: mp3_44100_128, mp3_44100_192, pcm_44100, ulaw_8000. See /docs/formats." />
          <Field name="stability" type="float 0–1" def="0.5" desc="Voice stability. Higher = more consistent but less expressive. Lower = more varied." />
          <Field name="similarity_boost" type="float 0–1" def="0.75" desc="How closely to match the voice. Higher = more similar to original voice." />
          <Field name="style" type="float 0–1" def="0.0" desc="Style exaggeration. Keep at 0 for neutral Nepali narration." />
          <Field name="use_speaker_boost" type="boolean" def="true" desc="Enhances voice clarity. Recommended to leave true." />
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Response</h2>
        <p className="text-sm text-muted-foreground">
          On success: <code className="bg-muted px-1 rounded">200 OK</code> with <code className="bg-muted px-1 rounded">Content-Type: audio/mpeg</code> (or the format you chose) and binary audio in the body.
        </p>
        <Code>{`// Response headers
Content-Type: audio/mpeg
X-Chars-Used: 28
X-Chars-Remaining: 99972
X-Chars-Limit: 100000
X-Plan: starter`}</Code>
      </section>

      <section className="space-y-4">
        <h2 className="text-xl font-bold">Code examples</h2>

        <Code lang="cURL">{`curl -X POST https://api.swor.io/api/v1/tts/synthesize/external \\
  -H "X-API-Key: swor_live_YOUR_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{
    "text": "नमस्ते, यो नेपाली भाषण हो।",
    "output_format": "mp3_44100_128"
  }' \\
  --output speech.mp3`}</Code>

        <Code lang="Python">{`import requests, os

def synthesize(text: str, output_path: str = "out.mp3"):
    resp = requests.post(
        "https://api.swor.io/api/v1/tts/synthesize/external",
        headers={
            "X-API-Key": os.environ["SWOR_API_KEY"],
            "Content-Type": "application/json",
        },
        json={
            "text": text,
            "output_format": "mp3_44100_128",
        },
    )
    if resp.status_code == 429:
        raise Exception("Quota exceeded: " + resp.json()["detail"])
    resp.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(resp.content)

    print(f"Chars remaining: {resp.headers['X-Chars-Remaining']}")

synthesize("नमस्ते, यो नेपाली भाषण हो।")`}</Code>

        <Code lang="JavaScript (browser)">{`async function synthesize(text) {
  const res = await fetch(
    "https://api.swor.io/api/v1/tts/synthesize/external",
    {
      method: "POST",
      headers: {
        "X-API-Key": "swor_live_YOUR_KEY",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text, output_format: "mp3_44100_128" }),
    }
  );

  if (res.status === 429) {
    const err = await res.json();
    throw new Error(err.detail); // quota exceeded
  }

  if (!res.ok) throw new Error("Request failed: " + res.status);

  const blob = await res.blob();
  const audio = new Audio(URL.createObjectURL(blob));
  audio.play();

  console.log("Remaining chars:", res.headers.get("X-Chars-Remaining"));
}`}</Code>

        <Code lang="Node.js">{`import fs from "fs";

const synthesize = async (text, outFile = "out.mp3") => {
  const res = await fetch(
    "https://api.swor.io/api/v1/tts/synthesize/external",
    {
      method: "POST",
      headers: {
        "X-API-Key": process.env.SWOR_API_KEY,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    }
  );

  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail ?? "Request failed");
  }

  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync(outFile, buf);
  console.log("Saved:", outFile);
  console.log("Remaining:", res.headers.get("X-Chars-Remaining"));
};

await synthesize("नमस्ते, यो नेपाली भाषण हो।");`}</Code>

        <Code lang="PHP">{`<?php
function synthesize(string $text, string $outFile = "out.mp3"): void {
    $ch = curl_init("https://api.swor.io/api/v1/tts/synthesize/external");
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_HTTPHEADER     => [
            "X-API-Key: " . getenv("SWOR_API_KEY"),
            "Content-Type: application/json",
        ],
        CURLOPT_POSTFIELDS     => json_encode(["text" => $text]),
    ]);
    $audio = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($status !== 200) {
        throw new Exception("API error: " . $status);
    }
    file_put_contents($outFile, $audio);
}

synthesize("नमस्ते, यो नेपाली भाषण हो।");`}</Code>
      </section>

      <div className="pt-4 flex gap-4 text-sm">
        <Link href="/dashboard/docs/batch" className="underline text-muted-foreground hover:text-foreground">Next: Batch requests →</Link>
      </div>
    </article>
  );
}
