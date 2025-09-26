import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import type { Id, WithTimestamps } from './types';

export interface UserProfile extends WithTimestamps<{ id: Id; name: string; email: string; role?: 'agent' | 'admin'; }>{}

export interface Preferences {
  darkMode: boolean;
  locale: string;
}

interface UserState {
  user: UserProfile | null;
  token: string | null;
  preferences: Preferences;
  // actions
  login: (user: UserProfile, token: string) => void;
  logout: () => void;
  updatePreferences: (updates: Partial<Preferences>) => void;
}

export const useUserStore = create<UserState>()(persist(devtools((set) => ({
  user: null,
  token: null,
  preferences: { darkMode: false, locale: 'en-US' },

  login: (user, token) => set({ user, token }),
  logout: () => set({ user: null, token: null }),
  updatePreferences: (updates) => set((s) => ({ preferences: { ...s.preferences, ...updates } })),
})), {
  name: 'ppai-user-store',
}));

// Selectors
export const selectCurrentUser = (s: UserState) => s.user;
export const selectAuthToken = (s: UserState) => s.token;
export const selectPreferences = (s: UserState) => s.preferences;