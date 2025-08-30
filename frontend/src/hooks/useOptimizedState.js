/**
 * Optimized State Management Hook for Dubai Real Estate RAG System
 * 
 * This hook provides optimized state management to prevent infinite loops,
 * stale state issues, and unnecessary re-renders in React components.
 */

import { useState, useCallback, useRef, useEffect, useMemo } from 'react';

/**
 * Custom hook for optimized state management
 * @param {any} initialState - Initial state value
 * @param {Object} options - Configuration options
 * @returns {Array} [state, setState, resetState]
 */
export const useOptimizedState = (initialState, options = {}) => {
  const {
    equalityCheck = (prev, next) => prev === next,
    debounceMs = 0,
    maxHistory = 10
  } = options;

  const [state, setStateInternal] = useState(initialState);
  const stateRef = useRef(state);
  const historyRef = useRef([]);
  const timeoutRef = useRef(null);
  const isUpdatingRef = useRef(false);

  // Update ref when state changes
  useEffect(() => {
    stateRef.current = state;
  }, [state]);

  // Debounced setState
  const setState = useCallback((newState) => {
    if (isUpdatingRef.current) {
      console.warn('State update blocked: update already in progress');
      return;
    }

    const updateState = () => {
      isUpdatingRef.current = true;
      
      try {
        const nextState = typeof newState === 'function' ? newState(stateRef.current) : newState;
        
        // Check if state actually changed
        if (!equalityCheck(stateRef.current, nextState)) {
          // Add to history
          historyRef.current.push(stateRef.current);
          if (historyRef.current.length > maxHistory) {
            historyRef.current.shift();
          }
          
          setStateInternal(nextState);
        }
      } finally {
        isUpdatingRef.current = false;
      }
    };

    if (debounceMs > 0) {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
      timeoutRef.current = setTimeout(updateState, debounceMs);
    } else {
      updateState();
    }
  }, [equalityCheck, debounceMs, maxHistory]);

  // Reset state to initial value
  const resetState = useCallback(() => {
    setState(initialState);
    historyRef.current = [];
  }, [initialState, setState]);

  // Undo last state change
  const undoState = useCallback(() => {
    if (historyRef.current.length > 0) {
      const previousState = historyRef.current.pop();
      setStateInternal(previousState);
    }
  }, []);

  // Cleanup timeout on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);

  return [state, setState, resetState, undoState];
};

/**
 * Hook for managing async state with loading and error states
 * @param {any} initialState - Initial state value
 * @returns {Object} { state, setState, loading, error, setLoading, setError, reset }
 */
