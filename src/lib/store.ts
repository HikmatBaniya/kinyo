"use client";

import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  organization: string | null;
  plan: "free" | "starter" | "pro" | "enterprise";
  role: "user" | "admin";
  is_active: boolean;
  is_verified: boolean;
  chars_used_this_period: number;
  billing_period_start: string | null;
  created_at: string;
}

interface AuthState {
  token: string | null;
  user: User | null;
  _hydrated: boolean;
  setAuth: (token: string, user: User) => void;
  updateUser: (user: User) => void;
  clearAuth: () => void;
  setHydrated: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      _hydrated: false,
      setAuth: (token, user) => set({ token, user }),
      updateUser: (user) => set({ user }),
      clearAuth: () => set({ token: null, user: null }),
      setHydrated: () => set({ _hydrated: true }),
    }),
    {
      name: "swor-auth",
      onRehydrateStorage: () => (state) => {
        state?.setHydrated();
      },
    }
  )
);

export const PLAN_LIMITS: Record<string, number> = {
  free: 10_000,
  starter: 100_000,
  pro: 500_000,
  enterprise: 10_000_000,
};

export const PLAN_MAX_KEYS: Record<string, number> = {
  free: 1,
  starter: 3,
  pro: 10,
  enterprise: 50,
};

export const PLAN_PRICE: Record<string, number> = {
  free: 0,
  starter: 19,
  pro: 79,
  enterprise: 299,
};
