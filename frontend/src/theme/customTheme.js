import { createTheme } from '@mui/material/styles';
import { 
  PRIORITY_COLORS, 
  STATUS_COLORS, 
  TYPOGRAPHY_SCALE, 
  SPACING_SCALE, 
  BORDER_RADIUS, 
  SHADOWS, 
  TRANSITIONS 
} from './designSystem';

// Create custom theme extending Material-UI's default theme
export const customTheme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#0d47a1',
      contrastText: '#ffffff',
    },
    secondary: {
      main: '#f57c00',
      light: '#ffb74d',
      dark: '#e65100',
      contrastText: '#ffffff',
    },
    success: {
      main: PRIORITY_COLORS.low.primary,
      light: PRIORITY_COLORS.low.light,
      dark: PRIORITY_COLORS.low.dark,
      contrastText: PRIORITY_COLORS.low.contrast,
    },
    warning: {
      main: PRIORITY_COLORS.medium.primary,
      light: PRIORITY_COLORS.medium.light,
      dark: PRIORITY_COLORS.medium.dark,
      contrastText: PRIORITY_COLORS.medium.contrast,
    },
    error: {
      main: PRIORITY_COLORS.high.primary,
      light: PRIORITY_COLORS.high.light,
      dark: PRIORITY_COLORS.high.dark,
      contrastText: PRIORITY_COLORS.high.contrast,
    },
    info: {
      main: PRIORITY_COLORS.ai.primary,
      light: PRIORITY_COLORS.ai.light,
      dark: PRIORITY_COLORS.ai.dark,
      contrastText: PRIORITY_COLORS.ai.contrast,
    },
    grey: {
      50: '#fafafa',
      100: '#f5f5f5',
      200: '#eeeeee',
      300: '#e0e0e0',
      400: '#bdbdbd',
      500: '#9e9e9e',
      600: '#757575',
      700: '#616161',
      800: '#424242',
      900: '#212121',
    },
    background: {
      default: '#fafafa',
      paper: '#ffffff',
    },
    text: {
      primary: '#212121',
      secondary: '#616161',
      disabled: '#9e9e9e',
    },
    divider: '#e0e0e0',
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
      '"Apple Color Emoji"',
      '"Segoe UI Emoji"',
      '"Segoe UI Symbol"',
    ].join(','),
    h1: {
      ...TYPOGRAPHY_SCALE.h1,
      color: '#212121',
    },
    h2: {
      ...TYPOGRAPHY_SCALE.h2,
      color: '#212121',
    },
    h3: {
      ...TYPOGRAPHY_SCALE.h3,
      color: '#212121',
    },
    h4: {
      ...TYPOGRAPHY_SCALE.h4,
      color: '#212121',
    },
    h5: {
      ...TYPOGRAPHY_SCALE.h5,
      color: '#212121',
    },
    h6: {
      ...TYPOGRAPHY_SCALE.h6,
      color: '#212121',
    },
    subtitle1: {
      ...TYPOGRAPHY_SCALE.subtitle1,
      color: '#616161',
    },
    subtitle2: {
      ...TYPOGRAPHY_SCALE.subtitle2,
      color: '#616161',
    },
    body1: {
      ...TYPOGRAPHY_SCALE.body1,
      color: '#212121',
    },
    body2: {
      ...TYPOGRAPHY_SCALE.body2,
      color: '#616161',
    },
    caption: {
      ...TYPOGRAPHY_SCALE.caption,
      color: '#9e9e9e',
    },
    button: {
      ...TYPOGRAPHY_SCALE.button,
      fontWeight: 600,
    },
  },
  spacing: (factor) => {
    // Convert our spacing scale to Material-UI's spacing function
    const spacingMap = {
      0: SPACING_SCALE.xs,
      1: SPACING_SCALE.sm,
      2: SPACING_SCALE.md,
      3: SPACING_SCALE.lg,
      4: SPACING_SCALE.xl,
      5: SPACING_SCALE.xxl,
      6: SPACING_SCALE.xxxl,
    };
    return spacingMap[factor] || `${factor * 8}px`;
  },
  shape: {
    borderRadius: BORDER_RADIUS.md,
  },
  shadows: [
    SHADOWS.none,
    SHADOWS.xs,
    SHADOWS.sm,
    SHADOWS.md,
    SHADOWS.lg,
    SHADOWS.xl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
    SHADOWS.xxl,
  ],
  transitions: {
    create: (props, options) => {
      const duration = options?.duration || 250;
      const easing = options?.easing || 'ease-in-out';
      const delay = options?.delay || 0;
      
      if (Array.isArray(props)) {
        return props.map(prop => 
          `${prop} ${duration}ms ${easing} ${delay}ms`
        ).join(', ');
      }
      
      return `${props} ${duration}ms ${easing} ${delay}ms`;
    },
    easing: {
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0.0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
      sharp: 'cubic-bezier(0.4, 0, 0.6, 1)',
    },
    duration: {
      shortest: 150,
      shorter: 200,
      short: 250,
      standard: 300,
      complex: 375,
      enteringScreen: 225,
      leavingScreen: 195,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: BORDER_RADIUS.md,
          textTransform: 'none',
          fontWeight: 600,
          transition: TRANSITIONS.normal,
          '&:hover': {
            transform: 'translateY(-1px)',
            boxShadow: SHADOWS.md,
          },
        },
        contained: {
          boxShadow: SHADOWS.sm,
          '&:hover': {
            boxShadow: SHADOWS.md,
          },
        },
        outlined: {
          borderWidth: '2px',
          '&:hover': {
            borderWidth: '2px',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: BORDER_RADIUS.lg,
          boxShadow: SHADOWS.sm,
          transition: TRANSITIONS.normal,
          '&:hover': {
            boxShadow: SHADOWS.md,
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: BORDER_RADIUS.md,
        },
        elevation1: {
          boxShadow: SHADOWS.xs,
        },
        elevation2: {
          boxShadow: SHADOWS.sm,
        },
        elevation3: {
          boxShadow: SHADOWS.md,
        },
        elevation4: {
          boxShadow: SHADOWS.lg,
        },
        elevation5: {
          boxShadow: SHADOWS.xl,
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: BORDER_RADIUS.round,
          fontWeight: 500,
        },
        outlined: {
          borderWidth: '1.5px',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: BORDER_RADIUS.md,
          },
        },
      },
    },
    MuiDialog: {
      styleOverrides: {
        paper: {
          borderRadius: BORDER_RADIUS.lg,
          boxShadow: SHADOWS.xl,
        },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: {
          borderRadius: BORDER_RADIUS.md,
          fontWeight: 500,
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: {
          borderRadius: BORDER_RADIUS.round,
          height: '8px',
        },
        bar: {
          borderRadius: BORDER_RADIUS.round,
        },
      },
    },
  },
});

// Export priority and status color getters for easy access
export const getPriorityColor = (priority) => {
  return PRIORITY_COLORS[priority] || PRIORITY_COLORS.neutral;
};

export const getStatusColor = (status) => {
  return STATUS_COLORS[status] || STATUS_COLORS.neutral;
};

export const getAIScoreColor = (score) => {
  if (score >= 90) return PRIORITY_COLORS.low.primary;
  if (score >= 80) return PRIORITY_COLORS.medium.primary;
  if (score >= 70) return PRIORITY_COLORS.ai.primary;
  return PRIORITY_COLORS.high.primary;
};
