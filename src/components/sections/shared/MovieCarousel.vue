<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { Play } from 'lucide-vue-next'
import { useUIStore } from '@/stores/uiStore'
import type { Movie } from '@/data/mockMovies'
import LemonPieRating from '@/components/LemonPieRating.vue'

interface Props {
  title: string
  subtitle?: string
  movies: Movie[]
  maxItems?: number
  showPlayButton?: boolean
  backgroundColor?: string
  textColor?: string
  subtitleColor?: string
}

const props = withDefaults(defineProps<Props>(), {
  maxItems: 6,
  showPlayButton: true,
  backgroundColor: 'bg-white',
  textColor: 'text-gray-900',
  subtitleColor: 'text-gray-600'
})

const uiStore = useUIStore()
const carouselRef = ref<HTMLElement>()
const loadedImages = ref<Set<string>>(new Set())
let imageObserver: IntersectionObserver | null = null

const scrollLeft = () => {
  if (carouselRef.value) {
    carouselRef.value.scrollBy({ left: -300, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (carouselRef.value) {
    carouselRef.value.scrollBy({ left: 300, behavior: 'smooth' })
  }
}

const playTrailer = (movie: Movie) => {
  uiStore.openTrailerModal(movie.id, movie.trailerUrl || '')
}

const navigateToMovie = (movieId: string) => {
  // This would typically use router.push
  window.location.href = `/movie/${movieId}`
}

const handleImageLoad = (movieId: string) => {
  loadedImages.value.add(movieId)
}

const isImageLoaded = (movieId: string) => {
  return loadedImages.value.has(movieId)
}

onMounted(() => {
  // Set up intersection observer for lazy loading
  imageObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement
          const movieId = img.dataset.movieId
          if (movieId && img.dataset.src) {
            img.src = img.dataset.src
            img.onload = () => handleImageLoad(movieId)
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
})

onUnmounted(() => {
  if (imageObserver) {
    imageObserver.disconnect()
  }
})
</script>

<template>
  <section :class="[backgroundColor, 'py-12']">
    <div class="container mx-auto px-4">
      <!-- Section Header -->
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-3">
          <div class="w-1 h-8 bg-orange-500 rounded"></div>
          <div>
            <h2 :class="['text-2xl font-bold', textColor]">{{ title }}</h2>
            <p v-if="subtitle" :class="[subtitleColor]">{{ subtitle }}</p>
          </div>
        </div>
        
        <!-- Navigation Arrows -->
        <div class="flex gap-2">
          <button 
            @click="scrollLeft"
            class="p-2 rounded-full bg-theme-surface hover:bg-theme-surface-hover transition-colors"
          >
            <svg class="w-5 h-5 text-theme-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
          </button>
          <button 
            @click="scrollRight"
            class="p-2 rounded-full bg-theme-surface hover:bg-theme-surface-hover transition-colors"
          >
            <svg class="w-5 h-5 text-theme-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Movies Carousel -->
      <div
        ref="carouselRef"
        class="flex gap-6 overflow-x-auto pb-4 scrollbar-hide scroll-smooth"
      >
        <div
          v-for="movie in movies.slice(0, maxItems)"
          :key="movie.id"
          class="flex-shrink-0 w-48 group cursor-pointer"
          @click="navigateToMovie(movie.id)"
        >
          <!-- Movie Poster with Play Button -->
          <div class="relative mb-3">
            <div class="relative w-full h-72 rounded-lg overflow-hidden shadow-md">
              <img
                :data-src="movie.posterUrl"
                :data-movie-id="movie.id"
                :alt="movie.title"
                :src="isImageLoaded(movie.id) ? movie.posterUrl : ''"
                class="w-full h-full object-cover transition-opacity duration-300"
                :class="{ 'opacity-100': isImageLoaded(movie.id), 'opacity-0': !isImageLoaded(movie.id) }"
                ref="(el) => el && imageObserver?.observe(el as HTMLImageElement)"
                loading="lazy"
                decoding="async"
              />
              <div
                v-if="!isImageLoaded(movie.id)"
                class="absolute inset-0 bg-gradient-to-br from-gray-300 to-gray-400 animate-pulse flex items-center justify-center"
              >
                <div class="text-gray-500 text-sm">Loading...</div>
              </div>
            </div>
           
            <!-- Play Button Overlay -->
            <div
              v-if="showPlayButton"
              class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded-lg"
            >
              <div
                class="bg-white/90 rounded-full p-3 transform scale-90 group-hover:scale-100 transition-transform"
                @click.stop="playTrailer(movie)"
              >
                <Play class="w-8 h-8 text-gray-800" fill="currentColor" />
              </div>
            </div>
           
            <!-- Rating Badge -->
            <div class="absolute top-3 left-3">
              <LemonPieRating
                :rating="movie.lemonPieRating"
                size="sm"
                :show-text="false"
              />
            </div>
          </div>
          
          <!-- Movie Title -->
          <h3 :class="['font-semibold text-sm leading-tight group-hover:text-orange-500 transition-colors', textColor]">
            {{ movie.title }}
          </h3>
          
          <!-- Additional Info -->
          <div class="text-xs text-theme-tertiary mt-1">
            {{ movie.releaseDate.split('-')[0] }} • {{ movie.genre.slice(0, 2).join(', ') }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>