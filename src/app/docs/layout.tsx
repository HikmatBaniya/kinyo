import Link from "next/link";
import { ThemeToggle } from "@/components/theme-toggle";
import { SworLogoLink } from "@/components/logo";
import { BackButton } from "@/components/back-button";
import { GetApiKeyButton } from "@/components/get-api-key-button";

const NAV = [
  {
    group: "Getting Started",
    links: [
      { href: "/docs", label: "Introduction" },
      { href: "/docs/quickstart", label: "Quick start" },
      { href: "/docs/api-keys", label: "API keys" },
    ],
  },
  {
    group: "Guides",
    links: [
      { href: "/docs/synthesize", label: "Synthesize speech" },
      { href: "/docs/batch", label: "Batch requests" },
      { href: "/docs/formats", label: "Audio formats" },
      { href: "/docs/voices", label: "Voices" },
    ],
  },
  {
    group: "Reference",
    links: [
      { href: "/docs/api-reference", label: "API reference" },
      { href: "/docs/errors", label: "Errors & limits" },
      { href: "/docs/plans", label: "Plans" },
    ],
  },
];

export default function DocsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Top nav */}
      <header className="border-b sticky top-0 bg-background z-20">
        <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <SworLogoLink size="sm" />
            <nav className="hidden md:flex gap-4 text-sm text-muted-foreground">
              <Link href="/docs" className="hover:text-foreground">Docs</Link>
              <Link href="/dashboard" className="hover:text-foreground">Dashboard</Link>
            </nav>
          </div>
          <div className="flex items-center gap-3">
            <BackButton />
            <ThemeToggle />
            <GetApiKeyButton />
          </div>
        </div>
      </header>

      <div className="flex flex-1 max-w-7xl mx-auto w-full">
        {/* Sidebar */}
        <aside className="w-56 shrink-0 border-r px-4 py-8 sticky top-14 h-[calc(100vh-3.5rem)] overflow-y-auto hidden md:block">
          {NAV.map((section) => (
            <div key={section.group} className="mb-6">
              <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2">
                {section.group}
              </p>
              <ul className="space-y-1">
                {section.links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      className="block text-sm py-1 px-2 rounded hover:bg-muted text-muted-foreground hover:text-foreground transition-colors"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </aside>

        {/* Content */}
        <main className="flex-1 px-8 py-10 max-w-3xl">
          {children}
        </main>
      </div>
    </div>
  );
}
