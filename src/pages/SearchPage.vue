<script setup lang="ts">
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSearchStore } from '@/stores/searchStore'
import { useMovieStore } from '@/stores/movieStore'
import { useUIStore } from '@/stores/uiStore'
import SearchHeader from '@/components/sections/search/SearchHeader.vue'
import SearchFilters from '@/components/sections/search/SearchFilters.vue'
import MovieGrid from '@/components/sections/browse/MovieGrid.vue'

const route = useRoute()
const searchStore = useSearchStore()
const movieStore = useMovieStore()
const uiStore = useUIStore()

// Methods
const handlePageChange = (page: number) => {
  searchStore.setPage(page)
  // Scroll to top
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const handlePlayTrailer = (movie: any) => {
  uiStore.openTrailerModal(movie.id, movie.trailerUrl || '')
}

// Lifecycle
onMounted(async () => {
  // Set page title
  uiStore.setPageTitle('Search Movies - Nollywood Movies')
  
  // Load search state from URL
  searchStore.loadFromURL(route.query)
})

// Watch for route changes
watch(() => route.query, (newQuery) => {
  searchStore.loadFromURL(newQuery)
}, { deep: true })
</script>

<template>
  <div class="min-h-screen bg-base-100">
    <!-- Search Header -->
    <SearchHeader />

    <!-- Filters Section -->
    <SearchFilters />

    <!-- Results Section -->
    <MovieGrid 
      :movies="searchStore.filteredResults"
      :loading="searchStore.searchState.isLoading"
      :current-page="searchStore.currentPage"
      :show-pagination="true"
      @page-change="handlePageChange"
      @play-trailer="handlePlayTrailer"
    />
  </div>
</template>

<style scoped>
/* Additional custom styles if needed */
</style>