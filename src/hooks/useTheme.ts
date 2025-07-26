import { ref, computed, watch, onMounted } from 'vue';

type Theme = 'light' | 'dark';

export function useTheme() {
  const theme = ref<Theme>('light');

  const initializeTheme = () => {
    const savedTheme = localStorage.getItem('theme') as Theme;
    if (savedTheme) {
      theme.value = savedTheme;
    } else {
      theme.value = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }
  };

  watch(theme, (newTheme) => {
    document.documentElement.classList.remove('light', 'dark');
    document.documentElement.classList.add(newTheme);
    localStorage.setItem('theme', newTheme);
  }, { immediate: true });

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light';
  };

  const isDark = computed(() => theme.value === 'dark');

  onMounted(() => {
    initializeTheme();
  });

  return {
    theme,
    toggleTheme,
    isDark
  };
}