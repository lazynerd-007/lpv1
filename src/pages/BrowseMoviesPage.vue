<template>
  <div class="min-h-screen bg-theme-background">
    <!-- Header Section -->
    <div class="container mx-auto px-2 py-4">
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-3">
          <span class="w-1 h-8 bg-orange-500 rounded"></span>
          <h1 class="text-3xl font-bold text-gray-900">Browse Movies</h1>
        </div>
        
        <div class="flex items-center gap-4">
          <!-- Genre Filter Dropdown -->
          <div class="relative">
            <select 
              v-model="selectedGenre" 
              @change="handleGenreChange"
              class="appearance-none bg-theme-surface border border-theme rounded-lg px-4 py-2 pr-8 text-theme-primary focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="">All Genres</option>
              <option v-for="genre in genres" :key="genre" :value="genre">{{ genre }}</option>
            </select>
            <ChevronDown class="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
          </div>
          
          <!-- Sort Dropdown -->
          <div class="relative">
            <select 
              v-model="sortBy" 
              @change="handleSortChange"
              class="appearance-none bg-theme-surface border border-theme rounded-lg px-4 py-2 pr-8 text-theme-primary focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="popularity">Most popular first</option>
              <option value="rating">Highest rated</option>
              <option value="newest">Newest first</option>
              <option value="oldest">Oldest first</option>
              <option value="title">A-Z</option>
            </select>
            <ChevronDown class="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
          </div>
          
          <!-- View Toggle -->
          <div class="flex border border-gray-300 rounded-lg overflow-hidden">
            <button 
              @click="viewMode = 'grid'" 
              :class="[
                'px-3 py-2 transition-colors',
                viewMode === 'grid' 
                  ? 'bg-theme-primary text-theme-primary-text' 
                  : 'bg-theme-surface text-theme-text hover:bg-theme-surface-hover'
              ]"
            >
              <Grid class="w-4 h-4" />
            </button>
            <button 
              @click="viewMode = 'list'" 
              :class="[
                'px-3 py-2 transition-colors border-l border-theme-border',
                viewMode === 'list' 
                  ? 'bg-theme-primary text-theme-primary-text' 
                  : 'bg-theme-surface text-theme-text hover:bg-theme-surface-hover'
              ]"
            >
              <List class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
      
      <!-- Filters Section -->
      <div v-if="showFilters" class="mb-8">
        <SearchFilters @filter-change="handleFilterChange" />
      </div>

      <!-- Movies Grid/List -->
      <div v-if="filteredMovies.length > 0">
        <!-- Grid View -->
        <div v-if="viewMode === 'grid'">
          <MovieGrid 
            :movies="displayedMovies"
            :loading="isLoading"
            :current-page="1"
            :show-pagination="false"
          />
        </div>

        <!-- List View -->
        <div v-else class="space-y-4">
          <div 
            v-for="movie in displayedMovies" 
            :key="movie.id" 
            class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex flex-col md:flex-row gap-6">
              <div class="flex-shrink-0">
                <img 
                  :src="movie.posterUrl" 
                  :alt="movie.title" 
                  class="w-24 h-36 object-cover rounded-lg"
                />
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-start mb-3">
                  <h3 class="text-xl font-bold text-gray-900">{{ movie.title }}</h3>
                  <div class="flex items-center gap-1">
                    <span class="text-orange-500 font-semibold">{{ movie.lemonPieRating.toFixed(1) }}</span>
                    <span class="text-gray-500">/10</span>
                  </div>
                </div>
                <p class="text-gray-600 mb-3">{{ movie.releaseDate }} • {{ movie.genre.join(', ') }}</p>
                <p class="text-gray-700 mb-4 line-clamp-2">{{ movie.plotSummary }}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                  <span 
                    v-for="actor in movie.cast.slice(0, 3)" 
                    :key="actor" 
                    class="bg-theme-surface text-theme-text px-3 py-1 rounded-full text-sm"
                  >
                    {{ actor }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <div class="text-sm text-gray-500">
                    {{ movie.runtime }} min • {{ movie.language }}
                  </div>
                  <router-link 
                    :to="`/movie/${movie.id}`" 
                    class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-semibold transition-colors"
                  >
                    View Details
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading Indicator for Infinite Scroll -->
        <div v-if="isLoading" class="flex justify-center mt-8">
          <div class="flex items-center gap-2 text-gray-600">
            <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-orange-500"></div>
            <span>Loading more movies...</span>
          </div>
        </div>
        
        <!-- End of Results Indicator -->
        <div v-else-if="!canLoadMore && displayedMovies.length > 0" class="text-center mt-8 py-4">
          <p class="text-gray-500">You've reached the end of the movie list</p>
        </div>
      </div>

      <!-- No Results -->
      <div v-else class="text-center py-8 bg-theme-section-alt rounded-lg border border-theme-light">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">No movies found</h3>
        <p class="text-gray-600 mb-6">Try adjusting your filters or search terms</p>
        <button 
          @click="clearFilters" 
          class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
        >
          Clear All Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted, nextTick } from 'vue'
