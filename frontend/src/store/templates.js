import { create } from 'zustand';
import { api } from '../utils/apiClient';

const useTemplateStore = create((set, get) => ({
  // State
  templates: [],
  brandAssets: [],
  loading: false,
  error: null,
  
  // Actions
  fetchTemplates: async (team = null) => {
    set({ loading: true, error: null });
    try {
      const params = team ? `?team=${team}` : '';
      const response = await api.get(`/requests/templates${params}`);
      set({ templates: response.data, loading: false });
      return response.data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },
  
  fetchBrandAssets: async () => {
    set({ loading: true, error: null });
    try {
      const response = await api.get('/requests/brand-kit');
      set({ brandAssets: response.data, loading: false });
      return response.data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },
  
  getTemplatesByTeam: (team) => {
    const { templates } = get();
    return templates.filter(template => template.team === team);
  },
  
  getTemplateById: (id) => {
    const { templates } = get();
    return templates.find(template => template.id === id);
  },
  
  getBrandAssetsByType: (type) => {
    const { brandAssets } = get();
    return brandAssets.filter(asset => asset.type === type);
  },
  
  clearError: () => set({ error: null })
}));

export default useTemplateStore;
