import { ref, computed } from 'vue';

type Theme = 'light' | 'dark';

const currentTheme = ref<Theme>('light');

export function useTheme() {
  const theme = computed(() => currentTheme.value);
  
  const isDark = computed(() => currentTheme.value === 'dark');
  
  const toggleTheme = () => {
    currentTheme.value = currentTheme.value === 'light' ? 'dark' : 'light';
    updateTheme();
    saveTheme();
  };
  
  const setTheme = (newTheme: Theme) => {
    currentTheme.value = newTheme;
    updateTheme();
    saveTheme();
  };
  
  const updateTheme = () => {
    const html = document.documentElement;
    html.setAttribute('data-theme', currentTheme.value);
    
    // Update class for Tailwind dark mode
    if (currentTheme.value === 'dark') {
      html.classList.add('dark');
    } else {
      html.classList.remove('dark');
    }
  };
  
  const saveTheme = () => {
    try {
      localStorage.setItem('lemonnpie-theme', currentTheme.value);
    } catch (error) {
      console.warn('Failed to save theme preference:', error);
    }
  };
  
  const loadTheme = () => {
    try {
      const saved = localStorage.getItem('lemonnpie-theme') as Theme;
      if (saved && ['light', 'dark'].includes(saved)) {
        currentTheme.value = saved;
      } else {
        // Check system preference
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        currentTheme.value = prefersDark ? 'dark' : 'light';
      }
    } catch (error) {
      console.warn('Failed to load theme preference:', error);
      currentTheme.value = 'light';
    }
  };
  
  const initTheme = () => {
    loadTheme();
    updateTheme();
    
    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      // Only update if user hasn't manually set a preference
      const hasManualPreference = localStorage.getItem('lemonnpie-theme');
      if (!hasManualPreference) {
        currentTheme.value = e.matches ? 'dark' : 'light';
        updateTheme();
      }
    };
    
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleChange);
    } else {
      // Fallback for older browsers
      mediaQuery.addListener(handleChange);
    }
  };
  
  return {
    theme,
    isDark,
    toggleTheme,
    setTheme,
    initTheme
  };
}

// Export theme colors for use in components
export const themeColors = {
  light: {
    primary: '#FFD700', // Nollywood Gold
    secondary: '#228B22', // Nigerian Green
    accent: '#FF6B35', // Vibrant Orange
    neutral: '#2C3E50', // Deep Navy
    base: '#FFFFFF',
    info: '#3ABFF8',
    success: '#36D399',
    warning: '#FBBD23',
    error: '#F87272'
  },
  dark: {
    primary: '#FFD700', // Nollywood Gold
    secondary: '#32CD32', // Lighter Nigerian Green
    accent: '#FF7F50', // Coral
    neutral: '#1F2937', // Dark Gray
    base: '#111827',
    info: '#3ABFF8',
    success: '#36D399',
    warning: '#FBBD23',
    error: '#F87272'
  }
};