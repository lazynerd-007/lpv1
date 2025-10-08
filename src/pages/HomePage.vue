<script setup lang="ts">
import { onMounted, defineAsyncComponent } from 'vue'
import { useMovieStore } from '@/stores/movieStore'
import { useUIStore } from '@/stores/uiStore'
import HeroSection from '@/components/sections/home/HeroSection.vue'
import MovieCarousel from '@/components/sections/shared/MovieCarousel.vue'

// Lazy load non-critical sections with loading states
const ReleasingSoonSection = defineAsyncComponent({
  loader: () => import('@/components/sections/home/ReleasingSoonSection.vue'),
  loadingComponent: { template: '<div class="h-64 bg-theme-surface animate-pulse rounded-lg mx-4 my-8"></div>' },
  delay: 200
})

const TrendingActorsSection = defineAsyncComponent({
  loader: () => import('@/components/sections/home/TrendingActorsSection.vue'),
  loadingComponent: { template: '<div class="h-64 bg-theme-surface animate-pulse rounded-lg mx-4 my-8"></div>' },
  delay: 200
})

const FreshLemonsSection = defineAsyncComponent({
  loader: () => import('@/components/sections/home/FreshLemonsSection.vue'),
  loadingComponent: { template: '<div class="h-64 bg-theme-surface animate-pulse rounded-lg mx-4 my-8"></div>' },
  delay: 200
})



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
      background-color="bg-theme-surface"
      text-color="text-theme-primary"
      subtitle-color="text-theme-secondary"
    />

    <!-- Releasing Soon Section -->
    <ReleasingSoonSection />

    <!-- Trending Actors Section -->
    <TrendingActorsSection />



    <!-- Featured Movies Section -->
    <MovieCarousel 
      title="Featured Movies" 
      subtitle="Handpicked selections from our critics"
      :movies="movieStore.pieMovies"
      :max-items="6"
      background-color="bg-theme-background"
      text-color="text-theme-primary"
      subtitle-color="text-theme-secondary"
    />
    
    <!-- Trending Movies Section -->
    <MovieCarousel 
      title="Trending Now" 
      subtitle="What everyone's watching"
      :movies="movieStore.trendingMovies"
      :max-items="6"
      background-color="bg-theme-surface"
      text-color="text-theme-primary"
      subtitle-color="text-theme-secondary"
    />
    
    <!-- Top Rated Movies Section -->
    <MovieCarousel 
      title="Top Rated" 
      subtitle="Highest rated by our community"
      :movies="movieStore.topRatedMovies"
      :max-items="6"
      background-color="bg-theme-background"
      text-color="text-theme-primary"
      subtitle-color="text-theme-secondary"
    />
    
    <!-- New Releases Section -->
    <MovieCarousel 
      title="New Releases" 
      subtitle="Fresh content just added"
      :movies="movieStore.recentlyAddedMovies"
      :max-items="6"
      background-color="bg-theme-surface"
      text-color="text-theme-primary"
      subtitle-color="text-theme-secondary"
    />

    <!-- Fresh Lemons Section -->
    <FreshLemonsSection />
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
