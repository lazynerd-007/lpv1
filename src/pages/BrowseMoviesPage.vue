<template>
  <div class="min-h-screen bg-white">
    <!-- Header Section -->
    <div class="container mx-auto px-4 py-8">
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-3">
          <span class="w-1 h-8 bg-orange-500 rounded"></span>
          <h1 class="text-3xl font-bold text-gray-900">Browse Movies</h1>
        </div>
        
        <div class="flex items-center gap-4">
          <!-- Sort Dropdown -->
          <div class="relative">
            <select 
              v-model="sortBy" 
              @change="handleSortChange"
              class="appearance-none bg-white border border-gray-300 rounded-lg px-4 py-2 pr-8 text-gray-700 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
            >
              <option value="popularity">Most popular first</option>
              <option value="rating">Highest rated</option>
              <option value="newest">Newest first</option>
              <option value="oldest">Oldest first</option>
              <option value="title">A-Z</option>
            </select>
            <ChevronDown class="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-500 pointer-events-none" />
          </div>
          
          <!-- Filter Button -->
          <button 
            @click="showFilters = !showFilters"
            class="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          >
            <Filter class="w-4 h-4" />
            Filter
          </button>
          
          <!-- View Toggle -->
          <div class="flex border border-gray-300 rounded-lg overflow-hidden">
            <button 
              @click="viewMode = 'grid'" 
              :class="[
                'px-3 py-2 transition-colors',
                viewMode === 'grid' 
                  ? 'bg-gray-900 text-white' 
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              ]"
            >
              <Grid class="w-4 h-4" />
            </button>
            <button 
              @click="viewMode = 'list'" 
              :class="[
                'px-3 py-2 transition-colors border-l border-gray-300',
                viewMode === 'list' 
                  ? 'bg-gray-900 text-white' 
                  : 'bg-white text-gray-700 hover:bg-gray-50'
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
            class="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow duration-200"
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
                  <h3 class="text-xl font-bold text-gray-900">{{ movie.title }}</h3>
                  <div class="flex items-center gap-1">
                    <span class="text-orange-500 font-semibold">{{ movie.lemonPieRating.toFixed(1) }}</span>
                    <span class="text-gray-500">/5</span>
                  </div>
                </div>
                <p class="text-gray-600 mb-3">{{ movie.releaseDate }} • {{ movie.genre.join(', ') }}</p>
                <p class="text-gray-700 mb-4 line-clamp-2">{{ movie.plotSummary }}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                  <span 
                    v-for="actor in movie.cast.slice(0, 3)" 
                    :key="actor" 
                    class="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm"
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

        <!-- Pagination -->
        <div class="flex justify-center mt-12" v-if="totalPages > 1">
          <div class="flex gap-2">
            <button 
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-colors border',
                currentPage === 1
                  ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              ]"
            >
              <ChevronLeft class="w-4 h-4" />
            </button>
            
            <button 
              v-for="page in visiblePages" 
              :key="page"
              @click="currentPage = page"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-colors border',
                currentPage === page
                  ? 'bg-orange-500 text-white border-orange-500'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              ]"
            >
              {{ page }}
            </button>
            
            <button 
              @click="currentPage = Math.min(totalPages, currentPage + 1)"
              :disabled="currentPage === totalPages"
              :class="[
                'px-4 py-2 rounded-lg font-medium transition-colors border',
                currentPage === totalPages
                  ? 'bg-gray-100 text-gray-400 border-gray-200 cursor-not-allowed'
                  : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
              ]"
            >
              <ChevronRight class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else class="text-center py-16 bg-gray-50 rounded-lg border border-gray-200">
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
import { ref, computed, onMounted, watch } from 'vue'
import { Filter, Search, RotateCcw, Grid, List, ChevronLeft, ChevronRight, ChevronDown } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useSearchStore } from '@/stores/searchStore'
import { useUIStore } from '@/stores/uiStore'
import MovieCard from '@/components/ui/MovieCard.vue'
import SearchFilters from '@/components/sections/search/SearchFilters.vue'
import MovieGrid from '@/components/sections/browse/MovieGrid.vue'

const movieStore = useMovieStore()
const searchStore = useSearchStore()
const uiStore = useUIStore()

// Local reactive data
const viewMode = ref('grid')
const currentPage = ref(1)
const itemsPerPage = 12
const showFilters = ref(false)
const sortBy = ref('popularity')

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

const handleSortChange = () => {
  // Sort functionality can be implemented here
  // For now, just reset to first page
  currentPage.value = 1
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