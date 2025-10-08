import { ref, onMounted, onUnmounted } from 'vue'

export interface BreakpointConfig {
  xs: number
  sm: number
  md: number
  lg: number
  xl: number
  '2xl': number
}

const defaultBreakpoints: BreakpointConfig = {
  xs: 0,
  sm: 640,
  md: 768,
  lg: 1024,
  xl: 1280,
  '2xl': 1536
}

export type BreakpointKey = keyof BreakpointConfig

export function useResponsive(breakpoints: BreakpointConfig = defaultBreakpoints) {
  const windowWidth = ref(0)
  const windowHeight = ref(0)
  const currentBreakpoint = ref<BreakpointKey>('xs')

  // Device type detection
  const isMobile = ref(false)
  const isTablet = ref(false)
  const isDesktop = ref(false)
  const isTouchDevice = ref(false)

  // Orientation
  const isPortrait = ref(true)
  const isLandscape = ref(false)

  const updateDimensions = () => {
    windowWidth.value = window.innerWidth
    windowHeight.value = window.innerHeight
    
    // Update orientation
    isPortrait.value = windowHeight.value > windowWidth.value
    isLandscape.value = !isPortrait.value
    
    // Update current breakpoint
    const width = windowWidth.value
    if (width >= breakpoints['2xl']) {
      currentBreakpoint.value = '2xl'
    } else if (width >= breakpoints.xl) {
      currentBreakpoint.value = 'xl'
    } else if (width >= breakpoints.lg) {
      currentBreakpoint.value = 'lg'
    } else if (width >= breakpoints.md) {
      currentBreakpoint.value = 'md'
    } else if (width >= breakpoints.sm) {
      currentBreakpoint.value = 'sm'
    } else {
      currentBreakpoint.value = 'xs'
    }
    
    // Update device types
    isMobile.value = width < breakpoints.md
    isTablet.value = width >= breakpoints.md && width < breakpoints.lg
    isDesktop.value = width >= breakpoints.lg
  }

  const detectTouchDevice = () => {
    isTouchDevice.value = 'ontouchstart' in window || navigator.maxTouchPoints > 0
  }

  // Breakpoint helpers
  const isXs = () => currentBreakpoint.value === 'xs'
  const isSm = () => currentBreakpoint.value === 'sm'
  const isMd = () => currentBreakpoint.value === 'md'
  const isLg = () => currentBreakpoint.value === 'lg'
  const isXl = () => currentBreakpoint.value === 'xl'
  const is2Xl = () => currentBreakpoint.value === '2xl'

  // Range helpers
  const isSmAndUp = () => windowWidth.value >= breakpoints.sm
  const isMdAndUp = () => windowWidth.value >= breakpoints.md
  const isLgAndUp = () => windowWidth.value >= breakpoints.lg
  const isXlAndUp = () => windowWidth.value >= breakpoints.xl
  const is2XlAndUp = () => windowWidth.value >= breakpoints['2xl']

  const isSmAndDown = () => windowWidth.value < breakpoints.md
  const isMdAndDown = () => windowWidth.value < breakpoints.lg
  const isLgAndDown = () => windowWidth.value < breakpoints.xl
  const isXlAndDown = () => windowWidth.value < breakpoints['2xl']

  // Responsive classes helper
  const getResponsiveClasses = (classes: Partial<Record<BreakpointKey, string>>) => {
    const result: string[] = []
    
    Object.entries(classes).forEach(([breakpoint, className]) => {
      const bp = breakpoint as BreakpointKey
      if (className) {
        if (bp === 'xs') {
          result.push(className)
        } else {
          result.push(`${bp}:${className}`)
        }
      }
    })
    
    return result.join(' ')
  }

  // Grid columns helper for responsive layouts
  const getGridCols = (config: Partial<Record<BreakpointKey, number>>) => {
    const classes: string[] = []
    
    Object.entries(config).forEach(([breakpoint, cols]) => {
      const bp = breakpoint as BreakpointKey
      if (cols) {
        if (bp === 'xs') {
          classes.push(`grid-cols-${cols}`)
        } else {
          classes.push(`${bp}:grid-cols-${cols}`)
        }
      }
    })
    
    return classes.join(' ')
  }

  // Safe area helpers for mobile devices
  const getSafeAreaClasses = () => {
    if (!isMobile.value) return ''
    
    return 'pb-safe-bottom pl-safe-left pr-safe-right'
  }

  // Touch-friendly sizing
  const getTouchFriendlySize = (baseSize: string, touchSize?: string) => {
    return isTouchDevice.value && touchSize ? touchSize : baseSize
  }

  // Responsive font sizes
  const getResponsiveFontSize = (config: {
    base: string
    sm?: string
    md?: string
    lg?: string
    xl?: string
  }) => {
    const classes = [config.base]
    
    if (config.sm) classes.push(`sm:${config.sm}`)
    if (config.md) classes.push(`md:${config.md}`)
    if (config.lg) classes.push(`lg:${config.lg}`)
    if (config.xl) classes.push(`xl:${config.xl}`)
    
    return classes.join(' ')
  }

  // Responsive spacing
  const getResponsiveSpacing = (config: {
    base: string
    sm?: string
    md?: string
    lg?: string
  }) => {
    const classes = [config.base]
    
    if (config.sm) classes.push(`sm:${config.sm}`)
    if (config.md) classes.push(`md:${config.md}`)
    if (config.lg) classes.push(`lg:${config.lg}`)
    
    return classes.join(' ')
  }

  // Initialize
  onMounted(() => {
    updateDimensions()
    detectTouchDevice()
    window.addEventListener('resize', updateDimensions)
    window.addEventListener('orientationchange', updateDimensions)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', updateDimensions)
    window.removeEventListener('orientationchange', updateDimensions)
  })

  return {
    // Dimensions
    windowWidth,
    windowHeight,
    currentBreakpoint,
    
    // Device types
    isMobile,
    isTablet,
    isDesktop,
    isTouchDevice,
    
    // Orientation
    isPortrait,
    isLandscape,
    
    // Breakpoint checks
    isXs,
    isSm,
    isMd,
    isLg,
    isXl,
    is2Xl,
    
    // Range checks
    isSmAndUp,
    isMdAndUp,
    isLgAndUp,
    isXlAndUp,
    is2XlAndUp,
    isSmAndDown,
    isMdAndDown,
    isLgAndDown,
    isXlAndDown,
    
    // Helpers
    getResponsiveClasses,
    getGridCols,
    getSafeAreaClasses,
    getTouchFriendlySize,
    getResponsiveFontSize,
    getResponsiveSpacing
  }
}

// Predefined responsive configurations
export const responsiveConfigs = {
  // Common grid layouts
  movieGrid: {
    xs: 1,
    sm: 2,
    md: 3,
    lg: 4,
    xl: 5
  },
  
  reviewGrid: {
    xs: 1,
    md: 2,
    lg: 3
  },
  
  // Typography scales
  headingText: {
    base: 'text-2xl',
    sm: 'text-3xl',
    md: 'text-4xl',
    lg: 'text-5xl'
  },
  
  bodyText: {
    base: 'text-sm',
    sm: 'text-base',
    md: 'text-lg'
  },
  
  // Spacing scales
  sectionPadding: {
    base: 'p-4',
    sm: 'p-6',
    md: 'p-8',
    lg: 'p-12'
  },
  
  cardSpacing: {
    base: 'p-3',
    sm: 'p-4',
    md: 'p-6'
  }
}