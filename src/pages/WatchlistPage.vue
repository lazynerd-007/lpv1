<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <!-- Header Section -->
    <div class="bg-gradient-to-r from-yellow-600 to-orange-600 py-12">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h1 class="text-4xl md:text-5xl font-bold mb-2">My Watchlist</h1>
            <p class="text-yellow-100 text-lg">
              {{ watchlistMovies.length }} {{ watchlistMovies.length === 1 ? 'item' : 'items' }} saved for later
            </p>
          </div>
          <div class="mt-4 md:mt-0 flex items-center space-x-4">
            <!-- View Toggle -->
            <div class="flex bg-black bg-opacity-30 rounded-lg p-1">
              <button
                @click="viewMode = 'grid'"
                :class="[
                  'px-3 py-2 rounded-md transition-colors',
                  viewMode === 'grid' ? 'bg-white text-gray-900' : 'text-white hover:bg-white hover:bg-opacity-20'
                ]"
              >
                <Grid3X3 class="w-5 h-5" />
              </button>
              <button
                @click="viewMode = 'list'"
                :class="[
                  'px-3 py-2 rounded-md transition-colors',
                  viewMode === 'list' ? 'bg-white text-gray-900' : 'text-white hover:bg-white hover:bg-opacity-20'
                ]"
              >
                <List class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <!-- Controls Section -->
      <div class="mb-8">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <!-- Search and Filter -->
          <div class="flex flex-col sm:flex-row gap-4 flex-1">
            <!-- Search -->
            <div class="relative flex-1 max-w-md">
              <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search your watchlist..."
                class="w-full pl-10 pr-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-yellow-500 focus:border-transparent text-white placeholder-gray-400"
              />
            </div>
            
            <!-- Filter Dropdown -->
            <div class="relative">
              <select
                v-model="selectedFilter"
                class="appearance-none bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 pr-10 text-white focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
              >
                <option value="all">All Items</option>
                <option value="movies">Movies Only</option>
                <option value="series">Series Only</option>
                <option value="recent">Recently Added</option>
              </select>
              <ChevronDown class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 pointer-events-none" />
            </div>
            
            <!-- Genre Filter -->
            <div class="relative">
              <select
                v-model="selectedGenre"
                class="appearance-none bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 pr-10 text-white focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
              >
                <option value="">All Genres</option>
                <option v-for="genre in availableGenres" :key="genre" :value="genre">
                  {{ genre }}
                </option>
              </select>
              <ChevronDown class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5 pointer-events-none" />
            </div>
          </div>

          <!-- Sort Options -->
          <div class="flex items-center gap-4">
            <span class="text-gray-400 text-sm">Sort by:</span>
            <select
              v-model="sortBy"
              class="appearance-none bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 pr-10 text-white focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
            >
              <option value="dateAdded">Date Added</option>
              <option value="title">Title (A-Z)</option>
              <option value="rating">Rating</option>
              <option value="year">Release Year</option>
            </select>
            <button
              @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'"
              class="p-2 bg-gray-800 border border-gray-700 rounded-lg hover:bg-gray-700 transition-colors"
              :title="sortOrder === 'asc' ? 'Sort Descending' : 'Sort Ascending'"
            >
              <ArrowUpDown class="w-5 h-5" :class="sortOrder === 'desc' ? 'rotate-180' : ''" />
            </button>
          </div>
        </div>
      </div>

      <!-- Results Info -->
      <div class="mb-6">
        <p class="text-gray-400">
          Showing {{ filteredAndSortedMovies.length }} of {{ watchlistMovies.length }} items
          <span v-if="searchQuery || selectedFilter !== 'all'" class="ml-2">
            <button
              @click="clearFilters"
              class="text-yellow-500 hover:text-yellow-400 underline"
            >
              Clear filters
            </button>
          </span>
        </p>
      </div>

      <!-- Watchlist Content -->
      <div v-if="filteredAndSortedMovies.length > 0">
        <!-- Grid View -->
        <div v-if="viewMode === 'grid'" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-6">
          <div
            v-for="movie in filteredAndSortedMovies"
            :key="movie.id"
            class="group relative bg-gray-800 rounded-lg overflow-hidden hover:bg-gray-750 transition-all duration-300 hover:scale-105 cursor-pointer"
            @click="goToDetails(movie.id)"
          >
            <!-- Movie Poster -->
            <div class="relative aspect-[2/3] overflow-hidden">
              <img
                :src="movie.posterUrl"
                :alt="movie.title"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                loading="lazy"
              />
              
              <!-- Rating Badge -->
              <div class="absolute top-2 left-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-sm font-bold">
                <span class="mr-1">{{ getRatingIcon(movie.lemonPieRating) }}</span>
                <span :class="getRatingColor(movie.lemonPieRating)">{{ movie.lemonPieRating.toFixed(1) }}</span>
              </div>
              
              <!-- Status Badge -->
              <div :class="`absolute top-2 right-2 px-2 py-1 rounded text-xs font-medium ${getStatusBadgeColor(movie.productionState)}`">
                {{ movie.productionState }}
              </div>
              
              <!-- Overlay Actions -->
              <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 flex items-center justify-center">
                <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex space-x-3">
                  <button
                    v-if="movie.trailerUrl"
                    @click.stop="playTrailer(movie)"
                    class="bg-yellow-500 hover:bg-yellow-600 text-black p-3 rounded-full transition-colors"
                    title="Play Trailer"
                  >
                    <Play class="w-5 h-5" />
                  </button>
                  <button
                    @click.stop="removeFromWatchlist(movie.id)"
                    class="bg-red-500 hover:bg-red-600 text-white p-3 rounded-full transition-colors"
                    title="Remove from Watchlist"
                  >
                    <Trash2 class="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Movie Info -->
            <div class="p-4">
              <h3 class="font-semibold text-white mb-1 line-clamp-2 group-hover:text-yellow-400 transition-colors" :title="movie.title">
                {{ movie.title }}
              </h3>
              <p class="text-gray-400 text-sm mb-2">{{ formatDate(movie.releaseDate) }} • {{ formatRuntime(movie.runtime) }}</p>
              <p class="text-gray-300 text-sm mb-2">{{ movie.genre.slice(0, 3).join(', ') }}</p>
              <div class="flex items-center justify-between">
                <div class="flex items-center space-x-1">
                  <Star class="w-4 h-4 text-yellow-500 fill-current" />
                  <span class="text-sm text-gray-300">{{ movie.lemonPieRating.toFixed(1) }}</span>
                  <span class="text-gray-500 text-xs">({{ movie.reviewCount }})</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- List View -->
        <div v-else class="space-y-4">
          <div
            v-for="movie in filteredAndSortedMovies"
            :key="movie.id"
            class="bg-gray-800 rounded-lg p-4 hover:bg-gray-750 transition-colors group cursor-pointer"
            @click="goToDetails(movie.id)"
          >
            <div class="flex items-center space-x-4">
              <!-- Poster Thumbnail -->
              <div class="flex-shrink-0 relative">
                <img
                  :src="movie.posterUrl"
                  :alt="movie.title"
                  class="w-16 h-24 object-cover rounded"
                  loading="lazy"
                />
                <!-- Rating Badge -->
                <div class="absolute -top-2 -right-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded text-xs font-bold">
                  <span class="mr-1">{{ getRatingIcon(movie.lemonPieRating) }}</span>
                  <span :class="getRatingColor(movie.lemonPieRating)">{{ movie.lemonPieRating.toFixed(1) }}</span>
                </div>
              </div>
              
              <!-- Movie Details -->
              <div class="flex-1 min-w-0">
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="flex items-center space-x-2 mb-1">
                      <h3 class="text-lg font-semibold text-white group-hover:text-yellow-400 transition-colors">
                        {{ movie.title }}
                      </h3>
                      <span :class="`px-2 py-1 rounded text-xs font-medium ${getStatusBadgeColor(movie.productionState)}`">
                        {{ movie.productionState }}
                      </span>
                    </div>
                    <p class="text-gray-400 text-sm mb-2">{{ formatDate(movie.releaseDate) }} • {{ formatRuntime(movie.runtime) }} • {{ movie.director }}</p>
                    <p class="text-gray-300 text-sm mb-2">{{ movie.genre.join(', ') }}</p>
                    <p class="text-gray-300 text-sm line-clamp-2">{{ movie.plotSummary }}</p>
                  </div>
                  
                  <!-- Actions -->
                  <div class="flex items-center space-x-2 ml-4">
                    <div class="flex items-center space-x-1">
                      <Star class="w-4 h-4 text-yellow-500 fill-current" />
                      <span class="text-sm text-gray-300">{{ movie.lemonPieRating.toFixed(1) }}</span>
                      <span class="text-gray-500 text-xs">({{ movie.reviewCount }})</span>
                    </div>
                    <button
                      v-if="movie.trailerUrl"
                      @click.stop="playTrailer(movie)"
                      class="bg-yellow-500 hover:bg-yellow-600 text-black p-2 rounded transition-colors"
                      title="Play Trailer"
                    >
                      <Play class="w-4 h-4" />
                    </button>
                    <button
                      @click.stop="removeFromWatchlist(movie.id)"
                      class="bg-red-500 hover:bg-red-600 text-white p-2 rounded transition-colors"
                      title="Remove from Watchlist"
                    >
                      <Trash2 class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-16">
        <div class="max-w-md mx-auto">
          <div class="mb-6">
            <Heart class="w-24 h-24 text-gray-600 mx-auto mb-4" />
          </div>
          <h3 class="text-2xl font-bold text-white mb-4">
            {{ searchQuery || selectedFilter !== 'all' ? 'No matches found' : 'Your watchlist is empty' }}
          </h3>
          <p class="text-gray-400 mb-8">
            {{ searchQuery || selectedFilter !== 'all' 
              ? 'Try adjusting your search or filter criteria.' 
              : 'Start building your watchlist by adding movies and series you want to watch later.' 
            }}
          </p>
          <div class="space-y-4">
            <button
              v-if="searchQuery || selectedFilter !== 'all'"
              @click="clearFilters"
              class="bg-yellow-500 hover:bg-yellow-600 text-black px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              Clear Filters
            </button>
            <router-link
              to="/browse/movies"
              class="inline-block bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
            >
              Browse Movies
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import { useMovieStore } from '@/stores/movieStore'
import {
  Search,
  Grid3X3,
  List,
  ChevronDown,
  ArrowUpDown,
  Star,
  Heart,
  X,
  Play,
  Calendar,
  Clock,
  Trash2
} from 'lucide-vue-next'
import type { Movie } from '@/data/mockMovies'

