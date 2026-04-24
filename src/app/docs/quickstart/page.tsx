import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent } from "@/components/ui/card";

const Step = ({ n, title, children }: { n: number; title: string; children: React.ReactNode }) => (
  <div className="flex gap-4">
    <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center text-sm font-bold shrink-0 mt-0.5">
      {n}
    </div>
    <div className="flex-1 space-y-3 pb-8 border-b last:border-0">
      <h3 className="font-semibold text-lg">{title}</h3>
      {children}
    </div>
  </div>
);

const Code = ({ children }: { children: string }) => (
  <pre className="bg-muted rounded-lg p-4 text-sm overflow-x-auto"><code>{children}</code></pre>
);

export default function QuickstartPage() {
  return (
    <article className="space-y-8">
      <div className="space-y-2">
        <Badge variant="secondary">5 minutes</Badge>
        <h1 className="text-3xl font-bold">Quick start</h1>
        <p className="text-muted-foreground">From zero to Nepali audio in 5 minutes.</p>
      </div>

      <div className="space-y-0">
        <Step n={1} title="Create an account">
          <p className="text-sm text-muted-foreground">
            Go to <Link href="/register" className="underline font-medium text-foreground">swor.io/register</Link> and sign up.
            Your account is created with the <strong>Free plan</strong> — 10,000 characters per month, no credit card required.
          </p>
        </Step>

        <Step n={2} title="Create your first API key">
          <p className="text-sm text-muted-foreground">
            In your dashboard, go to <Link href="/dashboard/keys" className="underline font-medium text-foreground">API Keys</Link> and click <strong>Create key</strong>.
            Give it a name like <code className="bg-muted px-1 rounded">my-app</code>.
          </p>
          <Card className="border-yellow-200 bg-yellow-50 dark:bg-yellow-950 dark:border-yellow-800">
            <CardContent className="pt-4 pb-4">
              <p className="text-sm text-yellow-800 dark:text-yellow-200">
                <strong>Copy your key immediately.</strong> It looks like <code>swor_live_abc123...</code> and is shown only once.
                Store it in your environment variables, not in code.
              </p>
            </CardContent>
          </Card>
        </Step>

        <Step n={3} title="Make your first request">
          <p className="text-sm text-muted-foreground mb-3">
            Replace <code className="bg-muted px-1 rounded">YOUR_KEY</code> with your actual key and run:
          </p>
          <Code>{`curl -X POST https://api.swor.io/api/v1/tts/synthesize/external \\
  -H "X-API-Key: swor_live_YOUR_KEY" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "नमस्ते! स्वागत छ।"}' \\
  --output hello.mp3`}</Code>
          <p className="text-sm text-muted-foreground">
            This saves <code className="bg-muted px-1 rounded">hello.mp3</code> to your current directory.
          </p>
        </Step>

        <Step n={4} title="Check your usage">
          <p className="text-sm text-muted-foreground mb-3">
            Every response includes quota headers so you know how much you've used:
          </p>
          <Code>{`X-Chars-Used: 12
X-Chars-Remaining: 9988
X-Chars-Limit: 10000
X-Plan: free`}</Code>
          <p className="text-sm text-muted-foreground">
            You can also see full usage history in your <Link href="/dashboard/usage" className="underline font-medium text-foreground">Usage dashboard</Link>.
          </p>
        </Step>

        <Step n={5} title="Integrate into your app">
          <p className="text-sm text-muted-foreground mb-3">Python example:</p>
          <Code>{`import requests, os

def nepali_tts(text: str) -> bytes:
    resp = requests.post(
        "https://api.swor.io/api/v1/tts/synthesize/external",
        headers={
            "X-API-Key": os.environ["SWOR_API_KEY"],
            "Content-Type": "application/json",
        },
        json={"text": text},
    )
    resp.raise_for_status()
    return resp.content  # raw MP3 bytes

audio = nepali_tts("नमस्ते, यो मेरो एप हो।")
with open("output.mp3", "wb") as f:
    f.write(audio)`}</Code>

          <p className="text-sm text-muted-foreground mb-3 mt-4">JavaScript / Node.js:</p>
          <Code>{`const tts = async (text) => {
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
  if (!res.ok) throw new Error(await res.text());
  return res.arrayBuffer(); // raw MP3
};`}</Code>
        </Step>
      </div>

      <div className="pt-4 flex gap-4 text-sm">
        <Link href="/docs/api-keys" className="underline text-muted-foreground hover:text-foreground">
          Next: Managing API keys →
        </Link>
      </div>
    </article>
  );
}
