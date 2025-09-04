// Mock axios module for testing
const mockAxios = {
  // Mock HTTP methods
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  patch: jest.fn(),
  
  // Mock request method
  request: jest.fn(),
  
  // Mock interceptors
  interceptors: {
    request: {
      use: jest.fn(),
      eject: jest.fn(),
    },
    response: {
      use: jest.fn(),
      eject: jest.fn(),
    },
  },
  
  // Mock create method
  create: jest.fn(() => mockAxios),
  
  // Mock defaults
  defaults: {
    baseURL: '',
    headers: {},
    timeout: 0,
  },
  
  // Mock isAxiosError
  isAxiosError: jest.fn(),
  
  // Mock CancelToken
  CancelToken: {
    source: jest.fn(() => ({
      token: 'mock-token',
      cancel: jest.fn(),
    })),
  },
};

// Set up default mock responses
mockAxios.get.mockResolvedValue({ data: {}, status: 200, statusText: 'OK' });
mockAxios.post.mockResolvedValue({ data: {}, status: 201, statusText: 'Created' });
mockAxios.put.mockResolvedValue({ data: {}, status: 200, statusText: 'OK' });
mockAxios.delete.mockResolvedValue({ data: {}, status: 204, statusText: 'No Content' });
mockAxios.patch.mockResolvedValue({ data: {}, status: 200, statusText: 'OK' });

// Export as both default and named export
module.exports = mockAxios;
module.exports.default = mockAxios;
