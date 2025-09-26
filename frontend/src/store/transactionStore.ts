import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { apiGet, apiPost } from '../services/api';
import type { BaseAsyncSlice, RequestStatus, Id, WithTimestamps } from './types';

export type MilestoneStatus = 'pending' | 'in_progress' | 'completed' | 'blocked';

export interface Milestone extends WithTimestamps<{ id: Id; name: string; dueDate: string; status: MilestoneStatus; notes?: string; }>{}

export interface Transaction extends WithTimestamps<{ id: Id; propertyId: Id; buyerId?: Id; sellerId?: Id; status: 'pre_contract' | 'in_contract' | 'closed' | 'canceled'; milestones: Milestone[]; escrowDocs?: string[]; }>{}

export interface TransactionState {
  transactions: Transaction[];
  fetch: BaseAsyncSlice;
  mutate: BaseAsyncSlice;
  // actions
  fetchTransactions: () => Promise<void>;
  createTransaction: (payload: Omit<Transaction, 'id'>) => Promise<Transaction>;
  updateMilestone: (txId: Id, milestoneId: Id, updates: Partial<Milestone>) => Promise<Transaction>;
  uploadDocument: (txId: Id, fileUrl: string) => Promise<Transaction>;
}

const initialAsync: BaseAsyncSlice = { status: 'idle', error: null };

export const useTransactionStore = create<TransactionState>()(devtools((set, get) => ({
  transactions: [],
  fetch: initialAsync,
  mutate: initialAsync,

  fetchTransactions: async () => {
    set({ fetch: { status: 'loading', error: null } });
    try {
      const data = await apiGet<Transaction[]>('/transactions');
      set({ transactions: data, fetch: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
    } catch (e: any) {
      set({ fetch: { status: 'error', error: e.message } });
    }
  },

  createTransaction: async (payload) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      const created = await apiPost<Transaction>('/transactions', payload);
      set({ transactions: [created, ...get().transactions], mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
      return created;
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },

  updateMilestone: async (txId, milestoneId, updates) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      const updated = await apiPost<Transaction>(`/transactions/${txId}/milestones/${milestoneId}`, { ...updates, _method: 'PATCH' });
      set({ transactions: get().transactions.map(t => t.id === txId ? updated : t), mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
      return updated;
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },

  uploadDocument: async (txId, fileUrl) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      const updated = await apiPost<Transaction>(`/transactions/${txId}/documents`, { fileUrl });
      set({ transactions: get().transactions.map(t => t.id === txId ? updated : t), mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
      return updated;
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },
})));

// Selectors
export const selectTransactions = (s: TransactionState) => s.transactions;
export const selectTransactionById = (id: Id) => (s: TransactionState) => s.transactions.find(t => t.id === id) || null;
export const selectUpcomingDeadlines = (daysAhead: number) => (s: TransactionState) => {
  const now = new Date();
  const cutoff = new Date(now.getTime() + daysAhead * 24 * 60 * 60 * 1000);
  return s.transactions.flatMap(t => t.milestones.filter(m => new Date(m.dueDate) <= cutoff && m.status !== 'completed').map(m => ({ txId: t.id, milestone: m })));
};
export const selectTransactionFetchStatus = (s: TransactionState): RequestStatus => s.fetch.status;
export const selectTransactionMutateStatus = (s: TransactionState): RequestStatus => s.mutate.status;