<script setup lang="ts">
import { ref } from 'vue'
import { ChevronLeft, ChevronRight, Play } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'

const movieStore = useMovieStore()
const scrollContainer = ref<HTMLElement>()

// Get a subset of movies for Fresh Lemons section
const freshLemonMovies = movieStore.allMovies.slice(8, 12)

const scrollLeft = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: -320, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: 320, behavior: 'smooth' })
  }
}

const playTrailer = (movieId: string) => {
  console.log('Playing trailer for movie:', movieId)
}
</script>

<template>
  <section class="py-16 bg-yellow-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-3">
            <span class="w-1 h-6 bg-yellow-500 rounded"></span>
            <h2 class="text-2xl font-bold text-gray-900">Fresh Lemons</h2>
          </div>
          <p class="text-gray-600 hidden sm:block">Zesty and refreshing movie picks</p>
        </div>
        
        <!-- Navigation Arrows -->
        <div class="flex gap-2">
          <button 
            @click="scrollLeft"
            class="p-2 rounded-full bg-white shadow-md hover:shadow-lg transition-shadow duration-200 hover:bg-gray-50"
          >
            <ChevronLeft class="w-5 h-5 text-gray-600" />
          </button>
          <button 
            @click="scrollRight"
            class="p-2 rounded-full bg-white shadow-md hover:shadow-lg transition-shadow duration-200 hover:bg-gray-50"
          >
            <ChevronRight class="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>

      <!-- Movies Carousel -->
      <div 
        ref="scrollContainer"
        class="flex gap-6 overflow-x-auto scrollbar-hide scroll-smooth"
        style="scroll-snap-type: x mandatory;"
      >
        <div 
          v-for="movie in freshLemonMovies" 
          :key="movie.id"
          class="flex-none w-72 group cursor-pointer"
          style="scroll-snap-align: start;"
        >
          <!-- Movie Card -->
          <div class="relative bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
            <!-- Movie Poster -->
            <div class="relative aspect-[3/4] overflow-hidden">
              <img 
                :src="movie.poster" 
                :alt="movie.title"
                class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                loading="lazy"
              />
              
              <!-- Play Button Overlay -->
              <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                <button 
                  @click="playTrailer(movie.id)"
                  class="opacity-0 group-hover:opacity-100 transform scale-75 group-hover:scale-100 transition-all duration-300 bg-yellow-500 hover:bg-yellow-600 text-white rounded-full p-3 shadow-lg"
                >
                  <Play class="w-6 h-6 fill-current" />
                </button>
              </div>
              
              <!-- Rating Badge -->
              <div class="absolute top-3 right-3 bg-yellow-500 text-white px-2 