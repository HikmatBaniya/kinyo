import { DocsSubnav } from "@/components/docs-subnav";

export default function DashboardDocsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-full overflow-hidden">
      <DocsSubnav />
      <main className="flex-1 overflow-y-auto px-8 py-8 max-w-3xl">
        {children}
      </main>
    </div>
  );
}
