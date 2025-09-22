<script setup lang="ts">
import { ref, computed } from 'vue'
import { Play, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'

const movieStore = useMovieStore()

// Mock data for upcoming releases
const upcomingMovies = ref([
  {
    id: 'upcoming-1',
    title: 'The Naked Gun',
    releaseDate: '7/30/2025',
    poster: 'https://images.unsplash.com/photo-1489599735734-79b4169c2a78?w=400&h=600&fit=crop&crop=center',
    trailerUrl: '#'
  },
  {
    id: 'upcoming-2', 
    title: 'Labinak',
    releaseDate: '8/21/2025',
    poster: 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=400&h=600&fit=crop&crop=center',
    trailerUrl: '#'
  },
  {
    id: 'upcoming-3',
    title: 'Weapons',
    releaseDate: '8/6/2025 • R',
    poster: 'https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=400&h=600&fit=crop&crop=center',
    trailerUrl: '#'
  },
  {
    id: 'upcoming-4',
    title: 'Freakier Friday',
    releaseDate: '8/6/2025 • PG',
    poster: 'https://images.unsplash.com/photo-1594736797933-d0401ba2fe65?w=400&h=600&fit=crop&crop=center',
    trailerUrl: '#'
  },
  {
    id: 'upcoming-5',
    title: 'The Last Dance',
    releaseDate: '9/15/2025 • PG-13',
    poster: 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400&h=600&fit=crop&crop=center',
    trailerUrl: '#'
  }
])

const scrollContainer = ref<HTMLElement>()
const canScrollLeft = ref(false)
const canScrollRight = ref(true)

const checkScrollButtons = () => {
  if (scrollContainer.value) {
    const { scrollLeft, scrollWidth, clientWidth } = scrollContainer.value
    canScrollLeft.value = scrollLeft > 0
    canScrollRight.value = scrollLeft < scrollWidth - clientWidth - 10
  }
}

const scrollLeft = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: -300, behavior: 'smooth' })
    setTimeout(checkScrollButtons, 300)
  }
}

const scrollRight = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: 300, behavior: 'smooth' })
    setTimeout(checkScrollButtons, 300)
  }
}

const playTrailer = (movie: any) => {
  console.log('Playing trailer for:', movie.title)
  // Implement trailer playback logic
}
</script>

<template>
  <section class="py-12 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="flex items-center justify-between mb-8">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <span class="w-1 h-6 bg-orange-500 rounded"></span>
            Fresh pies
            <ChevronRight class="w-5 h-5 text-gray-400" />
          </h2>
          <p class="text-gray-600 mt-1">Fresh and exciting movies coming your way</p>
        </div>
        
        <!-- Navigation Buttons -->
        <div class="flex gap-2">
          <button 
            @click="scrollLeft"
            :disabled="!canScrollLeft"
            class="p-2 rounded-full bg-theme-surface hover:bg-theme-surface-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <ChevronLeft class="w-5 h-5 text-theme-secondary" />
          </button>
          <button 
            @click="scrollRight"
            :disabled="!canScrollRight"
            class="p-2 rounded-full bg-theme-surface hover:bg-theme-surface-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <ChevronRight class="w-5 h-5 text-theme-secondary" />
          </button>
        </div>
      </div>

      <!-- Movies Carousel -->
      <div class="relative">
        <div 
          ref="scrollContainer"
          @scroll="checkScrollButtons"
          class="flex gap-6 overflow-x-auto scrollbar-hide pb-4"
          style="scroll-snap-type: x mandatory;"
        >
          <div 
            v-for="movie in upcomingMovies" 
            :key="movie.id"
            class="flex-none w-64 group cursor-pointer"
            style="scroll-snap-align: start;"
            @click="playTrailer(movie)"
          >
            <!-- Movie Poster -->
            <div class="relative aspect-[3/4] rounded-lg overflow-hidden bg-gray-200 mb-3">
              <img 
                :src="movie.poster" 
                :alt="movie.title"
                class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
                loading="lazy"
              />
              
              <!-- Play Button Overlay -->
              <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center">
                <div class="w-16 h-16 bg-white bg-opacity-90 rounded-full flex items-center justify-center transform scale-0 group-hover:scale-100 transition-transform duration-300">
                  <Play class="w-6 h-6 text-gray-900 ml-1" fill="currentColor" />
                </div>
              </div>
            </div>
            
            <!-- Movie Info -->
            <div class="space-y-1">
              <h3 class="font-semibold text-theme-primary text-lg leading-tight">{{ movie.title }}</h3>
              <p class="text-theme-secondary text-sm">{{ movie.releaseDate }}</p>
            </div>
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