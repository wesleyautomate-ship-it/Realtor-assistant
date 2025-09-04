import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import {
  Box,
  CircularProgress,
  useTheme,
  Fade,
  Grow,
  useMediaQuery,
} from '@mui/material';
import { 
  SPACING_SCALE, 
  BORDER_RADIUS, 
  TRANSITIONS,
  SHADOWS 
} from '../../theme/designSystem';

// Performance-optimized components with accessibility features

// Lazy loading wrapper with intersection observer
export const LazyLoad = ({ 
  children, 
  threshold = 0.1, 
  rootMargin = '50px',
  fallback = null,
  ...props 
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold, rootMargin }
    );

    if (ref.current) {
      observer.observe(ref.current);
    }

    return () => observer.disconnect();
  }, [threshold, rootMargin]);

  useEffect(() => {
    if (isVisible) {
      // Simulate loading delay for better UX
      const timer = setTimeout(() => setIsLoaded(true), 100);
      return () => clearTimeout(timer);
    }
  }, [isVisible]);

  return (
    <Box ref={ref} {...props}>
      {!isLoaded ? (
        fallback || (
          <Box
            sx={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              p: 3,
              borderRadius: BORDER_RADIUS.md,
              bgcolor: 'background.paper',
              border: '1px solid',
              borderColor: 'divider',
            }}
          >
            <CircularProgress size={24} />
          </Box>
        )
      ) : (
        <Fade in={isLoaded} timeout={300}>
          <Box>{children}</Box>
        </Fade>
      )}
    </Box>
  );
};

// Memoized list item for performance
export const MemoizedListItem = React.memo(({ 
  item, 
  renderItem, 
  onClick,
  selected = false,
  ...props 
}) => {
  const theme = useTheme();
  
  const handleClick = useCallback(() => {
    onClick?.(item);
  }, [item, onClick]);

  return (
    <Box
      onClick={handleClick}
      sx={{
        p: 2,
        borderRadius: BORDER_RADIUS.md,
        border: `1px solid ${theme.palette.divider}`,
        bgcolor: selected ? 'primary.light' : 'background.paper',
        cursor: onClick ? 'pointer' : 'default',
        transition: TRANSITIONS.normal,
        '&:hover': onClick ? {
          bgcolor: selected ? 'primary.main' : 'action.hover',
          transform: 'translateY(-1px)',
          boxShadow: SHADOWS.md,
        } : {},
        ...props.sx,
      }}
      {...props}
    >
      {renderItem(item)}
    </Box>
  );
});

// Virtual scrolling container for large lists
export const VirtualList = ({ 
  items, 
  itemHeight = 72, 
  containerHeight = 400,
  renderItem,
  onItemClick,
  selectedIndex = -1,
  ...props 
}) => {
  const [scrollTop, setScrollTop] = useState(0);
  const containerRef = useRef(null);
  const theme = useTheme();

  const visibleItemCount = Math.ceil(containerHeight / itemHeight);
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(startIndex + visibleItemCount + 1, items.length);

  const visibleItems = useMemo(() => {
    return items.slice(startIndex, endIndex);
  }, [items, startIndex, endIndex]);

  const totalHeight = items.length * itemHeight;
  const offsetY = startIndex * itemHeight;

  const handleScroll = useCallback((event) => {
    setScrollTop(event.target.scrollTop);
  }, []);

  const scrollToItem = useCallback((index) => {
    if (containerRef.current) {
      const scrollTop = index * itemHeight;
      containerRef.current.scrollTop = scrollTop;
    }
  }, [itemHeight]);

  // Auto-scroll to selected item
  useEffect(() => {
    if (selectedIndex >= 0 && selectedIndex < items.length) {
      scrollToItem(selectedIndex);
    }
  }, [selectedIndex, items.length, scrollToItem]);

  return (
    <Box
      ref={containerRef}
      onScroll={handleScroll}
      sx={{
        height: containerHeight,
        overflow: 'auto',
        borderRadius: BORDER_RADIUS.md,
        border: `1px solid ${theme.palette.divider}`,
        bgcolor: 'background.paper',
        '&::-webkit-scrollbar': {
          width: '8px',
        },
        '&::-webkit-scrollbar-track': {
          bgcolor: 'grey.100',
          borderRadius: BORDER_RADIUS.round,
        },
        '&::-webkit-scrollbar-thumb': {
          bgcolor: 'grey.400',
          borderRadius: BORDER_RADIUS.round,
          '&:hover': {
            bgcolor: 'grey.500',
          },
        },
        ...props.sx,
      }}
      {...props}
    >
      <Box sx={{ height: totalHeight, position: 'relative' }}>
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            transform: `translateY(${offsetY}px)`,
          }}
        >
          {visibleItems.map((item, index) => (
            <Box
              key={startIndex + index}
              sx={{
                height: itemHeight,
                display: 'flex',
                alignItems: 'center',
                px: 2,
                borderBottom: index < visibleItems.length - 1 ? `1px solid ${theme.palette.divider}` : 'none',
              }}
            >
              {renderItem(item, startIndex + index)}
            </Box>
          ))}
        </Box>
      </Box>
    </Box>
  );
};

