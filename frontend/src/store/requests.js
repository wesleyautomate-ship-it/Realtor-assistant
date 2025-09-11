import { create } from 'zustand';
import { api } from '../utils/apiClient';

const useRequestStore = create((set, get) => ({
  // State
  requests: [],
  currentRequest: null,
  loading: false,
  error: null,
  
  // Actions
  fetchRequests: async (filters = {}) => {
    set({ loading: true, error: null });
    try {
      const params = new URLSearchParams();
      if (filters.status) params.append('status', filters.status);
      if (filters.team) params.append('team', filters.team);
      if (filters.limit) params.append('limit', filters.limit);
      if (filters.offset) params.append('offset', filters.offset);
      
      const response = await api.get(`/requests?${params.toString()}`);
      set({ requests: response.data, loading: false });
      return response.data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },
  
  fetchRequest: async (id) => {
    set({ loading: true, error: null });
    try {
      const response = await api.get(`/requests/${id}`);
      set({ currentRequest: response.data, loading: false });
      return response.data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },
  
  createRequest: async (requestData) => {
    set({ loading: true, error: null });
    try {
      const response = await api.post('/requests', requestData);
      const newRequest = response.data;
      
      set(state => ({
        requests: [newRequest, ...state.requests],
        loading: false
      }));
      
      return newRequest;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },
  
  createAudioRequest: async (audioFile, team, templateId) => {
    set({ loading: true, error: null });
    try {
      const formData = new FormData();
      formData.append('audio', audioFile);
      formData.append('team', team);
      if (templateId) formData.append('template_id', templateId);
      
      const response = await api.post('/requests/audio', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      return response.data;
    } catch (error) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },
  
  approveRequest: async (id) => {
    try {
      await api.post(`/requests/${id}/approve`);
      set(state => ({
        requests: state.requests.map(req => 
          req.id === id ? { ...req, status: 'approved' } : req
        ),
        currentRequest: state.currentRequest?.id === id 
          ? { ...state.currentRequest, status: 'approved' }
          : state.currentRequest
      }));
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },
  
  requestRevision: async (id, instructions) => {
    try {
      await api.post(`/requests/${id}/revise`, { instructions });
      set(state => ({
        requests: state.requests.map(req => 
          req.id === id ? { ...req, status: 'needs_info' } : req
        ),
        currentRequest: state.currentRequest?.id === id 
          ? { ...state.currentRequest, status: 'needs_info' }
          : state.currentRequest
      }));
    } catch (error) {
      set({ error: error.message });
      throw error;
    }
  },
  
  subscribeToRequest: (id, onUpdate) => {
    const eventSource = new EventSource(`/api/requests/${id}/stream`);
    
    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onUpdate(data);
        
        // Update store if needed
        if (data.type === 'status_change' || data.type === 'step_update') {
          set(state => ({
            requests: state.requests.map(req => 
              req.id === id ? { ...req, ...data.data } : req
            ),
            currentRequest: state.currentRequest?.id === id 
              ? { ...state.currentRequest, ...data.data }
              : state.currentRequest
          }));
        }
      } catch (error) {
        console.error('Error parsing SSE data:', error);
      }
    };
    
    eventSource.onerror = (error) => {
      console.error('SSE error:', error);
    };
    
    return eventSource;
  },
  
  clearError: () => set({ error: null }),
  clearCurrentRequest: () => set({ currentRequest: null })
}));

export default useRequestStore;
