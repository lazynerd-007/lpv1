<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { Play } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useUIStore } from '@/stores/uiStore'
import type { Movie } from '@/data/mockMovies'

interface Props {
  movie?: Movie
}

const props = defineProps<Props>()
const movieStore = useMovieStore()
const uiStore = useUIStore()

const featuredMovie = computed(() => props.movie || movieStore.featuredMovie)
const imageLoaded = ref(false)
const heroRef = ref<HTMLElement>()

const playTrailer = () => {
  if (featuredMovie.value) {
    uiStore.openTrailerModal(featuredMovie.value.id, featuredMovie.value.trailerUrl || '')
  }
}

const handleImageLoad = () => {
  imageLoaded.value = true
}

onMounted(() => {
  // Preload the featured movie image
  if (featuredMovie.value?.posterUrl) {
    const img = new Image()
    img.onload = handleImageLoad
    img.src = featuredMovie.value.posterUrl
  }
})
</script>

<template>
  <section v-if="featuredMovie" ref="heroRef" class="relative h-[80vh] overflow-hidden">
    <!-- Background Image with Solid Color Overlay -->
    <div 
      class="absolute inset-0 bg-cover bg-center bg-no-repeat transition-opacity duration-500"
      :class="{ 'opacity-100': imageLoaded, 'opacity-0': !imageLoaded }"
      :style="{ backgroundImage: imageLoaded ? `url(${featuredMovie.posterUrl})` : 'none' }"
    >
      <div class="absolute inset-0 bg-purple-900/80"></div>
    </div>
    
    <!-- Loading placeholder -->
    <div 
      v-if="!imageLoaded"
      class="absolute inset-0 bg-gradient-to-r from-purple-900 to-purple-800 animate-pulse"
    ></div>
    
    <!-- Content -->
    <div class="relative z-10 h-full flex items-center">
      <div class="container mx-auto px-4">
        <div class="flex items-center gap-8 max-w-6xl">
          <!-- Movie Poster -->
          <div class="hidden md:block flex-shrink-0">
            <div class="relative w-80 h-[450px] rounded-lg overflow-hidden shadow-2xl">
              <img 
                v-if="imageLoaded"
                :src="featuredMovie.posterUrl" 
                :alt="featuredMovie.title"
                class="w-full h-full object-cover transition-opacity duration-300"
                loading="eager"
                decoding="async"
              />
              <div 
                v-else
                class="w-full h-full bg-gradient-to-br from-gray-700 to-gray-800 animate-pulse flex items-center justify-center"
              >
                <div class="text-gray-400 text-lg">Loading...</div>
              </div>
            </div>
          </div>
          
          <!-- Movie Details -->
          <div class="flex-1 text-white">
            <!-- Rating -->
            <div class="flex items-center gap-2 mb-4">
              <div class="flex items-center gap-1">
                <span class="text-yellow-400">⭐</span>
                <span class="text-2xl font-bold">{{ featuredMovie.lemonPieRating }}</span>
                <span class="text-gray-300">/ 10</span>
              </div>
            </div>
            
            <!-- Title -->
            <h1 class="text-5xl md:text-6xl font-bold mb-4 leading-tight">
              {{ featuredMovie.title }}
            </h1>
            
            <!-- Local Title -->
            <p v-if="featuredMovie.localTitle" class="text-xl text-gray-300 italic mb-6">
              {{ featuredMovie.localTitle }}
            </p>
            
            <!-- Description -->
            <p class="text-lg text-white/90 mb-8 max-w-2xl leading-relaxed">
              {{ featuredMovie.plotSummary }}
            </p>
            
            <!-- Action Button -->
            <button 
              @click="playTrailer"
              class="flex items-center gap-3 bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors"
            >
              <Play class="w-6 h-6" fill="currentColor" />
              Play trailer
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Navigation Arrows -->
    <button class="absolute left-4 top-1/2 transform -translate-y-1/2 bg-black/30 hover:bg-black/60 text-white p-3 rounded-full transition-colors">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
      </svg>
    </button>
    <button class="absolute right-4 top-1/2 transform -translate-y-1/2 bg-black/30 hover:bg-black/60 text-white p-3 rounded-full transition-colors">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
      </svg>
    </button>
  </section>
</template>