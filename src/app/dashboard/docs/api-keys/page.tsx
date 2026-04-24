import Link from "next/link";

const Code = ({ children }: { children: string }) => (
  <pre className="bg-muted rounded-lg p-4 text-sm overflow-x-auto"><code>{children}</code></pre>
);

export default function ApiKeysPage() {
  return (
    <article className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">API keys</h1>
        <p className="text-muted-foreground">How to create, use, and manage your Swor API keys.</p>
      </div>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">What is an API key?</h2>
        <p className="text-sm text-muted-foreground leading-relaxed">
          An API key is a long secret string that identifies your account when you call the Swor API.
          Instead of sending your email and password, you attach the key to every request.
          Swor uses it to verify who you are, apply your plan's limits, and track your usage.
        </p>
        <p className="text-sm text-muted-foreground">
          Keys look like this:
        </p>
        <Code>{`swor_live_aBcDeFgHiJkLmNoPqRsTuVwXyZ0123456789012`}</Code>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Creating a key</h2>
        <ol className="space-y-2 text-sm text-muted-foreground">
          <li>1. Go to <Link href="/dashboard/keys" className="underline text-foreground">Dashboard → API Keys</Link></li>
          <li>2. Click <strong className="text-foreground">Create key</strong></li>
          <li>3. Give it a descriptive name (e.g. <code className="bg-muted px-1 rounded">production</code>, <code className="bg-muted px-1 rounded">mobile-app</code>)</li>
          <li>4. Copy the full key — <strong className="text-foreground">it is shown only once</strong></li>
        </ol>
        <p className="text-sm text-muted-foreground">
          Your plan controls how many active keys you can have at once (Free: 1, Starter: 3, Pro: 10, Enterprise: 50).
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Using a key in requests</h2>
        <p className="text-sm text-muted-foreground">
          Pass the key in the <code className="bg-muted px-1 rounded">X-API-Key</code> HTTP header on every request.
        </p>
        <Code>{`X-API-Key: swor_live_YOUR_KEY_HERE`}</Code>

        <p className="text-sm text-muted-foreground mt-2">Full example:</p>
        <Code>{`curl -X POST https://api.swor.io/api/v1/tts/synthesize/external \\
  -H "X-API-Key: swor_live_YOUR_KEY_HERE" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "नमस्ते"}' \\
  --output out.mp3`}</Code>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Storing your key safely</h2>
        <p className="text-sm text-muted-foreground">Never hardcode keys in source code or commit them to git.</p>
        <div className="space-y-3">
          <div>
            <p className="text-xs font-semibold uppercase text-muted-foreground mb-1">Environment variable (recommended)</p>
            <Code>{`# .env
SWOR_API_KEY=swor_live_YOUR_KEY_HERE`}</Code>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-muted-foreground mb-1">Python</p>
            <Code>{`import os
api_key = os.environ["SWOR_API_KEY"]`}</Code>
          </div>
          <div>
            <p className="text-xs font-semibold uppercase text-muted-foreground mb-1">Node.js</p>
            <Code>{`const apiKey = process.env.SWOR_API_KEY;`}</Code>
          </div>
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Revoking a key</h2>
        <p className="text-sm text-muted-foreground">
          If a key is compromised, go to <Link href="/dashboard/keys" className="underline text-foreground">Dashboard → API Keys</Link> and click the trash icon.
          The key is invalidated immediately — all requests using it will receive <code className="bg-muted px-1 rounded">401 Unauthorized</code>.
          Create a new key and update your app.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Errors</h2>
        <div className="space-y-2 text-sm">
          {[
            ["401", "Missing or invalid key", "Check the X-API-Key header is present and correct"],
            ["403", "Key revoked or account disabled", "Create a new key or contact support"],
            ["429", "Monthly quota exceeded", "Upgrade your plan or wait for the next billing period"],
          ].map(([code, reason, fix]) => (
            <div key={code} className="flex gap-4 py-2 border-b last:border-0">
              <code className="font-mono font-bold w-10 shrink-0">{code}</code>
              <span className="text-muted-foreground flex-1">{reason}</span>
              <span className="text-muted-foreground text-xs">{fix}</span>
            </div>
          ))}
        </div>
      </section>

      <div className="pt-4 flex gap-4 text-sm">
        <Link href="/dashboard/docs/synthesize" className="underline text-muted-foreground hover:text-foreground">
          Next: Synthesize speech →
        </Link>
      </div>
    </article>
  );
}
