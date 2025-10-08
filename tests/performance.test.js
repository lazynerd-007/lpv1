// Performance testing suite
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { 
  preloadCriticalImages, 
  preloadFonts, 
  createOptimizedImage, 
  deferScript,
  loadCSSAsync 
} from '../src/utils/performance'

// Mock DOM methods
Object.defineProperty(global, 'document', {
  value: {
    createElement: vi.fn(() => ({
      rel: '',
      as: '',
      href: '',
      type: '',
      crossOrigin: '',
      src: '',
      alt: '',
      loading: '',
      decoding: '',
      width: 0,
      height: 0,
      className: '',
      defer: false,
      onload: null
    })),
    head: {
      appendChild: vi.fn()
    }
  },
  writable: true
})

describe('Performance Utilities', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('preloadCriticalImages', () => {
    it('should create preload links for each image URL', () => {
      const imageUrls = [
        'https://example.com/image1.jpg',
        'https://example.com/image2.jpg'
      ]
      
      preloadCriticalImages(imageUrls)
      
      expect(document.createElement).toHaveBeenCalledTimes(2)
      expect(document.head.appendChild).toHaveBeenCalledTimes(2)
    })

    it('should set correct attributes for preload links', () => {
      const mockLink = {
        rel: '',
        as: '',
        href: ''
      }
      document.createElement.mockReturnValue(mockLink)
      
      preloadCriticalImages(['https://example.com/image.jpg'])
      
      expect(mockLink.rel).toBe('preload')
      expect(mockLink.as).toBe('image')
      expect(mockLink.href).toBe('https://example.com/image.jpg')
    })
  })

  describe('preloadFonts', () => {
    it('should create preload links for fonts with correct attributes', () => {
      const mockLink = {
        rel: '',
        as: '',
        type: '',
        crossOrigin: '',
        href: ''
      }
      document.createElement.mockReturnValue(mockLink)
      
      preloadFonts(['https://fonts.googleapis.com/font.woff2'])
      
      expect(mockLink.rel).toBe('preload')
      expect(mockLink.as).toBe('font')
      expect(mockLink.type).toBe('font/woff2')
      expect(mockLink.crossOrigin).toBe('anonymous')
    })
  })

  describe('createOptimizedImage', () => {
    it('should create image element with default attributes', () => {
      const mockImg = {
        src: '',
        alt: '',
        loading: '',
        decoding: ''
      }
      document.createElement.mockReturnValue(mockImg)
      
      const img = createOptimizedImage('test.jpg', 'Test image')
      
      expect(mockImg.src).toBe('test.jpg')
      expect(mockImg.alt).toBe('Test image')
      expect(mockImg.loading).toBe('lazy')
      expect(mockImg.decoding).toBe('async')
    })

    it('should apply custom options', () => {
      const mockImg = {
        src: '',
        alt: '',
        loading: '',
        decoding: '',
        width: 0,
        height: 0,
        className: ''
      }
      document.createElement.mockReturnValue(mockImg)
      
      createOptimizedImage('test.jpg', 'Test', {
        width: 300,
        height: 200,
        loading: 'eager',
        className: 'hero-image'
      })
      
      expect(mockImg.width).toBe(300)
      expect(mockImg.height).toBe(200)
      expect(mockImg.loading).toBe('eager')
      expect(mockImg.className).toBe('hero-image')
    })
  })

  describe('deferScript', () => {
    it('should create script element with defer attribute', () => {
      const mockScript = {
        src: '',
        defer: false,
        onload: null
      }
      document.createElement.mockReturnValue(mockScript)
      
      deferScript('script.js')
      
      expect(mockScript.src).toBe('script.js')
      expect(mockScript.defer).toBe(true)
    })

    it('should set onload callback when provided', () => {
      const mockScript = {
        src: '',
        defer: false,
        onload: null
      }
      document.createElement.mockReturnValue(mockScript)
      const callback = vi.fn()
      
      deferScript('script.js', callback)
      
      expect(mockScript.onload).toBe(callback)
    })
  })

  describe('loadCSSAsync', () => {
    it('should create preload link that converts to stylesheet', () => {
      const mockLink = {
        rel: '',
        as: '',
        href: '',
        onload: null
      }
      document.createElement.mockReturnValue(mockLink)
      
      loadCSSAsync('styles.css')
      
      expect(mockLink.rel).toBe('preload')
      expect(mockLink.as).toBe('style')
      expect(mockLink.href).toBe('styles.css')
      expect(typeof mockLink.onload).toBe('function')
    })
  })
})