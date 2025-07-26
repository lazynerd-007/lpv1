import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

interface Modal {
  id: string
  isOpen: boolean
  title?: string
  content?: string
  type?: 'info' | 'warning' | 'error' | 'success'
}

interface Toast {
  id: string
  message: string
  type: 'info' | 'success' | 'warning' | 'error'
  duration?: number
  isVisible: boolean
}

interface LoadingState {
  isLoading: boolean
  message?: string
}

export const useUIStore = defineStore('ui', () => {
  // State
  const theme = ref<'light' | 'dark'>('light')
  const sidebarOpen = ref(false)
  const mobileMenuOpen = ref(false)
  const modals = ref<Modal[]>([])
  const toasts = ref<Toast[]>([])
  const globalLoading = ref<LoadingState>({ isLoading: false })
  const pageTitle = ref('LemonNPie')
  const breadcrumbs = ref<Array<{ label: string; path?: string }>>([])
  
  // View preferences
  const movieViewMode = ref<'grid' | 'list'>('grid')
  const itemsPerPage = ref(12)
  const showFilters = ref(false)
  
  // Search UI state
  const searchFocused = ref(false)
  const searchSuggestions = ref<string[]>([])
  
  // Player state
  const trailerModal = ref({
    isOpen: false,
    movieId: '',
    trailerUrl: ''
  })

  // Getters
  const activeModals = computed(() => modals.value.filter(modal => modal.isOpen))
  const visibleToasts = computed(() => toasts.value.filter(toast => toast.isVisible))
  const hasActiveModal = computed(() => activeModals.value.length > 0)
  const isAnyModalOpen = computed(() => hasActiveModal.value)
  
  const currentThemeClass = computed(() => {
    return theme.value === 'dark' ? 'dark' : 'light'
  })

  // Actions
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light'
    // Persist theme preference
    localStorage.setItem('lemonnpie-theme', theme.value)
  }

  const setTheme = (newTheme: 'light' | 'dark') => {
    theme.value = newTheme
    localStorage.setItem('lemonnpie-theme', newTheme)
  }

  const initializeTheme = () => {
    const savedTheme = localStorage.getItem('lemonnpie-theme') as 'light' | 'dark' | null
    if (savedTheme) {
      theme.value = savedTheme
    } else {
      // Check system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
      theme.value = prefersDark ? 'dark' : 'light'
    }
  }

  const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value
  }

  const closeSidebar = () => {
    sidebarOpen.value = false
  }

  const toggleMobileMenu = () => {
    mobileMenuOpen.value = !mobileMenuOpen.value
  }

  const closeMobileMenu = () => {
    mobileMenuOpen.value = false
  }

  // Modal management
  const openModal = (modal: Omit<Modal, 'isOpen'>) => {
    const existingModal = modals.value.find(m => m.id === modal.id)
    if (existingModal) {
      existingModal.isOpen = true
      Object.assign(existingModal, modal)
    } else {
      modals.value.push({ ...modal, isOpen: true })
    }
  }

  const closeModal = (modalId: string) => {
    const modal = modals.value.find(m => m.id === modalId)
    if (modal) {
      modal.isOpen = false
    }
  }

  const closeAllModals = () => {
    modals.value.forEach(modal => {
      modal.isOpen = false
    })
  }

  // Toast management
  const showToast = (toast: Omit<Toast, 'id' | 'isVisible'>) => {
    const id = Date.now().toString()
    const newToast: Toast = {
      ...toast,
      id,
      isVisible: true,
      duration: toast.duration || 5000
    }
    
    toasts.value.push(newToast)
    
    // Auto-hide toast
    setTimeout(() => {
      hideToast(id)
    }, newToast.duration)
  }

  const hideToast = (toastId: string) => {
    const toast = toasts.value.find(t => t.id === toastId)
    if (toast) {
      toast.isVisible = false
      // Remove from array after animation
      setTimeout(() => {
        const index = toasts.value.findIndex(t => t.id === toastId)
        if (index > -1) {
          toasts.value.splice(index, 1)
        }
      }, 300)
    }
  }

  const clearAllToasts = () => {
    toasts.value.forEach(toast => {
      toast.isVisible = false
    })
    setTimeout(() => {
      toasts.value = []
    }, 300)
  }

  // Loading state
  const setGlobalLoading = (isLoading: boolean, message?: string) => {
    globalLoading.value = { isLoading, message }
  }

  const startLoading = (message?: string) => {
    setGlobalLoading(true, message)
  }

  const stopLoading = () => {
    setGlobalLoading(false)
  }

  // Page management
  const setPageTitle = (title: string) => {
    pageTitle.value = title
    document.title = `${title} | LemonNPie`
  }

  const setBreadcrumbs = (crumbs: Array<{ label: string; path?: string }>) => {
    breadcrumbs.value = crumbs
  }

  // View preferences
  const setMovieViewMode = (mode: 'grid' | 'list') => {
    movieViewMode.value = mode
    localStorage.setItem('lemonnpie-view-mode', mode)
  }

  const setItemsPerPage = (count: number) => {
    itemsPerPage.value = count
    localStorage.setItem('lemonnpie-items-per-page', count.toString())
  }

  const toggleFilters = () => {
    showFilters.value = !showFilters.value
  }

  // Search UI
  const setSearchFocus = (focused: boolean) => {
    searchFocused.value = focused
  }

  const setSearchSuggestions = (suggestions: string[]) => {
    searchSuggestions.value = suggestions
  }

  const clearSearchSuggestions = () => {
    searchSuggestions.value = []
  }

  // Trailer modal
  const openTrailerModal = (movieId: string, trailerUrl: string) => {
    trailerModal.value = {
      isOpen: true,
      movieId,
      trailerUrl
    }
  }

  const closeTrailerModal = () => {
    trailerModal.value = {
      isOpen: false,
      movieId: '',
      trailerUrl: ''
    }
  }

  // Utility functions
  const showSuccessToast = (message: string) => {
    showToast({ message, type: 'success' })
  }

  const showErrorToast = (message: string) => {
    showToast({ message, type: 'error' })
  }

  const showInfoToast = (message: string) => {
    showToast({ message, type: 'info' })
  }

  const showWarningToast = (message: string) => {
    showToast({ message, type: 'warning' })
  }

  // Initialize preferences
  const initializePreferences = () => {
    // Initialize theme
    initializeTheme()
    
    // Initialize view mode
    const savedViewMode = localStorage.getItem('lemonnpie-view-mode') as 'grid' | 'list' | null
    if (savedViewMode) {
      movieViewMode.value = savedViewMode
    }
    
    // Initialize items per page
    const savedItemsPerPage = localStorage.getItem('lemonnpie-items-per-page')
    if (savedItemsPerPage) {
      itemsPerPage.value = parseInt(savedItemsPerPage, 10)
    }
  }

  return {
    // State
    theme,
    sidebarOpen,
    mobileMenuOpen,
    modals,
    toasts,
    globalLoading,
    pageTitle,
    breadcrumbs,
    movieViewMode,
    itemsPerPage,
    showFilters,
    searchFocused,
    searchSuggestions,
    trailerModal,
    
    // Getters
    activeModals,
    visibleToasts,
    hasActiveModal,
    isAnyModalOpen,
    currentThemeClass,
    
    // Actions
    toggleTheme,
    setTheme,
    initializeTheme,
    toggleSidebar,
    closeSidebar,
    toggleMobileMenu,
    closeMobileMenu,
    openModal,
    closeModal,
    closeAllModals,
    showToast,
    hideToast,
    clearAllToasts,
    setGlobalLoading,
    startLoading,
    stopLoading,
    setPageTitle,
    setBreadcrumbs,
    setMovieViewMode,
    setItemsPerPage,
    toggleFilters,
    setSearchFocus,
    setSearchSuggestions,
    clearSearchSuggestions,
    openTrailerModal,
    closeTrailerModal,
    showSuccessToast,
    showErrorToast,
    showInfoToast,
    showWarningToast,
    initializePreferences
  }
})