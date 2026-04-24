import Link from "next/link";

const Code = ({ children }: { children: string }) => (
  <pre className="bg-muted rounded-lg p-4 text-sm overflow-x-auto"><code>{children}</code></pre>
);

export default function ErrorsPage() {
  return (
    <article className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Errors & limits</h1>
        <p className="text-muted-foreground">How errors are returned and what the limits are.</p>
      </div>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Error format</h2>
        <p className="text-sm text-muted-foreground">All errors return JSON with a <code className="bg-muted px-1 rounded">detail</code> field.</p>
        <Code>{`{
  "detail": "Monthly limit reached. 0 chars remaining on free plan."
}`}</Code>
        <p className="text-sm text-muted-foreground">Always check the HTTP status code first, then read <code className="bg-muted px-1 rounded">detail</code> for the human-readable reason.</p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">HTTP status codes</h2>
        <div className="space-y-0">
          {[
            { code: "200", color: "text-emerald-600", title: "OK", desc: "Request succeeded. Body is audio binary (synthesize) or JSON (other endpoints)." },
            { code: "400", color: "text-orange-500", title: "Bad Request", desc: 'Request body failed validation. Check the "detail" field for which field is invalid.' },
            { code: "401", color: "text-red-500", title: "Unauthorized", desc: "Missing or invalid X-API-Key header. Check the key is correct and not revoked." },
            { code: "403", color: "text-red-500", title: "Forbidden", desc: "Account disabled, or trying to create more API keys than your plan allows." },
            { code: "404", color: "text-orange-500", title: "Not Found", desc: "The resource (e.g. API key ID) does not exist." },
            { code: "422", color: "text-orange-500", title: "Unprocessable Entity", desc: "JSON is valid but field types are wrong (e.g. stability not a float)." },
            { code: "429", color: "text-red-500", title: "Too Many Requests", desc: "Monthly character quota exceeded. Upgrade your plan or wait for period reset." },
            { code: "502", color: "text-red-500", title: "Bad Gateway", desc: "ElevenLabs returned an error. Usually temporary — retry after a few seconds." },
          ].map(({ code, color, title, desc }) => (
            <div key={code} className="flex gap-4 py-3 border-b last:border-0">
              <code className={`font-mono font-bold w-12 shrink-0 ${color}`}>{code}</code>
              <div>
                <p className="font-medium text-sm">{title}</p>
                <p className="text-sm text-muted-foreground">{desc}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Handling errors in code</h2>
        <Code>{`# Python
import requests

resp = requests.post(url, headers=headers, json=body)

if resp.status_code == 429:
    print("Quota exceeded:", resp.json()["detail"])
elif resp.status_code == 401:
    print("Invalid API key")
elif resp.status_code == 502:
    print("ElevenLabs error — retry in 5s")
elif resp.ok:
    audio = resp.content
else:
    print("Error:", resp.status_code, resp.json())`}</Code>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Character limits per request</h2>
        <p className="text-sm text-muted-foreground">Each individual synthesis request is capped at <strong>5,000 characters</strong> regardless of plan. For longer texts, split into chunks.</p>
        <Code>{`# Split long text into chunks of 4500 chars (safe margin)
def chunk_text(text: str, size: int = 4500) -> list[str]:
    return [text[i:i+size] for i in range(0, len(text), size)]`}</Code>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Monthly quota reset</h2>
        <p className="text-sm text-muted-foreground">
          Quotas reset 30 days from your subscription start date, not on the 1st of each month.
          The <code className="bg-muted px-1 rounded">period_reset_at</code> field in <code className="bg-muted px-1 rounded">GET /usage/summary</code> shows when your current period started.
        </p>
      </section>

      <div className="pt-4 text-sm">
        <Link href="/docs/plans" className="underline text-muted-foreground hover:text-foreground">Next: Plans →</Link>
      </div>
    </article>
  );
}
