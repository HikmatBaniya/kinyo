"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const NAV = [
  {
    group: "Getting Started",
    links: [
      { href: "/dashboard/docs", label: "Introduction" },
      { href: "/dashboard/docs/quickstart", label: "Quick start" },
      { href: "/dashboard/docs/api-keys", label: "API keys" },
    ],
  },
  {
    group: "Guides",
    links: [
      { href: "/dashboard/docs/synthesize", label: "Synthesize speech" },
      { href: "/dashboard/docs/batch", label: "Batch requests" },
      { href: "/dashboard/docs/formats", label: "Audio formats" },
      { href: "/dashboard/docs/voices", label: "Voices" },
    ],
  },
  {
    group: "Reference",
    links: [
      { href: "/dashboard/docs/api-reference", label: "API reference" },
      { href: "/dashboard/docs/errors", label: "Errors & limits" },
      { href: "/dashboard/docs/plans", label: "Plans" },
    ],
  },
];

export function DocsSubnav() {
  const pathname = usePathname();
  return (
    <aside className="w-52 shrink-0 border-r overflow-y-auto h-full px-3 py-6">
      {NAV.map((section) => (
        <div key={section.group} className="mb-6">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-2 px-2">
            {section.group}
          </p>
          <ul className="space-y-0.5">
            {section.links.map((link) => (
              <li key={link.href}>
                <Link
                  href={link.href}
                  className={cn(
                    "block text-sm py-1.5 px-2 rounded transition-colors",
                    pathname === link.href
                      ? "bg-secondary text-foreground font-medium"
                      : "text-muted-foreground hover:text-foreground hover:bg-muted"
                  )}
                >
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </aside>
  );
}
