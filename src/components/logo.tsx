import Link from "next/link";
import { cn } from "@/lib/utils";

interface LogoProps {
  className?: string;
  showText?: boolean;
  size?: "sm" | "md" | "lg";
}

const SIZES = {
  sm: { icon: 24, text: "text-base" },
  md: { icon: 32, text: "text-xl" },
  lg: { icon: 48, text: "text-3xl" },
};

export function SworLogo({ className, showText = true, size = "md" }: LogoProps) {
  const s = SIZES[size];
  return (
    <div className={cn("flex items-center gap-2.5", className)}>
      {/* Sound wave icon */}
      <svg
        width={s.icon}
        height={s.icon}
        viewBox="0 0 32 32"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="Swor logo"
      >
        {/* Outer arc */}
        <path
          d="M26 6.5C29.5 9.5 31.5 12.6 31.5 16C31.5 19.4 29.5 22.5 26 25.5"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          className="text-primary"
        />
        {/* Middle arc */}
        <path
          d="M22 10C24.5 12 25.8 13.9 25.8 16C25.8 18.1 24.5 20 22 22"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          className="text-primary"
        />
        {/* Inner arc */}
        <path
          d="M18 13C19.5 14.2 20.2 15.1 20.2 16C20.2 16.9 19.5 17.8 18 19"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          className="text-primary"
        />
        {/* Speaker body */}
        <path
          d="M4 11H7L13 6V26L7 21H4C3.45 21 3 20.55 3 20V12C3 11.45 3.45 11 4 11Z"
          fill="currentColor"
          className="text-primary"
        />
      </svg>
      {showText && (
        <div className="flex flex-col leading-none">
          <span className={cn("font-bold tracking-tight", s.text)}>स्वर</span>
          <span className="text-xs text-muted-foreground font-medium tracking-widest uppercase">Swor</span>
        </div>
      )}
    </div>
  );
}

export function SworLogoLink({ className, size }: { className?: string; size?: "sm" | "md" | "lg" }) {
  return (
    <Link href="/" className={cn("hover:opacity-80 transition-opacity", className)}>
      <SworLogo size={size} />
    </Link>
  );
}