export const useAsyncState = (initialState) => {
  const [state, setState] = useState(initialState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const reset = useCallback(() => {
    setState(initialState);
    setLoading(false);
    setError(null);
  }, [initialState]);

  return {
    state,
    setState,
    loading,
    error,
    setLoading,
    setError,
    reset
  };
};

/**
 * Hook for managing form state with validation
 * @param {Object} initialValues - Initial form values
 * @param {Object} validationSchema - Validation schema
 * @returns {Object} Form state and handlers
 */
export const useFormState = (initialValues, validationSchema = {}) => {
  const [values, setValues] = useState(initialValues);
  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Validate a single field
  const validateField = useCallback((name, value) => {
    if (!validationSchema[name]) return '';
    
    const validator = validationSchema[name];
    if (typeof validator === 'function') {
      return validator(value, values) || '';
    }
    
    return '';
  }, [validationSchema, values]);

  // Validate all fields
  const validateForm = useCallback(() => {
    const newErrors = {};
    Object.keys(validationSchema).forEach(field => {
      const error = validateField(field, values[field]);
      if (error) {
        newErrors[field] = error;
      }
    });
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [validationSchema, values, validateField]);

  // Handle field change
  const handleChange = useCallback((name, value) => {
    setValues(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  }, [errors]);

  // Handle field blur
  const handleBlur = useCallback((name) => {
    setTouched(prev => ({ ...prev, [name]: true }));
    const error = validateField(name, values[name]);
    setErrors(prev => ({ ...prev, [name]: error }));
  }, [validateField, values]);

  // Reset form
  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  // Check if form is valid
  const isValid = useMemo(() => {
    return Object.keys(errors).length === 0 && 
           Object.keys(validationSchema).every(field => values[field] !== undefined && values[field] !== '');
  }, [errors, validationSchema, values]);

  return {
    values,
    errors,
    touched,
    isSubmitting,
    isValid,
    setValues,
    setErrors,
    setIsSubmitting,
    handleChange,
    handleBlur,
    validateField,
    validateForm,
    reset
  };
};

/**
 * Hook for managing list state with pagination and filtering
 * @param {Array} initialItems - Initial list items
 * @param {Object} options - Configuration options
 * @returns {Object} List state and handlers
 */
export const useListState = (initialItems = [], options = {}) => {
  const {
    pageSize = 10,
    initialPage = 1,
    sortBy = null,
    sortDirection = 'asc'
  } = options;

  const [items, setItems] = useState(initialItems);
  const [filteredItems, setFilteredItems] = useState(initialItems);
  const [currentPage, setCurrentPage] = useState(initialPage);
  const [sortConfig, setSortConfig] = useState({ field: sortBy, direction: sortDirection });
  const [filters, setFilters] = useState({});
  const [loading, setLoading] = useState(false);

  // Apply filters and sorting
  const applyFiltersAndSort = useCallback((itemsToProcess, newFilters, newSortConfig) => {
    let processed = [...itemsToProcess];

    // Apply filters
    Object.entries(newFilters).forEach(([field, value]) => {
      if (value !== undefined && value !== '') {
        processed = processed.filter(item => {
          const itemValue = item[field];
          if (typeof value === 'string') {
            return itemValue?.toLowerCase().includes(value.toLowerCase());
          }
          return itemValue === value;
        });
      }
    });

    // Apply sorting
    if (newSortConfig.field) {
      processed.sort((a, b) => {
        const aValue = a[newSortConfig.field];
        const bValue = b[newSortConfig.field];
        
        if (aValue < bValue) return newSortConfig.direction === 'asc' ? -1 : 1;
        if (aValue > bValue) return newSortConfig.direction === 'asc' ? 1 : -1;
        return 0;
      });
    }

    return processed;
  }, []);

  // Update filtered items when items, filters, or sort config changes
  useEffect(() => {
    const processed = applyFiltersAndSort(items, filters, sortConfig);
    setFilteredItems(processed);
    setCurrentPage(1); // Reset to first page when filters change
  }, [items, filters, sortConfig, applyFiltersAndSort]);

  // Get paginated items
  const paginatedItems = useMemo(() => {
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    return filteredItems.slice(startIndex, endIndex);
  }, [filteredItems, currentPage, pageSize]);

  // Add item
  const addItem = useCallback((item) => {
    setItems(prev => [...prev, item]);
  }, []);

  // Update item
  const updateItem = useCallback((id, updates) => {
    setItems(prev => prev.map(item => 
      item.id === id ? { ...item, ...updates } : item
    ));
  }, []);

  // Remove item
  const removeItem = useCallback((id) => {
    setItems(prev => prev.filter(item => item.id !== id));
  }, []);

  // Set filters
  const setFilter = useCallback((field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
  }, []);

  // Clear filters
  const clearFilters = useCallback(() => {
    setFilters({});
  }, []);

  // Set sort configuration
  const setSort = useCallback((field) => {
    setSortConfig(prev => ({
      field,
      direction: prev.field === field && prev.direction === 'asc' ? 'desc' : 'asc'
    }));
  }, []);

  // Go to page
  const goToPage = useCallback((page) => {
    const maxPage = Math.ceil(filteredItems.length / pageSize);
    if (page >= 1 && page <= maxPage) {
      setCurrentPage(page);
    }
  }, [filteredItems.length, pageSize]);

  return {
    // State
    items,
    filteredItems,
    paginatedItems,
    currentPage,
    totalPages: Math.ceil(filteredItems.length / pageSize),
    totalItems: filteredItems.length,
    sortConfig,
    filters,
    loading,
    
    // Actions
    setItems,
    addItem,
    updateItem,
    removeItem,
    setFilter,
    clearFilters,
    setSort,
    goToPage,
    setLoading,
    
    // Computed
    hasNextPage: currentPage < Math.ceil(filteredItems.length / pageSize),
    hasPrevPage: currentPage > 1
  };
};

/**
 * Hook for managing API state with caching and error handling
 * @param {Function} apiFunction - API function to call
 * @param {Object} options - Configuration options
 * @returns {Object} API state and handlers
 */
export const useApiState = (apiFunction, options = {}) => {
  const {
    cacheKey = null,
    cacheDuration = 5 * 60 * 1000, // 5 minutes
    autoFetch = false,
    dependencies = []
  } = options;

  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [lastFetched, setLastFetched] = useState(null);
  const cacheRef = useRef(new Map());

  // Check if data is cached and valid
  const getCachedData = useCallback(() => {
    if (!cacheKey) return null;
    
    const cached = cacheRef.current.get(cacheKey);
    if (cached && Date.now() - cached.timestamp < cacheDuration) {
      return cached.data;
    }
    
    return null;
  }, [cacheKey, cacheDuration]);

  // Set cached data
  const setCachedData = useCallback((key, data) => {
    if (key) {
      cacheRef.current.set(key, {
        data,
        timestamp: Date.now()
      });
    }
  }, []);

  // Fetch data
  const fetchData = useCallback(async (...args) => {
    try {
      setLoading(true);
      setError(null);

      // Check cache first
      const cached = getCachedData();
      if (cached) {
        setData(cached);
        setLastFetched(Date.now());
        return cached;
      }

      // Fetch from API
      const result = await apiFunction(...args);
      
      setData(result);
      setLastFetched(Date.now());
      setCachedData(cacheKey, result);
      
      return result;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [apiFunction, cacheKey, getCachedData, setCachedData]);

  // Auto-fetch on mount or when dependencies change
  useEffect(() => {
    if (autoFetch) {
      fetchData();
    }
  }, [autoFetch, fetchData, ...dependencies]);

  // Clear cache
  const clearCache = useCallback(() => {
    if (cacheKey) {
      cacheRef.current.delete(cacheKey);
    }
  }, [cacheKey]);

  // Clear all cache
  const clearAllCache = useCallback(() => {
    cacheRef.current.clear();
  }, []);

  return {
    data,
    loading,
    error,
    lastFetched,
    fetchData,
    setData,
    setError,
    clearCache,
    clearAllCache
  };
};
