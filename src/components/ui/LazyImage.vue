<template>
  <div 
    :class="[
      'lazy-image-container',
      {
        'loading': isLoading,
        'error': hasError,
        'loaded': isLoaded
      }
    ]"
    :style="containerStyle"
  >
    <!-- Loading placeholder -->
    <div 
      v-if="isLoading && showPlaceholder"
      class="lazy-placeholder"
      :style="placeholderStyle"
      :aria-label="t('imageLoading')"
    >
      <div class="lazy-spinner" />
      <span v-if="loadingText" class="lazy-loading-text">{{ loadingText }}</span>
    </div>

    <!-- Main image -->
    <img
      ref="imageRef"
      :src="currentSrc"
      :alt="alt"
      :class="[
        'lazy-image',
        imageClass,
        {
          'fade-in': fadeIn && isLoaded,
          'blur-up': blurUp && isLoading
        }
      ]"
      :style="imageStyle"
      :loading="nativeLoading ? 'lazy' : 'eager'"
      :decoding="decoding"
      :sizes="sizes"
      :srcset="srcset"
      @load="handleLoad"
      @error="handleError"
      @click="handleClick"
    />

    <!-- Error state -->
    <div 
      v-if="hasError && showErrorState"
      class="lazy-error-state"
      :aria-label="t('imageError')"
    >
      <svg class="lazy-error-icon" viewBox="0 0 24 24" fill="currentColor">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
      </svg>
      <span v-if="errorText" class="lazy-error-text">{{ errorText }}</span>
    </div>

    <!-- Progressive enhancement overlay -->
    <div 
      v-if="progressive && lowQualitySrc && isLoading"
      class="lazy-progressive-overlay"
      :style="{ backgroundImage: `url(${lowQualitySrc})` }"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useLazyLoading, useProgressiveImage, imageUtils } from '@/composables/useLazyLoading'
import { useLanguage } from '@/composables/useLanguage'
import { useResponsive } from '@/composables/useResponsive'

interface Props {
  src: string
  alt: string
  lowQualitySrc?: string
  fallbackSrc?: string
  width?: number | string
  height?: number | string
  aspectRatio?: string
  sizes?: string
  srcset?: string
  quality?: number
  format?: 'webp' | 'jpg' | 'png' | 'avif'
  loading?: 'lazy' | 'eager'
  decoding?: 'async' | 'sync' | 'auto'
  fadeIn?: boolean
  blurUp?: boolean
  progressive?: boolean
  showPlaceholder?: boolean
  showErrorState?: boolean
  loadingText?: string
  errorText?: string
  imageClass?: string
  nativeLoading?: boolean
  rootMargin?: string
  threshold?: number
  optimize?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: 'lazy',
  decoding: 'async',
  fadeIn: true,
  blurUp: false,
  progressive: false,
  showPlaceholder: true,
  showErrorState: true,
  nativeLoading: false,
  rootMargin: '50px',
  threshold: 0.1,
  quality: 80,
  format: 'webp',
  optimize: true
})

const emit = defineEmits<{
  load: [event: Event]
  error: [event: Event]
  click: [event: MouseEvent]
}>()

const { t } = useLanguage()
const { isMobile } = useResponsive()

const imageRef = ref<HTMLImageElement>()
const isLoading = ref(true)
const hasError = ref(false)
const isLoaded = ref(false)

// Initialize lazy loading
const { observe, unobserve } = useLazyLoading({
  rootMargin: props.rootMargin,
  threshold: props.threshold,
  fallbackSrc: props.fallbackSrc
})

// Progressive image loading
const { currentSrc: progressiveSrc, loadHighQuality } = props.progressive && props.lowQualitySrc
  ? useProgressiveImage(props.lowQualitySrc, props.src)
  : { currentSrc: ref(props.src), loadHighQuality: () => {} }

// Compute optimized image source
const currentSrc = computed(() => {
  if (props.progressive) {
    return progressiveSrc.value
  }
  
  if (props.optimize) {
    return imageUtils.optimizeUrl(props.src, {
      width: typeof props.width === 'number' ? props.width : undefined,
      height: typeof props.height === 'number' ? props.height : undefined,
      quality: props.quality,
      format: props.format
    })
  }
  
  return props.src
})

