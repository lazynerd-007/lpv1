import { ref, onMounted, onUnmounted } from 'vue'

export interface LazyLoadOptions {
  rootMargin?: string
  threshold?: number | number[]
  fallbackSrc?: string
  loadingClass?: string
  errorClass?: string
  loadedClass?: string
}

const defaultOptions: LazyLoadOptions = {
  rootMargin: '50px',
  threshold: 0.1,
  fallbackSrc: '/placeholder-image.jpg',
  loadingClass: 'lazy-loading',
  errorClass: 'lazy-error',
  loadedClass: 'lazy-loaded'
}

export function useLazyLoading(options: LazyLoadOptions = {}) {
  const config = { ...defaultOptions, ...options }
  const observer = ref<IntersectionObserver | null>(null)
  const loadedImages = new Set<string>()
  const failedImages = new Set<string>()

  // Create intersection observer
  const createObserver = () => {
    if (!('IntersectionObserver' in window)) {
      // Fallback for browsers without IntersectionObserver support
      return null
    }

    return new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const img = entry.target as HTMLImageElement
            loadImage(img)
            observer.value?.unobserve(img)
          }
        })
      },
      {
        rootMargin: config.rootMargin,
        threshold: config.threshold
      }
    )
  }

  // Load image with error handling
  const loadImage = (img: HTMLImageElement) => {
    const src = img.dataset.src
    if (!src) return

    // Add loading class
    if (config.loadingClass) {
      img.classList.add(config.loadingClass)
    }

    // Create new image to preload
    const imageLoader = new Image()
    
    imageLoader.onload = () => {
      img.src = src
      loadedImages.add(src)
      
      // Remove loading class and add loaded class
      if (config.loadingClass) {
        img.classList.remove(config.loadingClass)
      }
      if (config.loadedClass) {
        img.classList.add(config.loadedClass)
      }
      
      // Trigger custom event
      img.dispatchEvent(new CustomEvent('lazyloaded', { detail: { src } }))
    }
    
    imageLoader.onerror = () => {
      failedImages.add(src)
      
      // Set fallback image
      if (config.fallbackSrc) {
        img.src = config.fallbackSrc
      }
      
      // Remove loading class and add error class
      if (config.loadingClass) {
        img.classList.remove(config.loadingClass)
      }
      if (config.errorClass) {
        img.classList.add(config.errorClass)
      }
      
      // Trigger custom event
      img.dispatchEvent(new CustomEvent('lazyerror', { detail: { src, error: 'Failed to load image' } }))
    }
    
    imageLoader.src = src
  }

  // Observe an image element
  const observe = (img: HTMLImageElement) => {
    if (!observer.value) {
      // Fallback: load immediately if no observer
      loadImage(img)
      return
    }
    
    observer.value.observe(img)
  }

  // Unobserve an image element
  const unobserve = (img: HTMLImageElement) => {
    if (observer.value) {
      observer.value.unobserve(img)
    }
  }

  // Initialize observer
  onMounted(() => {
    observer.value = createObserver()
  })

  // Cleanup
  onUnmounted(() => {
    if (observer.value) {
      observer.value.disconnect()
    }
  })

  return {
    observe,
    unobserve,
    loadedImages,
    failedImages,
    isLoaded: (src: string) => loadedImages.has(src),
    hasFailed: (src: string) => failedImages.has(src)
  }
}

// Vue directive for lazy loading
export const vLazyLoad = {
  mounted(el: HTMLImageElement, binding: any) {
    const options = binding.value || {}
    const { observe } = useLazyLoading(options)
    
    // Store original src in data attribute
    if (el.src && !el.dataset.src) {
      el.dataset.src = el.src
      el.src = '' // Clear src to prevent immediate loading
    }
    
    observe(el)
  },
  
  unmounted(el: HTMLImageElement) {
    const { unobserve } = useLazyLoading()
    unobserve(el)
  }
}

// Utility function for progressive image loading
export function useProgressiveImage(lowQualitySrc: string, highQualitySrc: string) {
  const currentSrc = ref(lowQualitySrc)
  const isLoading = ref(true)
  const hasError = ref(false)

  const loadHighQuality = () => {
    const img = new Image()
    
    img.onload = () => {
      currentSrc.value = highQualitySrc
      isLoading.value = false
    }
    
    img.onerror = () => {
      hasError.value = true
      isLoading.value = false
    }
    
    img.src = highQualitySrc
  }

  return {
    currentSrc,
    isLoading,
    hasError,
    loadHighQuality
  }
}

// Utility for responsive images
export function useResponsiveImage(srcSet: Record<string, string>, defaultSrc: string) {
  const currentSrc = ref(defaultSrc)
  
  const updateSrc = (breakpoint: string) => {
    currentSrc.value = srcSet[breakpoint] || defaultSrc
  }

  return {
    currentSrc,
    updateSrc,
    srcSet
  }
}

// Image optimization utilities
export const imageUtils = {
  // Generate srcset for responsive images
  generateSrcSet: (baseSrc: string, sizes: number[]) => {
    return sizes
      .map(size => `${baseSrc}?w=${size} ${size}w`)
      .join(', ')
  },
  
  // Generate sizes attribute
  generateSizes: (breakpoints: Array<{ condition: string; size: string }>) => {
    return breakpoints
      .map(bp => `${bp.condition} ${bp.size}`)
      .join(', ')
  },
  
  // Optimize image URL with parameters
  optimizeUrl: (src: string, options: {
    width?: number
    height?: number
    quality?: number
    format?: 'webp' | 'jpg' | 'png' | 'avif'
  } = {}) => {
    const url = new URL(src, window.location.origin)
    
    if (options.width) url.searchParams.set('w', options.width.toString())
    if (options.height) url.searchParams.set('h', options.height.toString())
    if (options.quality) url.searchParams.set('q', options.quality.toString())
    if (options.format) url.searchParams.set('f', options.format)
    
    return url.toString()
  },
  
  // Check if image format is supported
  supportsFormat: (format: string): Promise<boolean> => {
    return new Promise((resolve) => {
      const img = new Image()
      img.onload = () => resolve(true)
      img.onerror = () => resolve(false)
      
      // Test images for different formats
      const testImages: Record<string, string> = {
        webp: 'data:image/webp;base64,UklGRiIAAABXRUJQVlA4IBYAAAAwAQCdASoBAAEADsD+JaQAA3AAAAAA',
        avif: 'data:image/avif;base64,AAAAIGZ0eXBhdmlmAAAAAGF2aWZtaWYxbWlhZk1BMUIAAADybWV0YQAAAAAAAAAoaGRscgAAAAAAAAAAcGljdAAAAAAAAAAAAAAAAGxpYmF2aWYAAAAADnBpdG0AAAAAAAEAAAAeaWxvYwAAAABEAAABAAEAAAABAAABGgAAAB0AAAAoaWluZgAAAAAAAQAAABppbmZlAgAAAAABAABhdjAxQ29sb3IAAAAAamlwcnAAAABLaXBjbwAAABRpc3BlAAAAAAAAAAIAAAACAAAAEHBpeGkAAAAAAwgICAAAAAxhdjFDgQ0MAAAAABNjb2xybmNseAACAAIAAYAAAAAXaXBtYQAAAAAAAAABAAEEAQKDBAAAACVtZGF0EgAKCBgABogQEAwgMg8f8D///8WfhwB8+ErK42A='
      }
      
      img.src = testImages[format] || ''
    })
  }
}