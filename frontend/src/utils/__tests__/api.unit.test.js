import { apiUtils, handleApiError } from '../api';

// Mock the axios instance
jest.mock('../api', () => {
  const originalModule = jest.requireActual('../api');
  return {
    ...originalModule,
    api: {
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn(),
      interceptors: {
        request: { use: jest.fn() },
        response: { use: jest.fn() }
      }
    }
  };
});

describe('API Utility Functions Unit Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Properties API', () => {
    it('should fetch properties with filters', async () => {
      const mockResponse = { data: [{ id: 1, title: 'Test Property' }] };
      const mockApi = require('../api').default;
      mockApi.get.mockResolvedValue(mockResponse);

      const result = await apiUtils.getProperties({ location: 'Dubai', type: 'apartment' });
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.get).toHaveBeenCalledWith('/properties?location=Dubai&type=apartment');
    });

    it('should handle empty filters', async () => {
      const mockResponse = { data: [{ id: 1, title: 'Test Property' }] };
      const mockApi = require('../api').default;
      mockApi.get.mockResolvedValue(mockResponse);

      const result = await apiUtils.getProperties();
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.get).toHaveBeenCalledWith('/properties?');
    });
  });

  describe('Chat API', () => {
    it('should send message without file upload', async () => {
      const mockResponse = { data: { message: 'Response received' } };
      const mockApi = require('../api').default;
      mockApi.post.mockResolvedValue(mockResponse);

      const result = await apiUtils.sendMessage('session123', 'Hello', null);
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.post).toHaveBeenCalledWith('/sessions/session123/chat', {
        message: 'Hello',
        session_id: 'session123'
      });
    });

    it('should send message with file upload', async () => {
      const mockResponse = { data: { message: 'Response received' } };
      const mockApi = require('../api').default;
      mockApi.post.mockResolvedValue(mockResponse);

      const result = await apiUtils.sendMessage('session123', 'Hello', { id: 'file123' });
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.post).toHaveBeenCalledWith('/sessions/session123/chat', {
        message: 'Hello',
        session_id: 'session123',
        file_upload: { file_id: 'file123' }
      });
    });
  });

  describe('Phase 3 API Functions', () => {
    it('should detect entities', async () => {
      const mockResponse = { data: { entities: [{ type: 'property', id: 1 }] } };
      const mockApi = require('../api').default;
      mockApi.post.mockResolvedValue(mockResponse);

      const result = await apiUtils.detectEntities('Test message');
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.post).toHaveBeenCalledWith('/phase3/ai/detect-entities', {
        message: 'Test message',
        conversation_id: null
      });
    });

    it('should fetch entity context', async () => {
      const mockResponse = { data: { context: 'Property details' } };
      const mockApi = require('../api').default;
      mockApi.get.mockResolvedValue(mockResponse);

      const result = await apiUtils.fetchEntityContext('property', 1);
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.get).toHaveBeenCalledWith('/phase3/context/property/1');
    });

    it('should get property details', async () => {
      const mockResponse = { data: { property: 'Details' } };
      const mockApi = require('../api').default;
      mockApi.get.mockResolvedValue(mockResponse);

      const result = await apiUtils.getPropertyDetails(1);
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.get).toHaveBeenCalledWith('/phase3/properties/1/details');
    });

    it('should get client info', async () => {
      const mockResponse = { data: { client: 'Info' } };
      const mockApi = require('../api').default;
      mockApi.get.mockResolvedValue(mockResponse);

      const result = await apiUtils.getClientInfo(1);
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.get).toHaveBeenCalledWith('/phase3/clients/1');
    });

    it('should get market context', async () => {
      const mockResponse = { data: { market: 'Context' } };
      const mockApi = require('../api').default;
      mockApi.get.mockResolvedValue(mockResponse);

      const result = await apiUtils.getMarketContext('Dubai', 'apartment');
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.get).toHaveBeenCalledWith('/phase3/market/context?location=Dubai&property_type=apartment');
    });

    it('should batch fetch context', async () => {
      const mockResponse = { data: { contexts: [] } };
      const mockApi = require('../api').default;
      mockApi.post.mockResolvedValue(mockResponse);

      const entities = [{ type: 'property', id: 1, name: 'Test' }];
      const result = await apiUtils.batchFetchContext(entities);
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.post).toHaveBeenCalledWith('/phase3/context/batch', {
        entities: [{ type: 'property', id: 1, name: 'Test' }]
      });
    });

    it('should clear context cache', async () => {
      const mockResponse = { data: { message: 'Cache cleared' } };
      const mockApi = require('../api').default;
      mockApi.delete.mockResolvedValue(mockResponse);

      const result = await apiUtils.clearContextCache();
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.delete).toHaveBeenCalledWith('/phase3/context/cache/clear');
    });

    it('should get Phase 3 health', async () => {
      const mockResponse = { data: { status: 'healthy' } };
      const mockApi = require('../api').default;
      mockApi.get.mockResolvedValue(mockResponse);

      const result = await apiUtils.getPhase3Health();
      
      expect(result).toEqual(mockResponse.data);
      expect(mockApi.get).toHaveBeenCalledWith('/phase3/health');
    });
  });

  describe('Error Handling', () => {
    it('should handle 401 errors', () => {
      const error = { response: { status: 401, data: { detail: 'Unauthorized' } } };
      const result = handleApiError(error);
      expect(result).toBe('Please log in to continue');
    });

    it('should handle 403 errors', () => {
      const error = { response: { status: 403, data: { detail: 'Forbidden' } } };
      const result = handleApiError(error);
      expect(result).toBe('You do not have permission to perform this action');
    });

    it('should handle 404 errors', () => {
      const error = { response: { status: 404, data: { detail: 'Not found' } } };
      const result = handleApiError(error);
      expect(result).toBe('The requested resource was not found');
    });

    it('should handle 422 errors', () => {
      const error = { response: { status: 422, data: { detail: 'Validation failed' } } };
      const result = handleApiError(error);
      expect(result).toBe('Validation failed');
    });

    it('should handle 500 errors', () => {
      const error = { response: { status: 500, data: { detail: 'Server error' } } };
      const result = handleApiError(error);
      expect(result).toBe('Server error. Please try again later.');
    });

    it('should handle network errors', () => {
      const error = { request: 'Network error' };
      const result = handleApiError(error);
      expect(result).toBe('Network error. Please check your connection and try again.');
    });

    it('should handle unexpected errors', () => {
      const error = { message: 'Unexpected error' };
      const result = handleApiError(error);
      expect(result).toBe('An unexpected error occurred. Please try again.');
    });

    it('should handle errors with custom detail messages', () => {
      const error = { response: { status: 400, data: { detail: 'Custom error message' } } };
      const result = handleApiError(error);
      expect(result).toBe('Custom error message');
    });
  });

  describe('API Configuration', () => {
    it('should have proper base URL', () => {
      const mockApi = require('../api').default;
      expect(mockApi.defaults?.baseURL).toBeDefined();
    });

    it('should have proper headers', () => {
      const mockApi = require('../api').default;
      expect(mockApi.defaults?.headers).toBeDefined();
    });

    it('should have proper timeout', () => {
      const mockApi = require('../api').default;
      expect(mockApi.defaults?.timeout).toBeDefined();
    });
  });
});
