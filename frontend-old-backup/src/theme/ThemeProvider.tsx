import React, { createContext, useContext, useMemo } from 'react';
import type { Theme } from './index';
import { theme as defaultTheme } from './index';

interface ThemeProviderProps {
  theme?: Theme;
  children: React.ReactNode;
}

const ThemeContext = createContext<Theme>(defaultTheme);

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ theme = defaultTheme, children }) => {
  const value = useMemo(() => theme, [theme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};

export const useTheme = (): Theme => useContext(ThemeContext);

export { ThemeContext };