import { Grid, List, ChevronDown } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useSearchStore } from '@/stores/searchStore'
import { useUIStore } from '@/stores/uiStore'

import SearchFilters from '@/components/sections/search/SearchFilters.vue'
import MovieGrid from '@/components/sections/browse/MovieGrid.vue'

const movieStore = useMovieStore()
const searchStore = useSearchStore()
const uiStore = useUIStore()

// Local reactive data
const viewMode = ref('grid')
const itemsPerPage = 12
const showFilters = ref(false)
const sortBy = ref('popularity')
const selectedGenre = ref('')
const displayedMoviesCount = ref(itemsPerPage)
const isLoading = ref(false)
const hasMoreMovies = ref(true)

// Get all unique genres from movies
const genres = computed(() => {
  const uniqueGenres = new Set<string>()
  movieStore.movies.forEach(movie => {
    movie.genre.forEach(g => uniqueGenres.add(g))
  })
  return Array.from(uniqueGenres).sort()
})

// Computed properties
const filteredMovies = computed(() => {
  // Use the selectedGenre value if it's set, otherwise use the searchStore filter
  const genreFilter = selectedGenre.value || searchStore.filters.genre
  
  return movieStore.filterMovies({
    genre: genreFilter,
    year: searchStore.filters.year,
    rating: searchStore.filters.rating,
    language: searchStore.filters.language,
    productionState: searchStore.filters.productionState
  })
})

const displayedMovies = computed(() => {
  return filteredMovies.value.slice(0, displayedMoviesCount.value)
})

const canLoadMore = computed(() => {
  return displayedMoviesCount.value < filteredMovies.value.length
})

// Methods
const clearFilters = () => {
  searchStore.clearFilters()
  selectedGenre.value = ''
  displayedMoviesCount.value = itemsPerPage
  hasMoreMovies.value = true
}

const handleSearch = (query: string) => {
  searchStore.performSearch(query)
  displayedMoviesCount.value = itemsPerPage
  hasMoreMovies.value = true
}

const handleFilterChange = () => {
  displayedMoviesCount.value = itemsPerPage
  hasMoreMovies.value = true
}

const handleGenreChange = () => {
  // Update the search store with the selected genre
  searchStore.filters.genre = selectedGenre.value
  displayedMoviesCount.value = itemsPerPage
  hasMoreMovies.value = true
}

const handleSortChange = () => {
  // Sort functionality can be implemented here
  // For now, just reset displayed count
  displayedMoviesCount.value = itemsPerPage
  hasMoreMovies.value = true
}

const loadMoreMovies = () => {
  if (isLoading.value || !canLoadMore.value) return
  
  isLoading.value = true
  
  // Simulate loading delay
  setTimeout(() => {
    displayedMoviesCount.value += itemsPerPage
    isLoading.value = false
    hasMoreMovies.value = canLoadMore.value
  }, 500)
}

const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight
  
  // Load more when user is 200px from bottom
  if (scrollTop + windowHeight >= documentHeight - 200) {
    loadMoreMovies()
  }
}

// Watch for filter changes to reset displayed count
watch(
  () => [searchStore.searchState.query, searchStore.filters],
  () => {
    // Sync selectedGenre with searchStore.filters.genre
    if (searchStore.filters.genre !== selectedGenre.value) {
      selectedGenre.value = searchStore.filters.genre || ''
    }
    displayedMoviesCount.value = itemsPerPage
    hasMoreMovies.value = true
  },
  { deep: true }
)

// Set page title and setup scroll listener
onMounted(async () => {
  uiStore.setPageTitle('Browse Movies - Nollywood Movies')
  
  // Add scroll event listener for infinite scroll
  window.addEventListener('scroll', handleScroll)
  
  // Movies are already loaded from mockMovies
})

// Cleanup scroll listener
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>