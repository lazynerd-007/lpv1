<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50">
    <!-- Header Section -->
    <div class="bg-gradient-to-r from-yellow-400 to-orange-500 py-12">
      <div class="container mx-auto px-4">
        <h1 class="text-4xl font-bold text-white mb-4">Browse Nollywood Movies</h1>
        <p class="text-xl text-yellow-100">Discover the best of Nigerian cinema</p>
      </div>
    </div>

    <!-- Filters Section -->
    <div class="container mx-auto px-4 py-8">
      <div class="card bg-white shadow-lg mb-8">
        <div class="card-body">
          <h2 class="card-title text-2xl mb-6 text-gray-800">
            <Filter class="w-6 h-6" />
            Filter Movies
          </h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <!-- Search -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Search Movies</span>
              </label>
              <div class="input-group">
                <input 
                  v-model="searchQuery" 
                  type="text" 
                  placeholder="Search by title, cast, or director..." 
                  class="input input-bordered flex-1"
                />
                <button class="btn btn-square btn-primary">
                  <Search class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Genre Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Genre</span>
              </label>
              <select v-model="selectedGenre" class="select select-bordered">
                <option value="">All Genres</option>
                <option v-for="genre in genres" :key="genre" :value="genre">
                  {{ genre }}
                </option>
              </select>
            </div>

            <!-- Year Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Release Year</span>
              </label>
              <select v-model="selectedYear" class="select select-bordered">
                <option value="">All Years</option>
                <option v-for="year in years" :key="year" :value="year">
                  {{ year }}
                </option>
              </select>
            </div>

            <!-- Rating Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Minimum Rating</span>
              </label>
              <select v-model="minRating" class="select select-bordered">
                <option value="0">Any Rating</option>
                <option value="6">🥧 Pies Only (6+)</option>
                <option value="8">🥧 Great Pies (8+)</option>
                <option value="9">🥧 Masterpieces (9+)</option>
              </select>
            </div>
          </div>

          <!-- Sort Options -->
          <div class="flex flex-wrap gap-4 mt-6">
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Sort By</span>
              </label>
              <select v-model="sortBy" class="select select-bordered">
                <option value="title">Title (A-Z)</option>
                <option value="year">Release Year</option>
                <option value="rating">Rating</option>
                <option value="reviews">Most Reviewed</option>
              </select>
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Order</span>
              </label>
              <select v-model="sortOrder" class="select select-bordered">
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>

            <div class="form-control">
              <label class="label">
                <span class="label-text">&nbsp;</span>
              </label>
              <button @click="clearFilters" class="btn btn-outline btn-warning">
                <RotateCcw class="w-4 h-4 mr-2" />
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Results Summary -->
      <div class="flex justify-between items-center mb-6">
        <div class="text-lg font-semibold text-gray-700">
          Showing {{ filteredMovies.length }} of {{ mockMovies.length }} movies
        </div>
        <div class="flex gap-2">
          <button 
            @click="viewMode = 'grid'" 
            :class="['btn btn-sm', viewMode === 'grid' ? 'btn-primary' : 'btn-outline']"
          >
            <Grid class="w-4 h-4" />
          </button>
          <button 
            @click="viewMode = 'list'" 
            :class="['btn btn-sm', viewMode === 'list' ? 'btn-primary' : 'btn-outline']"
          >
            <List class="w-4 h-4" />
          </button>
        </div>
      </div>

      <!-- Movies Grid/List -->
      <div v-if="filteredMovies.length > 0">
        <!-- Grid View -->
        <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <MovieCard 
            v-for="movie in paginatedMovies" 
            :key="movie.id" 
            :movie="movie" 
            class="transform hover:scale-105 transition-transform duration-200"
          />
        </div>

        <!-- List View -->
        <div v-else class="space-y-4">
          <div 
            v-for="movie in paginatedMovies" 
            :key="movie.id" 
            class="card bg-white shadow-lg hover:shadow-xl transition-shadow duration-200"
          >
            <div class="card-body">
              <div class="flex flex-col md:flex-row gap-4">
                <div class="flex-shrink-0">
                  <img 
                    :src="movie.poster" 
                    :alt="movie.title" 
                    class="w-24 h-36 object-cover rounded-lg"
                  />
                </div>
                <div class="flex-1">
                  <div class="flex justify-between items-start mb-2">
                    <h3 class="card-title text-xl">{{ movie.title }}</h3>
                    <LemonPieRating :rating="movie.lemonPieRating" size="sm" />
                  </div>
                  <p class="text-gray-600 mb-2">{{ movie.year }} • {{ movie.genre }}</p>
                  <p class="text-gray-700 mb-3 line-clamp-2">{{ movie.plot }}</p>
                  <div class="flex flex-wrap gap-2 mb-3">
                    <span 
                      v-for="actor in movie.cast.slice(0, 3)" 
                      :key="actor" 
                      class="badge badge-outline"
                    >
                      {{ actor }}
                    </span>
                  </div>
                  <div class="flex justify-between items-center">
                    <div class="text-sm text-gray-500">
                      {{ movie.reviews.length }} review{{ movie.reviews.length !== 1 ? 's' : '' }}
                    </div>
                    <router-link 
                      :to="`/movie/${movie.id}`" 
                      class="btn btn-primary btn-sm"
                    >
                      View Details
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Pagination -->
        <div class="flex justify-center mt-12" v-if="totalPages > 1">
          <div class="btn-group">
            <button 
              @click="currentPage = Math.max(1, currentPage - 1)"
              :disabled="currentPage === 1"
              class="btn"
            >
              <ChevronLeft class="w-4 h-4" />
            </button>
            
            <button 
              v-for="page in visiblePages" 
              :key="page"
              @click="currentPage = page"
              :class="['btn', currentPage === page ? 'btn-active' : '']"
            >
              {{ page }}
            </button>
            
            <button 
              @click="currentPage = Math.min(totalPages, currentPage + 1)"
              :disabled="currentPage === totalPages"
              class="btn"
            >
              <ChevronRight class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- No Results -->
      <div v-else class="text-center py-16">
        <div class="text-6xl mb-4">🔍</div>
        <h3 class="text-2xl font-bold text-gray-700 mb-2">No movies found</h3>
        <p class="text-gray-500 mb-6">Try adjusting your filters or search terms</p>
        <button @click="clearFilters" class="btn btn-primary">
          Clear All Filters
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Filter, Search, RotateCcw, Grid, List, ChevronLeft, ChevronRight } from 'lucide-vue-next'
import MovieCard from '@/components/MovieCard.vue'
import LemonPieRating from '@/components/LemonPieRating.vue'
import { mockMovies } from '@/data/mockMovies'
import type { Movie } from '@/data/mockMovies'

