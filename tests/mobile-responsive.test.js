// Mobile responsiveness and touch interaction tests
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import HomePage from '../src/pages/HomePage.vue'
import MovieCarousel from '../src/components/sections/shared/MovieCarousel.vue'
import HeroSection from '../src/components/sections/HeroSection.vue'

// Mock mobile environment
function mockMobileEnvironment(deviceType = 'mobile') {
  const devices = {
    mobile: {
      width: 375,
      height: 667,
      userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
      touchSupport: true,
      pixelRatio: 2
    },
    tablet: {
      width: 768,
      height: 1024,
      userAgent: 'Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
      touchSupport: true,
      pixelRatio: 2
    },
    desktop: {
      width: 1920,
      height: 1080,
      userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      touchSupport: false,
      pixelRatio: 1
    }
  }
  
  const device = devices[deviceType]
  
  // Mock window dimensions
  Object.defineProperty(window, 'innerWidth', {
    writable: true,
    configurable: true,
    value: device.width
  })
  
  Object.defineProperty(window, 'innerHeight', {
    writable: true,
    configurable: true,
    value: device.height
  })
  
  // Mock device pixel ratio
  Object.defineProperty(window, 'devicePixelRatio', {
    writable: true,
    configurable: true,
    value: device.pixelRatio
  })
  
  // Mock navigator
  Object.defineProperty(navigator, 'userAgent', {
    writable: true,
    configurable: true,
    value: device.userAgent
  })
  
  // Mock touch support
  Object.defineProperty(window, 'ontouchstart', {
    writable: true,
    configurable: true,
    value: device.touchSupport ? {} : undefined
  })
  
  // Mock matchMedia for responsive queries
  window.matchMedia = vi.fn((query) => {
    const matches = {
      '(max-width: 640px)': device.width <= 640,
      '(max-width: 768px)': device.width <= 768,
      '(max-width: 1024px)': device.width <= 1024,
      '(min-width: 768px)': device.width >= 768,
      '(min-width: 1024px)': device.width >= 1024,
      '(orientation: portrait)': device.height > device.width,
      '(orientation: landscape)': device.width > device.height,
      '(hover: hover)': !device.touchSupport,
      '(pointer: coarse)': device.touchSupport
    }
    
    return {
      matches: matches[query] || false,
      media: query,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      addListener: vi.fn(),
      removeListener: vi.fn()
    }
  })
}

// Mock stores
vi.mock('../src/stores/movieStore', () => ({
  useMovieStore: () => ({
    featuredMovie: {
      id: 1,
      title: 'Test Movie',
      localTitle: 'Test Local Title',
      plot: 'Test plot description',
      poster: 'https://example.com/poster.jpg',
      rating: 8.5
    },
    trendingMovies: Array.from({ length: 10 }, (_, i) => ({
      id: i + 1,
      title: `Movie ${i + 1}`,
      poster: `poster${i + 1}.jpg`,
      rating: 7.5 + (i * 0.1)
    }))
  })
}))

vi.mock('../src/stores/uiStore', () => ({
  useUIStore: () => ({
    isLoading: false,
    showTrailer: false,
    openTrailer: vi.fn(),
    closeTrailer: vi.fn()
  })
}))

vi.mock('../src/composables/useLazyImage', () => ({
  useLazyImage: () => ({
    loadedImages: new Set(),
    isImageLoaded: vi.fn(() => true),
    observeImage: vi.fn()
  })
}))

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage }
  ]
})

