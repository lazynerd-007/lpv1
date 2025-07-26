<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <!-- Header Section -->
    <div class="bg-gradient-to-r from-yellow-500 to-orange-600 py-16">
      <div class="container mx-auto px-4">
        <h1 class="text-5xl font-bold text-white mb-4">Browse Nollywood Movies</h1>
        <p class="text-xl text-yellow-100">Discover the best of Nigerian cinema</p>
      </div>
    </div>

    <!-- Filters Section -->
    <div class="container mx-auto px-4 py-8">
      <SearchFilters @filter-change="handleFilterChange" />

      <!-- Results Summary -->
      <div class="flex justify-between items-center mb-6">
        <div class="text-lg font-semibold text-white">
          Showing {{ filteredMovies.length }} of {{ movieStore.movies.length }} movies
        </div>
        <div class="flex gap-2">
          <button 
            @click="viewMode = 'grid'" 
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              viewMode === 'grid' 
                ? 'bg-yellow-500 text-black' 
                : 'bg-gray-700 text-white hover:bg-gray-600'
            ]"
          >
            <Grid class="w-4 h-4" />
          </button>
          <button 
            @click="viewMode = 'list'" 
            :class="[
              'px-4 py-2 rounded-lg font-medium transition-colors',
              viewMode === 'list' 
                ? 'bg-yellow-500 text-black' 
                : 'bg-gray-700 text-white hover:bg-gray-600'
            ]"
          >
            <List class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Movies Grid/List -->
      <div v-if="filteredMovies.length > 0">
        <!-- Grid View -->
        <div v-if="viewMode === 'grid'">
          <MovieGrid 
            :movies="paginatedMovies"
            :loading="false"
            :current-page="currentPage"
            :show-pagination="false"
            @page-change="handlePageChange"
          />
        </div>

        <!-- List View -->
        <div v-else class="space-y-4">
          <div 
            v-for="movie in paginatedMovies" 
            :key="movie.id" 
            class="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition-colors duration-200"
          >
            <div class="flex flex-col md:flex-row gap-6">
              <div class="flex-shrink-0">
                <img 
                  :src="movie.poster" 
                  :alt="movie.title" 
                  class="w-24 h-36 object-cover rounded-lg"
                />
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-start mb-3">
                  <h3 class="text-xl font-bold text-white">{{ movie.title }}</h3>
                  <div class="flex items-center gap-1">
                    <span class="text-yellow-400 font-semibold">{{ movie.lemonPieRating.toFixed(1) }}</span>
                    <span class="text-gray-400">/5</span>
                  </div>
                </div>
                <p class="text-gray-400 mb-3">{{ movie.releaseDate }} • {{ movie.genre.join(', ') }}</p>
                <p class="text-gray-300 mb-4 line-clamp-2">{{ movie.plotSummary }}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                  <span 
                    v-for="actor in movie.cast.slice(0, 3)" 
                    :key="actor" 
                    class="bg-gray-700 text-gray-300 px-3 py-1 rounded-full text-sm"
                  >
                    {{ actor }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <div class="text-sm text-gray-400">
                    {{ movie.runtime }} min • {{ movie.language }}
                  </div>
                  <router-link 
                    :to="`/movie/${movie.id}`" 
                    class="bg-yellow-500 hover:bg-yellow-600 text-black px-4 py-2 rounded-lg font-semibold transition-colors"
                  >
                    View Details
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex justify-center mt-12" v-if="totalPages > 1">
          <div class="flex gap-2">
            <button 
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-colors',
                currentPage === 1
                  ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                  : 'bg-gray-700 text-white hover:bg-gray-600'
              ]"
            >
              <ChevronLeft class="w-4 h-4" />
            </button>
            
            <button 
              v-for="page in visiblePages" 
              :key="page"
              @click="currentPage = page"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-colors',
                currentPage === page
                  ? 'bg-yellow-500 text-black'
                  : 'bg-gray-700 text-white hover:bg-gray-600'
              ]"
            >
              {{ page }}
            </button>
            
            <button 
              @click="currentPage = Math.min(totalPages, currentPage + 1)"
              :disabled="currentPage === totalPages"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-colors',
                currentPage === totalPages
                  ? 'bg-gray-700 text-gray-500 cursor-not-allowed'
                  : 'bg-gray-700 text-white hover:bg-gray-600'
              ]"
            >
              <ChevronRight class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else class="text-center py-16 bg-gray-800 rounded-lg">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-2xl font-bold text-white mb-2">No movies found</h3>
        <p class="text-gray-400 mb-6">Try adjusting your filters or search terms</p>
        <button 
          @click="clearFilters" 
          class="bg-yellow-500 hover:bg-yellow-600 text-black px-6 py-3 rounded-lg font-semibold transition-colors"
        >
          Clear All Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { Filter, Search, RotateCcw, Grid, List, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useSearchStore } from '@/stores/searchStore'
import { useUIStore } from '@/stores/uiStore'
import MovieCard from '@/components/ui/MovieCard.vue'
import SearchFilters from '@/components/sections/SearchFilters.vue'
import MovieGrid from '@/components/sections/MovieGrid.vue'

const movieStore = useMovieStore()
const searchStore = useSearchStore()
const uiStore = useUIStore()

// Local reactive data
const viewMode = ref('grid')
const currentPage = ref(1)
const itemsPerPage = 12

// Computed properties
const filteredMovies = computed(() => {
  return movieStore.filterMovies({
    genre: searchStore.filters.genre,
    year: searchStore.filters.year,
    rating: searchStore.filters.rating,
    language: searchStore.filters.language,
    productionState: searchStore.filters.productionState
  })
})

const totalPages = computed(() => Math.ceil(filteredMovies.value.length / itemsPerPage))

const paginatedMovies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredMovies.value.slice(start, end)
})

const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, start + 4)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const clearFilters = () => {
  searchStore.clearFilters()
  currentPage.value = 1
}

const handleSearch = (query: string) => {
  searchStore.performSearch(query)
  currentPage.value = 1
}

const handleFilterChange = () => {
  currentPage.value = 1
}

const handlePageChange = (page: number) => {
  currentPage.value = page
}

// Watch for filter changes to reset pagination
watch(
  () => [searchStore.searchState.query, searchStore.filters],
  () => {
    currentPage.value = 1
  },
  { deep: true }
)

// Set page title and load data
onMounted(async () => {
  uiStore.setPageTitle('Browse Movies - Nollywood Movies')
  
  // Movies are already loaded from mockMovies
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>