// Container styles
const containerStyle = computed(() => {
  const styles: Record<string, string> = {
    position: 'relative',
    overflow: 'hidden'
  }
  
  if (props.width) {
    styles.width = typeof props.width === 'number' ? `${props.width}px` : props.width
  }
  
  if (props.height) {
    styles.height = typeof props.height === 'number' ? `${props.height}px` : props.height
  }
  
  if (props.aspectRatio) {
    styles.aspectRatio = props.aspectRatio
  }
  
  return styles
})

// Image styles
const imageStyle = computed(() => {
  const styles: Record<string, string> = {
    width: '100%',
    height: '100%',
    objectFit: 'cover'
  }
  
  if (props.blurUp && isLoading.value) {
    styles.filter = 'blur(5px)'
    styles.transform = 'scale(1.1)'
  }
  
  return styles
})

// Placeholder styles
const placeholderStyle = computed((): Record<string, string> => ({
  backgroundColor: '#f0f0f0',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  flexDirection: 'column',
  gap: '8px',
  width: '100%',
  height: '100%',
  position: 'absolute',
  top: '0',
  left: '0'
}))

// Event handlers
const handleLoad = (event: Event) => {
  isLoading.value = false
  isLoaded.value = true
  hasError.value = false
  emit('load', event)
}

const handleError = (event: Event) => {
  isLoading.value = false
  hasError.value = true
  isLoaded.value = false
  emit('error', event)
}

const handleClick = (event: MouseEvent) => {
  emit('click', event)
}

// Setup lazy loading
onMounted(() => {
  if (imageRef.value && props.loading === 'lazy' && !props.nativeLoading) {
    // Store original src in data attribute for lazy loading
    imageRef.value.dataset.src = currentSrc.value
    imageRef.value.src = '' // Clear src to prevent immediate loading
    observe(imageRef.value)
  }
  
  if (props.progressive && props.lowQualitySrc) {
    loadHighQuality()
  }
})

onUnmounted(() => {
  if (imageRef.value) {
    unobserve(imageRef.value)
  }
})

// Watch for src changes
watch(() => props.src, (newSrc) => {
  if (imageRef.value && newSrc) {
    isLoading.value = true
    isLoaded.value = false
    hasError.value = false
    
    if (props.loading === 'lazy' && !props.nativeLoading) {
      imageRef.value.dataset.src = newSrc
      observe(imageRef.value)
    } else {
      imageRef.value.src = newSrc
    }
  }
})
</script>

<style scoped>
.lazy-image-container {
  display: inline-block;
  background-color: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.lazy-image {
  display: block;
  border-radius: inherit;
  transition: all 0.3s ease;
}

.lazy-image.fade-in {
  opacity: 0;
  animation: fadeIn 0.3s ease forwards;
}

.lazy-image.blur-up {
  transition: filter 0.3s ease, transform 0.3s ease;
}

.lazy-placeholder {
  color: #6b7280;
  font-size: 14px;
  z-index: 1;
}

.lazy-spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #e5e7eb;
  border-top: 2px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.lazy-loading-text {
  font-size: 12px;
  color: #9ca3af;
}

.lazy-error-state {
  color: #ef4444;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  height: 100%;
  position: absolute;
  top: 0;
  left: 0;
  background-color: #fef2f2;
  z-index: 1;
}

.lazy-error-icon {
  width: 24px;
  height: 24px;
}

.lazy-error-text {
  font-size: 12px;
  text-align: center;
}

.lazy-progressive-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-size: cover;
  background-position: center;
  filter: blur(5px);
  transform: scale(1.1);
  z-index: 0;
}

.loading .lazy-image {
  opacity: 0;
}

.loaded .lazy-placeholder,
.loaded .lazy-progressive-overlay {
  opacity: 0;
  pointer-events: none;
}

.error .lazy-image {
  opacity: 0;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Mobile optimizations */
@media (max-width: 768px) {
  .lazy-placeholder {
    font-size: 12px;
  }
  
  .lazy-spinner {
    width: 20px;
    height: 20px;
  }
  
  .lazy-error-icon {
    width: 20px;
    height: 20px;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .lazy-image,
  .lazy-placeholder,
  .lazy-progressive-overlay {
    transition: none;
    animation: none;
  }
  
  .lazy-image.blur-up {
    filter: none;
    transform: none;
  }
  
  .lazy-spinner {
    animation: none;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .lazy-placeholder {
    background-color: #000;
    color: #fff;
  }
  
  .lazy-error-state {
    background-color: #fff;
    color: #000;
    border: 2px solid #000;
  }
}
</style>