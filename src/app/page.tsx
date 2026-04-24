import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { ThemeToggle } from "@/components/theme-toggle";
import { SworLogoLink } from "@/components/logo";
import { Check, Mic, Zap, Shield, Globe } from "lucide-react";

const PLANS = [
  {
    name: "Free",
    price: 0,
    chars: "10,000",
    keys: 1,
    features: ["10,000 chars/month", "1 API key", "Community support"],
    cta: "Get started",
    href: "/register",
    highlight: false,
  },
  {
    name: "Starter",
    price: 19,
    chars: "100,000",
    keys: 3,
    features: ["100,000 chars/month", "3 API keys", "Email support", "Usage dashboard"],
    cta: "Start free trial",
    href: "/register?plan=starter",
    highlight: false,
  },
  {
    name: "Pro",
    price: 79,
    chars: "500,000",
    keys: 10,
    features: ["500,000 chars/month", "10 API keys", "Priority support", "Usage analytics", "Custom voice config"],
    cta: "Start free trial",
    href: "/register?plan=pro",
    highlight: true,
  },
  {
    name: "Enterprise",
    price: 299,
    chars: "10,000,000",
    keys: 50,
    features: ["10M chars/month", "50 API keys", "Dedicated support", "SLA guarantee", "Custom integration"],
    cta: "Contact us",
    href: "mailto:dev@nepawholesale.com",
    highlight: false,
  },
];

const FEATURES = [
  { icon: Mic, title: "Native Nepali TTS", desc: "Optimized for Nepali language using eleven_multilingual_v2 model" },
  { icon: Zap, title: "Low latency API", desc: "Simple REST API with X-API-Key auth — integrate in minutes" },
  { icon: Shield, title: "Plan-based limits", desc: "Character quotas enforced per billing cycle, auto-reset monthly" },
  { icon: Globe, title: "Built for orgs", desc: "Multiple API keys, usage tracking, team-ready from day one" },
];

export default function Home() {
  return (
    <div className="min-h-screen">
      {/* Nav */}
      <header className="border-b">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <SworLogoLink />
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <Link href="/login"><Button variant="ghost">Sign in</Button></Link>
            <Link href="/register"><Button>Get started</Button></Link>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 pt-24 pb-16 text-center space-y-6">
        <Badge variant="secondary" className="text-sm">Nepali Text-to-Speech API</Badge>
        <h1 className="text-5xl font-extrabold tracking-tight leading-tight">
          The Nepali TTS API<br />for your product
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Swor gives your organization a simple, reliable API to convert Nepali text to natural-sounding speech.
          Powered by ElevenLabs. Priced for teams.
        </p>
        <div className="flex gap-4 justify-center">
          <Link href="/register"><Button size="lg">Start for free</Button></Link>
          <Link href="/docs"><Button size="lg" variant="outline">View API docs</Button></Link>
        </div>
      </section>

      {/* Code snippet */}
      <section className="max-w-3xl mx-auto px-6 pb-20">
        <pre className="bg-card border rounded-xl p-6 text-sm overflow-x-auto text-left">
          <code>{`curl -X POST https://api.swor.io/api/v1/tts/synthesize/external \\
  -H "X-API-Key: swor_live_xxxxxxxxxxxx" \\
  -H "Content-Type: application/json" \\
  -d '{"text": "नमस्ते, यो नेपाली भाषण हो।"}' \\
  --output speech.mp3`}</code>
        </pre>
      </section>

      {/* Features */}
      <section className="bg-muted/40 py-20">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-3xl font-bold text-center mb-12">Why Swor</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {FEATURES.map(({ icon: Icon, title, desc }) => (
              <Card key={title}>
                <CardContent className="pt-6 space-y-3">
                  <Icon className="h-8 w-8 text-primary" />
                  <h3 className="font-semibold">{title}</h3>
                  <p className="text-sm text-muted-foreground">{desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section className="py-24 max-w-6xl mx-auto px-6" id="pricing">
        <div className="text-center mb-12 space-y-3">
          <h2 className="text-3xl font-bold">Simple pricing</h2>
          <p className="text-muted-foreground">Pay for what you use. Upgrade or downgrade anytime.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {PLANS.map((plan) => (
            <Card key={plan.name} className={plan.highlight ? "border-primary shadow-lg" : ""}>
              <CardHeader>
                {plan.highlight && <Badge className="w-fit mb-2">Most popular</Badge>}
                <CardTitle>{plan.name}</CardTitle>
                <CardDescription>
                  <span className="text-3xl font-bold text-foreground">${plan.price}</span>
                  {plan.price > 0 && <span className="text-sm">/month</span>}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <ul className="space-y-2">
                  {plan.features.map((f) => (
                    <li key={f} className="flex items-center gap-2 text-sm">
                      <Check className="h-4 w-4 text-primary flex-shrink-0" />
                      {f}
                    </li>
                  ))}
                </ul>
                <Link href={plan.href} className="block">
                  <Button className="w-full" variant={plan.highlight ? "default" : "outline"}>
                    {plan.cta}
                  </Button>
                </Link>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="max-w-6xl mx-auto px-6 flex items-center justify-between text-sm text-muted-foreground">
          <span>© 2025 Swor — Nepali TTS Platform</span>
          <div className="flex gap-6">
            <Link href="/docs" className="hover:text-foreground">Docs</Link>
            <Link href="mailto:dev@nepawholesale.com" className="hover:text-foreground">Support</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}