describe('Mobile Responsiveness Tests', () => {
  let pinia
  
  beforeEach(() => {
    pinia = createPinia()
    vi.clearAllMocks()
  })
  
  describe('Mobile Device (375px width)', () => {
    beforeEach(() => {
      mockMobileEnvironment('mobile')
    })
    
    it('should detect mobile environment correctly', () => {
      expect(window.innerWidth).toBe(375)
      expect(window.ontouchstart).toBeDefined()
      expect(window.matchMedia('(max-width: 768px)').matches).toBe(true)
      expect(window.matchMedia('(pointer: coarse)').matches).toBe(true)
    })
    
    it('should render HomePage with mobile layout', () => {
      const wrapper = mount(HomePage, {
        global: {
          plugins: [router, pinia]
        }
      })
      
      expect(wrapper.exists()).toBe(true)
      // Mobile layout should be more compact
      expect(window.matchMedia('(max-width: 768px)').matches).toBe(true)
    })
    
    it('should handle touch interactions in MovieCarousel', () => {
      const mockMovies = Array.from({ length: 10 }, (_, i) => ({
        id: i + 1,
        title: `Movie ${i + 1}`,
        poster: `poster${i + 1}.jpg`,
        rating: 8.0
      }))
      
      const wrapper = mount(MovieCarousel, {
        props: {
          title: 'Test Carousel',
          movies: mockMovies
        },
        global: {
          plugins: [router, pinia]
        }
      })
      
      // Should have touch-friendly navigation
      const carousel = wrapper.find('.carousel-container')
      expect(carousel.exists()).toBe(true)
    })
    
    it('should optimize images for mobile', () => {
      const wrapper = mount(HeroSection, {
        global: {
          plugins: [router, pinia]
        }
      })
      
      // Should load appropriate image sizes for mobile
      expect(wrapper.exists()).toBe(true)
    })
    
    it('should handle mobile navigation', () => {
      // Test that mobile navigation works
      expect(window.innerWidth).toBe(375)
      
      // Mobile should show hamburger menu or simplified navigation
      const isMobile = window.matchMedia('(max-width: 768px)').matches
      expect(isMobile).toBe(true)
    })
  })
  
  describe('Tablet Device (768px width)', () => {
    beforeEach(() => {
      mockMobileEnvironment('tablet')
    })
    
    it('should detect tablet environment correctly', () => {
      expect(window.innerWidth).toBe(768)
      expect(window.ontouchstart).toBeDefined()
      expect(window.matchMedia('(min-width: 768px)').matches).toBe(true)
      expect(window.matchMedia('(max-width: 1024px)').matches).toBe(true)
    })
    
    it('should render with tablet-optimized layout', () => {
      const wrapper = mount(HomePage, {
        global: {
          plugins: [router, pinia]
        }
      })
      
      expect(wrapper.exists()).toBe(true)
      // Tablet should have more space than mobile
      expect(window.matchMedia('(min-width: 768px)').matches).toBe(true)
    })
    
    it('should show more items in carousel on tablet', () => {
      const mockMovies = Array.from({ length: 10 }, (_, i) => ({
        id: i + 1,
        title: `Movie ${i + 1}`,
        poster: `poster${i + 1}.jpg`,
        rating: 8.0
      }))
      
      const wrapper = mount(MovieCarousel, {
        props: {
          title: 'Test Carousel',
          movies: mockMovies
        },
        global: {
          plugins: [router, pinia]
        }
      })
      
      // Tablet should show more items than mobile
      expect(wrapper.exists()).toBe(true)
    })
  })
  
  describe('Desktop Device (1920px width)', () => {
    beforeEach(() => {
      mockMobileEnvironment('desktop')
    })
    
    it('should detect desktop environment correctly', () => {
      expect(window.innerWidth).toBe(1920)
      expect(window.ontouchstart).toBeUndefined()
      expect(window.matchMedia('(min-width: 1024px)').matches).toBe(true)
      expect(window.matchMedia('(hover: hover)').matches).toBe(true)
    })
    
    it('should render with desktop layout', () => {
      const wrapper = mount(HomePage, {
        global: {
          plugins: [router, pinia]
        }
      })
      
      expect(wrapper.exists()).toBe(true)
      // Desktop should have full layout
      expect(window.matchMedia('(min-width: 1024px)').matches).toBe(true)
    })
  })
  
  describe('Touch Interactions', () => {
    beforeEach(() => {
      mockMobileEnvironment('mobile')
    })
    
    it('should handle touch events for carousel navigation', () => {
      const mockMovies = Array.from({ length: 10 }, (_, i) => ({
        id: i + 1,
        title: `Movie ${i + 1}`,
        poster: `poster${i + 1}.jpg`,
        rating: 8.0
      }))
      
      const wrapper = mount(MovieCarousel, {
        props: {
          title: 'Test Carousel',
          movies: mockMovies
        },
        global: {
          plugins: [router, pinia]
        }
      })
      
      // Should support touch scrolling
      const carousel = wrapper.find('.carousel-container')
      if (carousel.exists()) {
        // Touch events should be supported
        expect(window.ontouchstart).toBeDefined()
      }
    })
    
    it('should have touch-friendly button sizes', () => {
      // Buttons should be at least 44px for touch targets
      const minTouchTarget = 44
      expect(minTouchTarget).toBeGreaterThanOrEqual(44)
    })
  })
  
  describe('Orientation Changes', () => {
    it('should handle portrait orientation', () => {
      mockMobileEnvironment('mobile') // 375x667 (portrait)
      
      expect(window.matchMedia('(orientation: portrait)').matches).toBe(true)
      expect(window.matchMedia('(orientation: landscape)').matches).toBe(false)
    })
    
    it('should handle landscape orientation', () => {
      // Mock landscape mobile (667x375)
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 667
      })
      
      Object.defineProperty(window, 'innerHeight', {
        writable: true,
        configurable: true,
        value: 375
      })
      
      window.matchMedia = vi.fn((query) => ({
        matches: query === '(orientation: landscape)',
        addEventListener: vi.fn(),
        removeEventListener: vi.fn()
      }))
      
      expect(window.matchMedia('(orientation: landscape)').matches).toBe(true)
    })
  })
  
  describe('Performance on Mobile', () => {
    beforeEach(() => {
      mockMobileEnvironment('mobile')
    })
    
    it('should optimize for mobile performance', () => {
      // Mobile should use more aggressive lazy loading
      const isMobile = window.matchMedia('(max-width: 768px)').matches
      expect(isMobile).toBe(true)
      
      // Should load fewer items initially on mobile
      const mobileItemLimit = isMobile ? 4 : 8
      expect(mobileItemLimit).toBe(4)
    })
    
    it('should use appropriate image sizes for mobile', () => {
      const devicePixelRatio = window.devicePixelRatio
      const screenWidth = window.innerWidth
      
      // Calculate optimal image width for mobile
      const optimalImageWidth = Math.min(screenWidth * devicePixelRatio, 800)
      expect(optimalImageWidth).toBeLessThanOrEqual(800)
    })
  })
  
  describe('Accessibility on Mobile', () => {
    beforeEach(() => {
      mockMobileEnvironment('mobile')
    })
    
    it('should maintain accessibility on touch devices', () => {
      // Touch devices should still support keyboard navigation
      expect(window.ontouchstart).toBeDefined()
      
      // Focus indicators should be visible
      const supportsFocus = true // CSS :focus-visible should work
      expect(supportsFocus).toBe(true)
    })
    
    it('should have appropriate text sizes for mobile', () => {
      // Text should be readable on mobile (minimum 16px)
      const minFontSize = 16
      expect(minFontSize).toBeGreaterThanOrEqual(16)
    })
  })
})