// Debounced search input for performance
export const DebouncedSearch = ({ 
  onSearch, 
  placeholder = 'Search...',
  delay = 300,
  minLength = 2,
  ...props 
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const searchTimeoutRef = useRef(null);
  const theme = useTheme();

  const debouncedSearch = useCallback(
    (term) => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }

      searchTimeoutRef.current = setTimeout(() => {
        if (term.length >= minLength) {
          setIsSearching(true);
          onSearch(term).finally(() => setIsSearching(false));
        } else if (term.length === 0) {
          onSearch('');
        }
      }, delay);
    },
    [onSearch, delay, minLength]
  );

  const handleChange = useCallback((event) => {
    const value = event.target.value;
    setSearchTerm(value);
    debouncedSearch(value);
  }, [debouncedSearch]);

  useEffect(() => {
    return () => {
      if (searchTimeoutRef.current) {
        clearTimeout(searchTimeoutRef.current);
      }
    };
  }, []);

  return (
    <Box sx={{ position: 'relative' }}>
      <input
        type="text"
        value={searchTerm}
        onChange={handleChange}
        placeholder={placeholder}
        style={{
          width: '100%',
          padding: '12px 16px',
          border: `1px solid ${theme.palette.divider}`,
          borderRadius: BORDER_RADIUS.md,
          fontSize: '14px',
          outline: 'none',
          transition: TRANSITIONS.normal,
        }}
        {...props}
      />
      {isSearching && (
        <Box
          sx={{
            position: 'absolute',
            right: 12,
            top: '50%',
            transform: 'translateY(-50%)',
          }}
        >
          <CircularProgress size={16} />
        </Box>
      )}
    </Box>
  );
};

// Responsive image with lazy loading and optimization
export const OptimizedImage = ({ 
  src, 
  alt, 
  width, 
  height, 
  fallback,
  lazy = true,
  ...props 
}) => {
  const [isLoaded, setIsLoaded] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [imageSrc, setImageSrc] = useState(lazy ? '' : src);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));

  useEffect(() => {
    if (lazy) {
      const observer = new IntersectionObserver(
        ([entry]) => {
          if (entry.isIntersecting) {
            setImageSrc(src);
            observer.disconnect();
          }
        },
        { threshold: 0.1 }
      );

      const img = document.createElement('img');
      observer.observe(img);
      return () => observer.disconnect();
    }
  }, [src, lazy]);

  const handleLoad = useCallback(() => {
    setIsLoaded(true);
  }, []);

  const handleError = useCallback(() => {
    setHasError(true);
  }, []);

  if (hasError && fallback) {
    return (
      <Box
        sx={{
          width,
          height,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: 'grey.100',
          borderRadius: BORDER_RADIUS.md,
          color: 'text.secondary',
          fontSize: '0.875rem',
        }}
      >
        {fallback}
      </Box>
    );
  }

  return (
    <Box
      sx={{
        position: 'relative',
        width,
        height,
        overflow: 'hidden',
        borderRadius: BORDER_RADIUS.md,
        bgcolor: 'grey.100',
        ...props.sx,
      }}
      {...props}
    >
      {imageSrc && (
        <img
          src={imageSrc}
          alt={alt}
          width={width}
          height={height}
          onLoad={handleLoad}
          onError={handleError}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            opacity: isLoaded ? 1 : 0,
            transition: TRANSITIONS.normal,
          }}
        />
      )}
      
      {!isLoaded && (
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            bgcolor: 'grey.200',
          }}
        >
          <CircularProgress size={24} />
        </Box>
      )}
    </Box>
  );
};

// Performance monitoring hook
export const usePerformanceMonitor = (componentName) => {
  const renderCount = useRef(0);
  const lastRenderTime = useRef(performance.now());

  useEffect(() => {
    renderCount.current += 1;
    const currentTime = performance.now();
    const timeSinceLastRender = currentTime - lastRenderTime.current;
    
    console.log(`[${componentName}] Render #${renderCount.current} (${timeSinceLastRender.toFixed(2)}ms)`);
    
    lastRenderTime.current = currentTime;
  });

  return {
    renderCount: renderCount.current,
    lastRenderTime: lastRenderTime.current,
  };
};

// Accessibility wrapper for keyboard navigation
export const KeyboardNavigable = ({ 
  children, 
  onKeyDown,
  tabIndex = 0,
  role = 'button',
  ...props 
}) => {
  const handleKeyDown = useCallback((event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      onKeyDown?.(event);
    }
  }, [onKeyDown]);

  return (
    <Box
      tabIndex={tabIndex}
      role={role}
      onKeyDown={handleKeyDown}
      sx={{
        outline: 'none',
        '&:focus-visible': {
          outline: '2px solid',
          outlineColor: 'primary.main',
          outlineOffset: '2px',
        },
        ...props.sx,
      }}
      {...props}
    >
      {children}
    </Box>
  );
};

// Export all performance components
export default {
  LazyLoad,
  MemoizedListItem,
  VirtualList,
  DebouncedSearch,
  OptimizedImage,
  usePerformanceMonitor,
  KeyboardNavigable,
};