// Reactive data
const searchQuery = ref('')
const selectedGenre = ref('')
const selectedYear = ref('')
const minRating = ref(0)
const sortBy = ref('title')
const sortOrder = ref('asc')
const viewMode = ref('grid')
const currentPage = ref(1)
const itemsPerPage = 12

// Computed properties
const genres = computed(() => {
  const allGenres = mockMovies.map(movie => movie.genre)
  return [...new Set(allGenres)].sort()
})

const years = computed(() => {
  const allYears = mockMovies.map(movie => movie.year)
  return [...new Set(allYears)].sort((a, b) => b - a)
})

const filteredMovies = computed(() => {
  let filtered = mockMovies.filter(movie => {
    const matchesSearch = !searchQuery.value || 
      movie.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      movie.cast.some(actor => actor.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      movie.director.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesGenre = !selectedGenre.value || movie.genre === selectedGenre.value
    const matchesYear = !selectedYear.value || movie.year === parseInt(selectedYear.value)
    const matchesRating = movie.lemonPieRating >= minRating.value
    
    return matchesSearch && matchesGenre && matchesYear && matchesRating
  })

  // Sort movies
  filtered.sort((a, b) => {
    let aValue: any, bValue: any
    
    switch (sortBy.value) {
      case 'title':
        aValue = a.title.toLowerCase()
        bValue = b.title.toLowerCase()
        break
      case 'year':
        aValue = a.year
        bValue = b.year
        break
      case 'rating':
        aValue = a.lemonPieRating
        bValue = b.lemonPieRating
        break
      case 'reviews':
        aValue = a.reviews.length
        bValue = b.reviews.length
        break
      default:
        return 0
    }
    
    if (sortOrder.value === 'desc') {
      return aValue < bValue ? 1 : aValue > bValue ? -1 : 0
    } else {
      return aValue > bValue ? 1 : aValue < bValue ? -1 : 0
    }
  })

  return filtered
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
  searchQuery.value = ''
  selectedGenre.value = ''
  selectedYear.value = ''
  minRating.value = 0
  sortBy.value = 'title'
  sortOrder.value = 'asc'
  currentPage.value = 1
}

// Watch for filter changes to reset pagination
const resetPagination = () => {
  currentPage.value = 1
}

// Set page title
onMounted(() => {
  document.title = 'Browse Movies - LemonNPie'
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