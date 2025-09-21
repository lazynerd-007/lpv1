<template>
  <div class="min-h-screen bg-theme-background">
    <!-- Header Section -->
    <div class="container mx-auto px-2 py-4">
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-3">
          <span class="w-1 h-8 bg-orange-500 rounded"></span>
          <h1 class="text-3xl font-bold text-gray-900">Browse Series</h1>
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
              <option value="seasons">Most seasons</option>
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

      <!-- Series Grid/List -->
      <div v-if="filteredSeries.length > 0">
        <!-- Grid View -->
        <div v-if="viewMode === 'grid'">
          <SeriesGrid 
            :series="displayedSeries"
            :loading="isLoading"
            :current-page="1"
            :show-pagination="false"
          />
        </div>

        <!-- List View -->
        <div v-else class="space-y-4">
          <div 
            v-for="show in displayedSeries" 
            :key="show.id" 
            class="bg-white border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow duration-200"
          >
            <div class="flex flex-col md:flex-row gap-6">
              <div class="flex-shrink-0">
                <img 
                  :src="show.posterUrl" 
                  :alt="show.title" 
                  class="w-24 h-36 object-cover rounded-lg"
                />
              </div>
              <div class="flex-1">
                <div class="flex justify-between items-start mb-3">
                  <h3 class="text-xl font-bold text-gray-900">{{ show.title }}</h3>
                  <div class="flex items-center gap-1">
                    <span class="text-orange-500 font-semibold">{{ show.lemonPieRating.toFixed(1) }}</span>
                    <span class="text-gray-500">/10</span>
                  </div>
                </div>
                <p class="text-gray-600 mb-3">
                  {{ show.releaseDate }} • {{ show.genre.join(', ') }} • 
                  <span :class="getStatusColor(show.status)" class="px-2 py-1 rounded text-xs font-semibold capitalize">
                    {{ show.status }}
                  </span>
                </p>
                <p class="text-gray-700 mb-4 line-clamp-2">{{ show.plotSummary }}</p>
                <div class="flex flex-wrap gap-2 mb-4">
                  <span 
                    v-for="actor in show.cast.slice(0, 3)" 
                    :key="actor" 
                    class="bg-theme-surface text-theme-text px-3 py-1 rounded-full text-sm"
                  >
                    {{ actor }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <div class="text-sm text-gray-500">
                    {{ show.seasons }} Season{{ show.seasons !== 1 ? 's' : '' }} • 
                    {{ show.episodes }} Episodes • 
                    {{ show.language.join(', ') }}
                  </div>
                  <router-link 
                    :to="`/series/${show.id}`" 
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
            <span>Loading more series...</span>
          </div>
        </div>
        
        <!-- End of Results Indicator -->
        <div v-else-if="!canLoadMore && displayedSeries.length > 0" class="text-center mt-8 py-4">
          <p class="text-gray-500">You've reached the end of the series list</p>
        </div>
      </div>

      <!-- No Results -->
      <div v-else class="text-center py-8 bg-theme-section-alt rounded-lg border border-theme-light">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-2xl font-bold text-gray-900 mb-2">No series found</h3>
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
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { Grid, List, ChevronDown } from 'lucide-vue-next'
import { useSeriesStore } from '@/stores/seriesStore'
import { useSearchStore } from '@/stores/searchStore'
import { useUIStore } from '@/stores/uiStore'
import SearchFilters from '@/components/sections/search/SearchFilters.vue'
import SeriesGrid from '@/components/sections/browse/SeriesGrid.vue'

const seriesStore = useSeriesStore()
const searchStore = useSearchStore()
const uiStore = useUIStore()

// Local reactive data
const viewMode = ref('grid')
const itemsPerPage = 12
const showFilters = ref(false)
const sortBy = ref('popularity')
const selectedGenre = ref('')
const displayedSeriesCount = ref(itemsPerPage)
const isLoading = ref(false)
const hasMoreSeries = ref(true)

// Extract unique genres from all series
const genres = computed(() => {
  const genreSet = new Set<string>()
  seriesStore.series.forEach(show => {
    show.genre.forEach(g => genreSet.add(g))
  })
  return Array.from(genreSet).sort()
})

// Computed properties
const filteredSeries = computed(() => {
  // Determine which genre filter to use
  const genreFilter = selectedGenre.value || searchStore.filters.genre
  
  return seriesStore.filterSeries({
    genre: genreFilter,
    year: searchStore.filters.year,
    rating: searchStore.filters.rating,
    language: searchStore.filters.language,
    productionState: searchStore.filters.productionState
  })
})

const displayedSeries = computed(() => {
  return filteredSeries.value.slice(0, displayedSeriesCount.value)
})

const canLoadMore = computed(() => {
  return displayedSeriesCount.value < filteredSeries.value.length
})

// Methods
const clearFilters = () => {
  searchStore.clearFilters()
  selectedGenre.value = ''
  displayedSeriesCount.value = itemsPerPage
  hasMoreSeries.value = true
}

const handleSearch = (query: string) => {
  searchStore.performSearch(query)
  displayedSeriesCount.value = itemsPerPage
  hasMoreSeries.value = true
}

const handleFilterChange = () => {
  displayedSeriesCount.value = itemsPerPage
  hasMoreSeries.value = true
}

const handleGenreChange = () => {
  searchStore.updateFilter('genre', selectedGenre.value)
  displayedSeriesCount.value = itemsPerPage
  hasMoreSeries.value = true
}

const handleSortChange = () => {
  // Sort functionality can be implemented here
  // For now, just reset displayed count
  displayedSeriesCount.value = itemsPerPage
  hasMoreSeries.value = true
}

const loadMoreSeries = () => {
  if (isLoading.value || !canLoadMore.value) return
  
  isLoading.value = true
  
  // Simulate loading delay
  setTimeout(() => {
    displayedSeriesCount.value += itemsPerPage
    isLoading.value = false
    hasMoreSeries.value = canLoadMore.value
  }, 500)
}

const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight
  
  // Load more when user is 200px from bottom
  if (scrollTop + windowHeight >= documentHeight - 200) {
    loadMoreSeries()
  }
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'ongoing':
      return 'bg-green-100 text-green-800'
    case 'completed':
      return 'bg-blue-100 text-blue-800'
    case 'cancelled':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-theme-surface text-theme-text'
  }
}

// Watch for filter changes to reset displayed count
watch(
  () => [searchStore.searchState.query, searchStore.filters],
  (newValue) => {
    displayedSeriesCount.value = itemsPerPage
    hasMoreSeries.value = true
    
    // Sync selectedGenre with searchStore.filters.genre
    if (selectedGenre.value !== searchStore.filters.genre) {
      selectedGenre.value = searchStore.filters.genre || ''
    }
  },
  { deep: true }
)

// Set page title and setup scroll listener
onMounted(async () => {
  uiStore.setPageTitle('Browse Series - Nollywood TV Shows')
  
  // Add scroll event listener for infinite scroll
  window.addEventListener('scroll', handleScroll)
  
  // Series are already loaded from mockTVShows
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
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>