// Stores
const userStore = useUserStore()
const uiStore = useUIStore()
const movieStore = useMovieStore()
const router = useRouter()

// Reactive state
const viewMode = ref<'grid' | 'list'>('grid')
const searchQuery = ref('')
const selectedFilter = ref('all')
const selectedGenre = ref('')
const sortBy = ref('dateAdded')
const sortOrder = ref<'asc' | 'desc'>('desc')

// Computed properties
const watchlistMovies = computed(() => userStore.watchlistMovies)

const availableGenres = computed(() => {
  const genres = new Set<string>()
  watchlistMovies.value.forEach(movie => {
    movie.genre.forEach(g => genres.add(g))
  })
  return Array.from(genres).sort()
})

const filteredAndSortedMovies = computed(() => {
  let filtered = watchlistMovies.value

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(movie => 
      movie.title.toLowerCase().includes(query) ||
      movie.localTitle?.toLowerCase().includes(query) ||
      movie.director.toLowerCase().includes(query) ||
      movie.cast.some(actor => actor.toLowerCase().includes(query)) ||
      movie.genre.some(g => g.toLowerCase().includes(query)) ||
      movie.plotSummary.toLowerCase().includes(query)
    )
  }

  // Apply category filter
  if (selectedFilter.value !== 'all') {
    switch (selectedFilter.value) {
      case 'movies':
        // All items in watchlist are movies, so no filtering needed
        break
      case 'series':
        // No series in current Movie interface, filter to empty array
        filtered = []
        break
      case 'recent':
        // Show items added in the last 30 days (mock implementation)
        // In a real app, you'd track when items were added to watchlist
        break
    }
  }

  // Apply genre filter
  if (selectedGenre.value) {
    filtered = filtered.filter(movie => 
      movie.genre.includes(selectedGenre.value)
    )
  }

  // Apply sorting
  const sorted = [...filtered].sort((a, b) => {
    let comparison = 0
    
    switch (sortBy.value) {
      case 'title':
        comparison = a.title.localeCompare(b.title)
        break
      case 'rating':
        comparison = b.lemonPieRating - a.lemonPieRating
        break
      case 'year':
        comparison = new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime()
        break
      case 'dateAdded':
      default:
        // Mock date added sorting - in real app, track actual add dates
        comparison = a.id.localeCompare(b.id)
        break
    }
    
    return sortOrder.value === 'asc' ? comparison : -comparison
  })

  return sorted
})

