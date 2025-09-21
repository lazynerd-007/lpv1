<script setup lang="ts">
import { onMounted } from 'vue'
import { useMovieStore } from '@/stores/movieStore'
import { useUIStore } from '@/stores/uiStore'
import HeroSection from '@/components/sections/home/HeroSection.vue'
import MovieCarousel from '@/components/sections/shared/MovieCarousel.vue'
import ReleasingSoonSection from '@/components/sections/home/ReleasingSoonSection.vue'
import TrendingActorsSection from '@/components/sections/home/TrendingActorsSection.vue'
import FreshLemonsSection from '@/components/sections/home/FreshLemonsSection.vue'

const movieStore = useMovieStore()
const uiStore = useUIStore()

onMounted(async () => {
  // Set page title
  uiStore.setPageTitle('Home - Nollywood Movies')
  
  // Movies are already loaded from mockMovies
})
</script>

<template>
  <div class="min-h-screen bg-theme-background">
    <!-- Hero Section -->
    <HeroSection />

    <!-- Now Playing Section -->
    <MovieCarousel 
      title="Now Playing"
      subtitle="Latest Nollywood releases in cinemas"
      :movies="movieStore.trendingMovies"
      :max-items="8"
      background-color="bg-gray-900"
      text-color="text-white"
      subtitle-color="text-gray-300"
    />

    <!-- Releasing Soon Section -->
    <ReleasingSoonSection />

    <!-- Trending Actors Section -->
    <TrendingActorsSection />

    <!-- Trending Movies Section -->
    <MovieCarousel 
      title="Trending Movies"
      subtitle="Most popular Nollywood films right now"
      :movies="movieStore.movies.slice(0, 8)"
      :max-items="8"
      background-color="bg-theme-section-alt"
      text-color="text-theme-primary"
      subtitle-color="text-theme-secondary"
    />

    <!-- Fresh Lemons Section -->
    <FreshLemonsSection />

    <!-- Top Rated Section -->
    <MovieCarousel 
      title="Top Rated"
      subtitle="Highest rated Nollywood films of all time"
      :movies="movieStore.topRatedMovies"
      :max-items="8"
      background-color="bg-theme-section-accent"
      text-color="text-theme-primary"
      subtitle-color="text-theme-secondary"
    />

    <!-- Recently Added Section -->
    <MovieCarousel 
      title="Recently Added"
      subtitle="Fresh additions to our Nollywood collection"
      :movies="movieStore.recentlyAddedMovies"
      :max-items="8"
      background-color="bg-theme-background"
      text-color="text-theme-primary"
      subtitle-color="text-theme-secondary"
    />
  </div>
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
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
