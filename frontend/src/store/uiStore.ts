import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

export interface Snackbar {
  id: string;
  message: string;
  type?: 'info' | 'success' | 'warning' | 'error';
}

interface UIState {
  modalId: string | null;
  globalLoading: boolean;
  snackbars: Snackbar[];
  // actions
  openModal: (id: string) => void;
  closeModal: () => void;
  startLoading: () => void;
  stopLoading: () => void;
  pushSnackbar: (snackbar: Snackbar) => void;
  removeSnackbar: (id: string) => void;
}

export const useUIStore = create<UIState>()(devtools((set, get) => ({
  modalId: null,
  globalLoading: false,
  snackbars: [],

  openModal: (id) => set({ modalId: id }),
  closeModal: () => set({ modalId: null }),
  startLoading: () => set({ globalLoading: true }),
  stopLoading: () => set({ globalLoading: false }),
  pushSnackbar: (snackbar) => set({ snackbars: [...get().snackbars, snackbar] }),
  removeSnackbar: (id) => set({ snackbars: get().snackbars.filter(s => s.id !== id) }),
})));

// Selectors
export const selectModalId = (s: UIState) => s.modalId;
export const selectGlobalLoading = (s: UIState) => s.globalLoading;
export const selectSnackbars = (s: UIState) => s.snackbars;