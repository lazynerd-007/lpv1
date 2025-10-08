import { ref, onMounted, onUnmounted } from 'vue'

export function useLazyImage() {
  const loadedImages = ref<Set<string>>(new Set())
  let imageObserver: IntersectionObserver | null = null

  const handleImageLoad = (imageId: string) => {
    loadedImages.value.add(imageId)
  }

  const isImageLoaded = (imageId: string) => {
    return loadedImages.value.has(imageId)
  }

  const setupObserver = () => {
    imageObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const img = entry.target as HTMLImageElement
            const imageId = img.dataset.imageId
            if (imageId && img.dataset.src) {
              img.src = img.dataset.src
              img.onload = () => handleImageLoad(imageId)
              imageObserver?.unobserve(img)
            }
          }
        })
      },
      {
        rootMargin: '50px',
        threshold: 0.1
      }
    )
  }

  const observeImage = (img: HTMLImageElement) => {
    if (imageObserver && img) {
      imageObserver.observe(img)
    }
  }

  const preloadImage = (src: string, imageId: string) => {
    const img = new Image()
    img.onload = () => handleImageLoad(imageId)
    img.src = src
  }

  onMounted(() => {
    setupObserver()
  })

  onUnmounted(() => {
    if (imageObserver) {
      imageObserver.disconnect()
    }
  })

  return {
    loadedImages,
    isImageLoaded,
    observeImage,
    preloadImage,
    handleImageLoad
  }
}