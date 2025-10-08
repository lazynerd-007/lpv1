// Performance optimization utilities

/**
 * Preload critical images for better LCP
 */
export function preloadCriticalImages(imageUrls: string[]) {
  imageUrls.forEach(url => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.as = 'image'
    link.href = url
    document.head.appendChild(link)
  })
}

/**
 * Preload critical fonts
 */
export function preloadFonts(fontUrls: string[]) {
  fontUrls.forEach(url => {
    const link = document.createElement('link')
    link.rel = 'preload'
    link.as = 'font'
    link.type = 'font/woff2'
    link.crossOrigin = 'anonymous'
    link.href = url
    document.head.appendChild(link)
  })
}

/**
 * Optimize images with modern formats and lazy loading
 */
export function createOptimizedImage(src: string, alt: string, options: {
  width?: number
  height?: number
  loading?: 'lazy' | 'eager'
  decoding?: 'async' | 'sync' | 'auto'
  className?: string
} = {}) {
  const img = document.createElement('img')
  img.src = src
  img.alt = alt
  img.loading = options.loading || 'lazy'
  img.decoding = options.decoding || 'async'
  
  if (options.width) img.width = options.width
  if (options.height) img.height = options.height
  if (options.className) img.className = options.className
  
  return img
}

/**
 * Defer non-critical JavaScript
 */
export function deferScript(src: string, callback?: () => void) {
  const script = document.createElement('script')
  script.src = src
  script.defer = true
  
  if (callback) {
    script.onload = callback
  }
  
  document.head.appendChild(script)
}

/**
 * Measure and report performance metrics
 */
export function measurePerformance() {
  if ('performance' in window) {
    window.addEventListener('load', () => {
      setTimeout(() => {
        const perfData = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming
        
        const metrics = {
          FCP: 0,
          LCP: 0,
          FID: 0,
          CLS: 0,
          TTFB: perfData.responseStart - perfData.requestStart
        }
        
        // Get FCP
        const fcpEntry = performance.getEntriesByName('first-contentful-paint')[0]
        if (fcpEntry) {
          metrics.FCP = fcpEntry.startTime
        }
        
        // Get LCP
        if ('PerformanceObserver' in window) {
          const observer = new PerformanceObserver((list) => {
            const entries = list.getEntries()
            const lastEntry = entries[entries.length - 1]
            metrics.LCP = lastEntry.startTime
          })
          observer.observe({ entryTypes: ['largest-contentful-paint'] })
        }
        
        console.log('Performance Metrics:', metrics)
      }, 0)
    })
  }
}

/**
 * Optimize CSS delivery
 */
export function loadCSSAsync(href: string) {
  const link = document.createElement('link')
  link.rel = 'preload'
  link.as = 'style'
  link.href = href
  link.onload = function(this: HTMLLinkElement) {
    this.onload = null
    this.rel = 'stylesheet'
  }
  document.head.appendChild(link)
}