import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { apiGet, apiPost } from '../services/api';
import type { BaseAsyncSlice, RequestStatus, Id, WithTimestamps } from './types';

export type LeadStatus = 'new' | 'contacted' | 'qualified' | 'nurturing' | 'converted' | 'archived';

export interface Client extends WithTimestamps<{ id: Id; name: string; email?: string; phone?: string; leadScore?: number; status: LeadStatus; lastContactedAt?: string; notes?: string; }>{}

export interface CommunicationLog extends WithTimestamps<{ id: Id; clientId: Id; type: 'call' | 'email' | 'sms' | 'meeting'; content?: string; at: string; }>{}

export interface ClientState {
  clients: Client[];
  logs: CommunicationLog[];
  fetch: BaseAsyncSlice;
  mutate: BaseAsyncSlice;
  // actions
  fetchClients: () => Promise<void>;
  addClient: (payload: Omit<Client, 'id'>) => Promise<Client>;
  updateClient: (id: Id, updates: Partial<Client>) => Promise<Client>;
  logCommunication: (payload: Omit<CommunicationLog, 'id'>) => Promise<CommunicationLog>;
  setLeadStatus: (id: Id, status: LeadStatus) => Promise<Client>;
}

const initialAsync: BaseAsyncSlice = { status: 'idle', error: null };

export const useClientStore = create<ClientState>()(devtools((set, get) => ({
  clients: [],
  logs: [],
  fetch: initialAsync,
  mutate: initialAsync,

  fetchClients: async () => {
    set({ fetch: { status: 'loading', error: null } });
    try {
      const data = await apiGet<Client[]>('/api/v1/clients');
      set({ clients: data, fetch: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
    } catch (e: any) {
      set({ fetch: { status: 'error', error: e.message } });
    }
  },

  addClient: async (payload) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      const created = await apiPost<Client>('/api/v1/clients', payload);
      set({ clients: [created, ...get().clients], mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
      return created;
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },

  updateClient: async (id, updates) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      const updated = await apiPost<Client>(`/api/v1/clients/${id}`, { ...updates, _method: 'PATCH' });
      set({ clients: get().clients.map(c => c.id === id ? { ...c, ...updated } : c), mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
      return updated;
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },

  logCommunication: async (payload) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      const created = await apiPost<CommunicationLog>('/api/v1/clients/communications', payload);
      set({ logs: [created, ...get().logs], mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
      return created;
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },

  setLeadStatus: async (id, status) => {
    return get().updateClient(id, { status });
  },
})));

// Selectors
export const selectClients = (s: ClientState) => s.clients;
export const selectClientById = (id: Id) => (s: ClientState) => s.clients.find(c => c.id === id) || null;
export const selectClientFetchStatus = (s: ClientState): RequestStatus => s.fetch.status;
export const selectClientMutateStatus = (s: ClientState): RequestStatus => s.mutate.status;