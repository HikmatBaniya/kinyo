import Link from "next/link";
import { Check } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

const PLANS = [
  {
    name: "Free",
    price: 0,
    chars: 10_000,
    keys: 1,
    features: ["10,000 chars/month", "1 API key", "MP3 + PCM output", "Community support"],
  },
  {
    name: "Starter",
    price: 19,
    chars: 100_000,
    keys: 3,
    features: ["100,000 chars/month", "3 API keys", "All output formats", "Email support", "Usage dashboard"],
    highlight: true,
  },
  {
    name: "Pro",
    price: 79,
    chars: 500_000,
    keys: 10,
    features: ["500,000 chars/month", "10 API keys", "All output formats", "Priority support", "Usage analytics"],
  },
  {
    name: "Enterprise",
    price: 299,
    chars: 10_000_000,
    keys: 50,
    features: ["10M chars/month", "50 API keys", "All output formats", "Dedicated support", "SLA guarantee", "Custom integration help"],
  },
];

export default function PlansPage() {
  return (
    <article className="space-y-8">
      <div className="space-y-2">
        <h1 className="text-3xl font-bold">Plans</h1>
        <p className="text-muted-foreground">Every plan includes access to all Nepali TTS endpoints.</p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {PLANS.map((p) => (
          <Card key={p.name} className={p.highlight ? "border-primary" : ""}>
            <CardHeader>
              {p.highlight && <Badge className="w-fit mb-1 text-xs">Most popular</Badge>}
              <CardTitle className="text-lg">{p.name}</CardTitle>
              <CardDescription>
                <span className="text-2xl font-bold text-foreground">${p.price}</span>
                {p.price > 0 && <span className="text-sm">/month</span>}
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-3">
              <ul className="space-y-1.5">
                {p.features.map((f) => (
                  <li key={f} className="flex items-center gap-2 text-sm text-muted-foreground">
                    <Check className="h-3.5 w-3.5 text-primary shrink-0" />
                    {f}
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        ))}
      </div>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Upgrading</h2>
        <p className="text-sm text-muted-foreground">
          Upgrade from your <Link href="/dashboard/billing" className="underline text-foreground">Billing page</Link>.
          Upgrades take effect immediately via Stripe. Downgrade takes effect at the end of the current billing period.
        </p>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">What counts as a character?</h2>
        <p className="text-sm text-muted-foreground">
          Each Unicode character in your <code className="bg-muted px-1 rounded">text</code> field counts as one character.
          Nepali Devanagari characters, spaces, and punctuation all count equally.
          Response headers always show your current usage.
        </p>
        <pre className="bg-muted rounded-lg p-4 text-sm"><code>{`"नमस्ते" → 6 characters
"नमस्ते, यो नेपाली भाषण हो।" → 28 characters`}</code></pre>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-bold">Enterprise</h2>
        <p className="text-sm text-muted-foreground">
          For custom volume, SLA requirements, or on-premise integration, contact us at{" "}
          <a href="mailto:dev@nepawholesale.com" className="underline text-foreground">dev@nepawholesale.com</a>.
        </p>
      </section>

      <div className="pt-2">
        <Link href="/register">
          <Button>Get started free →</Button>
        </Link>
      </div>
    </article>
  );
}
