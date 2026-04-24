import Link from "next/link";

export default function FormatsPage() {
  return (
    <article className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Audio formats</h1>
        <p className="text-muted-foreground">Choose the right audio format for your use case.</p>
      </div>

      <section className="space-y-4">
        {[
          {
            value: "mp3_44100_128",
            label: "MP3 128kbps",
            mime: "audio/mpeg",
            default: true,
            use: "General purpose. Good quality, small file size. Best for web apps, mobile, and most use cases.",
          },
          {
            value: "mp3_44100_192",
            label: "MP3 192kbps (high quality)",
            mime: "audio/mpeg",
            default: false,
            use: "Higher fidelity MP3. Use when audio quality is critical and bandwidth is not a concern.",
          },
          {
            value: "pcm_44100",
            label: "PCM 44.1kHz",
            mime: "audio/wav",
            default: false,
            use: "Uncompressed audio. Use for post-processing, audio editing, or when you need lossless quality.",
          },
          {
            value: "ulaw_8000",
            label: "μ-law 8kHz",
            mime: "audio/basic",
            default: false,
            use: "Telephony format. Use for phone systems (IVR, SIP), VoIP, or low-bandwidth channels.",
          },
        ].map((f) => (
          <div key={f.value} className="border rounded-lg p-4 space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <code className="font-mono text-sm font-bold">{f.value}</code>
              {f.default && <span className="text-xs bg-primary text-primary-foreground px-2 py-0.5 rounded">default</span>}
              <span className="text-xs text-muted-foreground">{f.mime}</span>
            </div>
            <p className="text-sm text-muted-foreground">{f.use}</p>
          </div>
        ))}
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Setting the format</h2>
        <pre className="bg-muted rounded-lg p-4 text-sm overflow-x-auto">
          <code>{`{
  "text": "नमस्ते",
  "output_format": "mp3_44100_192"
}`}</code>
        </pre>
      </section>

      <div className="pt-4 text-sm">
        <Link href="/dashboard/docs/voices" className="underline text-muted-foreground hover:text-foreground">Next: Voices →</Link>
      </div>
    </article>
  );
}