const availableStatuses = computed(() => {
  const statuses = new Set<string>()
  watchlistMovies.value.forEach(movie => {
    statuses.add(movie.productionState)
  })
  return Array.from(statuses).sort()
})

// Methods
const removeFromWatchlist = async (movieId: string) => {
  try {
    await userStore.removeFromWatchlist(movieId)
    uiStore.showSuccessToast('Movie removed from watchlist')
  } catch (error) {
    console.error('Error removing from watchlist:', error)
    uiStore.showErrorToast('Failed to remove movie from watchlist')
  }
}

const goToDetails = (movieId: string) => {
  router.push(`/movie/${movieId}`)
}

const playTrailer = (movie: Movie) => {
  if (movie.trailerUrl) {
    window.open(movie.trailerUrl, '_blank')
  }
}

const getStatusBadgeColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'released':
      return 'bg-green-500 text-white'
    case 'in production':
      return 'bg-blue-500 text-white'
    case 'post-production':
      return 'bg-yellow-500 text-black'
    case 'pre-production':
      return 'bg-purple-500 text-white'
    default:
      return 'bg-gray-500 text-white'
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
}

const formatRuntime = (minutes: number) => {
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`
}

const getRatingIcon = (rating: number) => {
  if (rating >= 8) return '🍋'
  if (rating >= 6) return '🥧'
  return '🍅'
}

const getRatingColor = (rating: number) => {
  if (rating >= 8) return 'text-green-400'
  if (rating >= 6) return 'text-yellow-400'
  return 'text-red-400'
}

const clearFilters = () => {
  searchQuery.value = ''
  selectedFilter.value = 'all'
  selectedGenre.value = ''
  sortBy.value = 'dateAdded'
  sortOrder.value = 'desc'
}

// Lifecycle
onMounted(() => {
  uiStore.setPageTitle('My Watchlist - LemonNPie')
  // Load user data if not already loaded
  if (!userStore.isAuthenticated) {
    userStore.checkAuthStatus()
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.bg-gray-750 {
  background-color: #374151;
}
</style>