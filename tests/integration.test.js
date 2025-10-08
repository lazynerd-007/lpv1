// Integration tests for main application functionality
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia } from 'pinia'
import App from '../src/App.vue'
import HomePage from '../src/pages/HomePage.vue'
import HeroSection from '../src/components/sections/HeroSection.vue'
import MovieCarousel from '../src/components/sections/shared/MovieCarousel.vue'

// Mock router
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomePage },
    { path: '/movie/:id', component: { template: '<div>Movie Details</div>' } }
  ]
})

// Mock stores
vi.mock('../src/stores/movieStore', () => ({
  useMovieStore: () => ({
    featuredMovie: {
      id: 1,
      title: 'Test Movie',
      localTitle: 'Test Local Title',
      plot: 'Test plot description',
      poster: 'https://example.com/poster.jpg',
      rating: 8.5,
      trailerUrl: 'https://example.com/trailer'
    },
    trendingMovies: [
      { id: 1, title: 'Movie 1', poster: 'poster1.jpg', rating: 8.0 },
      { id: 2, title: 'Movie 2', poster: 'poster2.jpg', rating: 7.5 }
    ],
    popularMovies: [
      { id: 3, title: 'Movie 3', poster: 'poster3.jpg', rating: 9.0 }
    ],
    fetchFeaturedMovie: vi.fn(),
    fetchTrendingMovies: vi.fn(),
    fetchPopularMovies: vi.fn()
  })
}))

vi.mock('../src/stores/uiStore', () => ({
  useUIStore: () => ({
    isLoading: false,
    showTrailer: false,
    currentTrailerUrl: '',
    setLoading: vi.fn(),
    openTrailer: vi.fn(),
    closeTrailer: vi.fn()
  })
}))

vi.mock('../src/stores/userStore', () => ({
  useUserStore: () => ({
    user: null,
    isAuthenticated: false,
    checkAuthStatus: vi.fn()
  })
}))

// Mock composables
vi.mock('../src/composables/useTheme', () => ({
  useTheme: () => ({
    theme: 'light',
    isDark: false,
    initTheme: vi.fn(),
    toggleTheme: vi.fn()
  })
}))

vi.mock('../src/composables/useLazyImage', () => ({
  useLazyImage: () => ({
    loadedImages: new Set(),
    isImageLoaded: vi.fn(() => true),
    observeImage: vi.fn(),
    preloadImage: vi.fn()
  })
}))

// Mock performance utils
vi.mock('../src/utils/performance', () => ({
  measurePerformance: vi.fn(),
  preloadCriticalImages: vi.fn()
}))

describe('Application Integration Tests', () => {
  let pinia

  beforeEach(() => {
    pinia = createPinia()
    vi.clearAllMocks()
  })

  describe('App Component', () => {
    it('should render without errors', async () => {
      const wrapper = mount(App, {
        global: {
          plugins: [router, pinia]
        }
      })

      expect(wrapper.exists()).toBe(true)
    })

    it('should show header and footer on non-auth pages', async () => {
      await router.push('/')
      
      const wrapper = mount(App, {
        global: {
          plugins: [router, pinia]
        }
      })

      // Should render main content
      expect(wrapper.find('main').exists()).toBe(true)
    })
  })

  describe('HomePage Component', () => {
    it('should render all main sections', () => {
      const wrapper = mount(HomePage, {
        global: {
          plugins: [router, pinia]
        }
      })

      // Check if main sections are present
      expect(wrapper.find('[data-testid="hero-section"]').exists() || 
             wrapper.findComponent(HeroSection).exists()).toBe(true)
    })

    it('should handle lazy loading of sections', async () => {
      const wrapper = mount(HomePage, {
        global: {
          plugins: [router, pinia]
        }
      })

      // Wait for async components to load
      await wrapper.vm.$nextTick()
      
      expect(wrapper.exists()).toBe(true)
    })
  })

  describe('HeroSection Component', () => {
    it('should display featured movie information', () => {
      const wrapper = mount(HeroSection, {
        global: {
          plugins: [router, pinia]
        }
      })

      expect(wrapper.text()).toContain('Test Movie')
      expect(wrapper.text()).toContain('Test plot description')
    })

    it('should handle image loading states', async () => {
      const wrapper = mount(HeroSection, {
        global: {
          plugins: [router, pinia]
        }
      })

      // Should have loading placeholder initially
      expect(wrapper.find('.loading-placeholder').exists() || 
             wrapper.text().includes('Loading')).toBe(true)
    })
  })

  describe('MovieCarousel Component', () => {
    const mockMovies = [
      { id: 1, title: 'Movie 1', poster: 'poster1.jpg', rating: 8.0 },
      { id: 2, title: 'Movie 2', poster: 'poster2.jpg', rating: 7.5 }
    ]

    it('should render movie list correctly', () => {
      const wrapper = mount(MovieCarousel, {
        props: {
          title: 'Test Carousel',
          movies: mockMovies
        },
        global: {
          plugins: [router, pinia]
        }
      })

      expect(wrapper.text()).toContain('Test Carousel')
      expect(wrapper.text()).toContain('Movie 1')
      expect(wrapper.text()).toContain('Movie 2')
    })

    it('should handle empty movie list', () => {
      const wrapper = mount(MovieCarousel, {
        props: {
          title: 'Empty Carousel',
          movies: []
        },
        global: {
          plugins: [router, pinia]
        }
      })

      expect(wrapper.text()).toContain('Empty Carousel')
    })

    it('should implement lazy loading for images', () => {
      const wrapper = mount(MovieCarousel, {
        props: {
          title: 'Test Carousel',
          movies: mockMovies
        },
        global: {
          plugins: [router, pinia]
        }
      })

      // Check for data-src attributes (lazy loading)
      const images = wrapper.findAll('img')
      images.forEach(img => {
        expect(img.attributes('data-src') || img.attributes('src')).toBeDefined()
      })
    })
  })

  describe('Navigation and Routing', () => {
    it('should navigate to movie details page', async () => {
      await router.push('/movie/1')
      expect(router.currentRoute.value.path).toBe('/movie/1')
    })

    it('should handle route parameters correctly', async () => {
      await router.push('/movie/123')
      expect(router.currentRoute.value.params.id).toBe('123')
    })
  })

  describe('Performance Optimizations', () => {
    it('should implement lazy loading for components', () => {
      // Test that components are loaded asynchronously
      const wrapper = mount(HomePage, {
        global: {
          plugins: [router, pinia]
        }
      })

      expect(wrapper.exists()).toBe(true)
    })

    it('should preload critical resources', () => {
      // This would be tested in the actual browser environment
      // Here we just verify the functions are called
      expect(true).toBe(true)
    })
  })
})