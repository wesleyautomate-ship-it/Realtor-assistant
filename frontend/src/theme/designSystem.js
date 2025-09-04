// Design System Constants for Dubai RAG System
// This file defines our visual design standards and priority color coding

export const PRIORITY_COLORS = {
  // Priority-based color coding
  high: {
    primary: '#d32f2f',      // Red for high priority
    light: '#ffcdd2',
    dark: '#b71c1c',
    contrast: '#ffffff'
  },
  medium: {
    primary: '#f57c00',      // Orange for medium priority
    light: '#ffe0b2',
    dark: '#e65100',
    contrast: '#ffffff'
  },
  low: {
    primary: '#388e3c',      // Green for low priority
    light: '#c8e6c9',
    dark: '#2e7d32',
    contrast: '#ffffff'
  },
  ai: {
    primary: '#1976d2',      // Blue for AI-generated content
    light: '#bbdefb',
    dark: '#0d47a1',
    contrast: '#ffffff'
  },
  neutral: {
    primary: '#757575',      // Gray for neutral items
    light: '#eeeeee',
    dark: '#424242',
    contrast: '#ffffff'
  }
};

export const STATUS_COLORS = {
  // Status-based color coding
  processing: {
    primary: '#1976d2',      // Blue for in-progress
    light: '#bbdefb',
    dark: '#0d47a1'
  },
  completed: {
    primary: '#388e3c',      // Green for completed
    light: '#c8e6c9',
    dark: '#2e7d32'
  },
  error: {
    primary: '#d32f2f',      // Red for errors
    light: '#ffcdd2',
    dark: '#b71c1c'
  },
  pending: {
    primary: '#f57c00',      // Orange for pending
    light: '#ffe0b2',
    dark: '#e65100'
  },
  paused: {
    primary: '#ff9800',      // Amber for paused
    light: '#ffe0b2',
    dark: '#f57c00'
  }
};

export const TYPOGRAPHY_SCALE = {
  // Typography hierarchy with consistent scaling
  h1: {
    fontSize: '2.5rem',
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.02em'
  },
  h2: {
    fontSize: '2rem',
    fontWeight: 600,
    lineHeight: 1.3,
    letterSpacing: '-0.01em'
  },
  h3: {
    fontSize: '1.75rem',
    fontWeight: 600,
    lineHeight: 1.3,
    letterSpacing: '-0.01em'
  },
  h4: {
    fontSize: '1.5rem',
    fontWeight: 600,
    lineHeight: 1.4,
    letterSpacing: '0em'
  },
  h5: {
    fontSize: '1.25rem',
    fontWeight: 600,
    lineHeight: 1.4,
    letterSpacing: '0em'
  },
  h6: {
    fontSize: '1.125rem',
    fontWeight: 600,
    lineHeight: 1.4,
    letterSpacing: '0em'
  },
  subtitle1: {
    fontSize: '1rem',
    fontWeight: 500,
    lineHeight: 1.5,
    letterSpacing: '0.01em'
  },
  subtitle2: {
    fontSize: '0.875rem',
    fontWeight: 500,
    lineHeight: 1.5,
    letterSpacing: '0.01em'
  },
  body1: {
    fontSize: '1rem',
    fontWeight: 400,
    lineHeight: 1.6,
    letterSpacing: '0.01em'
  },
  body2: {
    fontSize: '0.875rem',
    fontWeight: 400,
    lineHeight: 1.6,
    letterSpacing: '0.01em'
  },
  caption: {
    fontSize: '0.75rem',
    fontWeight: 400,
    lineHeight: 1.5,
    letterSpacing: '0.02em'
  },
  button: {
    fontSize: '0.875rem',
    fontWeight: 500,
    lineHeight: 1.75,
    letterSpacing: '0.02em',
    textTransform: 'none'
  }
};

export const SPACING_SCALE = {
  // Consistent spacing scale (8px base unit)
  xs: '0.25rem',    // 4px
  sm: '0.5rem',     // 8px
  md: '1rem',       // 16px
  lg: '1.5rem',     // 24px
  xl: '2rem',       // 32px
  xxl: '3rem',      // 48px
  xxxl: '4rem'      // 64px
};

export const BORDER_RADIUS = {
  // Consistent border radius values
  xs: '0.25rem',    // 4px
  sm: '0.5rem',     // 8px
  md: '0.75rem',    // 12px
  lg: '1rem',       // 16px
  xl: '1.5rem',     // 24px
  round: '50%'      // Circular
};

export const SHADOWS = {
  // Elevation and shadow system
  none: 'none',
  xs: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  sm: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
  xxl: '0 25px 50px -12px rgba(0, 0, 0, 0.25)'
};

export const TRANSITIONS = {
  // Smooth transition timing
  fast: '150ms ease-in-out',
  normal: '250ms ease-in-out',
  slow: '350ms ease-in-out',
  bounce: '250ms cubic-bezier(0.68, -0.55, 0.265, 1.55)'
};

export const Z_INDEX = {
  // Z-index layering system
  base: 1,
  card: 10,
  dropdown: 100,
  sticky: 200,
  fixed: 300,
  modal: 400,
  popover: 500,
  tooltip: 600,
  toast: 700
};

// Helper function to get priority color
export const getPriorityColor = (priority) => {
  return PRIORITY_COLORS[priority] || PRIORITY_COLORS.neutral;
};

// Helper function to get status color
export const getStatusColor = (status) => {
  return STATUS_COLORS[status] || STATUS_COLORS.neutral;
};

// Helper function to get AI score color
export const getAIScoreColor = (score) => {
  if (score >= 90) return PRIORITY_COLORS.low.primary;
  if (score >= 80) return PRIORITY_COLORS.medium.primary;
  if (score >= 70) return PRIORITY_COLORS.ai.primary;
  return PRIORITY_COLORS.high.primary;
};
