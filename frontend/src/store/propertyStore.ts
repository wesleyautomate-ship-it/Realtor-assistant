import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { apiGet, apiPost } from '../services/api';
import type { BaseAsyncSlice, RequestStatus, Id, WithTimestamps } from './types';

export interface Property extends WithTimestamps<{ id: Id; title: string; price: number; address: string; city?: string; state?: string; zip?: string; beds?: number; baths?: number; sqft?: number; imageUrl?: string; status?: 'draft' | 'active' | 'pending' | 'sold'; }>{}

export interface PropertyState {
  items: Property[];
  selectedId: Id | null;
  fetch: BaseAsyncSlice;
  mutate: BaseAsyncSlice;
  // actions
  fetchProperties: () => Promise<void>;
  addProperty: (payload: Omit<Property, 'id'>) => Promise<Property>;
  updateProperty: (id: Id, updates: Partial<Property>) => Promise<Property>;
  deleteProperty: (id: Id) => Promise<void>;
  setSelected: (id: Id | null) => void;
}

const initialAsync: BaseAsyncSlice = { status: 'idle', error: null };

export const usePropertyStore = create<PropertyState>()(devtools((set, get) => ({
  items: [],
  selectedId: null,
  fetch: initialAsync,
  mutate: initialAsync,

  setSelected: (id) => set({ selectedId: id }),

  fetchProperties: async () => {
    set({ fetch: { status: 'loading', error: null } });
    try {
      // Unified API base uses /api prefix per services/api.ts usage across screens
      const data = await apiGet<Property[]>('/api/properties');
      set({ items: data, fetch: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
    } catch (e: any) {
      set({ fetch: { status: 'error', error: e.message } });
    }
  },

  addProperty: async (payload) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      const created = await apiPost<Property>('/api/properties', payload);
      set({ items: [created, ...get().items], mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
      return created;
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },

  updateProperty: async (id, updates) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      const updated = await apiPost<Property>(`/api/properties/${id}`, { ...updates, _method: 'PATCH' });
      set({ items: get().items.map(i => i.id === id ? { ...i, ...updated } : i), mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
      return updated;
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },

  deleteProperty: async (id) => {
    set({ mutate: { status: 'loading', error: null } });
    try {
      await apiPost(`/api/properties/${id}`, { _method: 'DELETE' });
      set({ items: get().items.filter(i => i.id !== id), mutate: { status: 'success', error: null, lastUpdated: new Date().toISOString() } });
    } catch (e: any) {
      set({ mutate: { status: 'error', error: e.message } });
      throw e;
    }
  },
})));

// Selectors
export const selectProperties = (s: PropertyState) => s.items;
export const selectSelectedProperty = (s: PropertyState) => s.items.find(i => i.id === s.selectedId) || null;
export const selectPropertyFetchStatus = (s: PropertyState): RequestStatus => s.fetch.status;
export const selectPropertyMutateStatus = (s: PropertyState): RequestStatus => s.mutate.status;