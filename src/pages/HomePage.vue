<script setup lang="ts">
import { onMounted } from 'vue'
import { useMovieStore } from '@/stores/movieStore'
import { useUIStore } from '@/stores/uiStore'
import HeroSection from '@/components/sections/HeroSection.vue'
import MovieCarousel from '@/components/sections/MovieCarousel.vue'
import ReleasingSoonSection from '@/components/sections/ReleasingSoonSection.vue'
import TrendingActorsSection from '@/components/sections/TrendingActorsSection.vue'

const movieStore = useMovieStore()
const uiStore = useUIStore()

onMounted(async () => {
  // Set page title
  uiStore.setPageTitle('Home - Nollywood Movies')
  
  // Movies are already loaded from mockMovies
})
</script>

<template>
  <div class="min-h-screen bg-base-100">
    <!-- Hero Section -->
    <HeroSection />

    <!-- Now Playing Section -->
    <MovieCarousel 
      title="Now Playing"
      subtitle="Latest Nollywood releases in cinemas"
      :movies="movieStore.trendingMovies"
      :max-items="8"
      background-color="bg-base-100"
    />

    <!-- Releasing Soon Section -->
    <ReleasingSoonSection />

    <!-- Trending Actors Section -->
    <TrendingActorsSection />

    <!-- Trending TV Shows Section -->
    <MovieCarousel 
      title="Trending TV Shows"
      subtitle="Popular Nollywood series and shows"
      :movies="movieStore.trendingMovies.slice(0, 8)"
      :max-items="8"
      background-color="bg-gray-50"
    />

  </div>
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -30px, 0);
  }
  70% {
    transform: translate3d(0, -15px, 0);
  }
  90% {
    transform: translate3d(0, -4px, 0);
  }
}

.animate-bounce {
  animation: bounce 2s infinite;
}
</style>
