<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <router-link to="/admin" class="text-slate-500 hover:text-slate-700 mr-4">
              <ArrowLeft class="w-5 h-5" />
            </router-link>
            <h1 class="text-2xl font-bold text-slate-900">Content Management</h1>
          </div>
          <div class="flex items-center space-x-4">
            <router-link
              to="/admin/content/add"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
            >
              <Plus class="w-4 h-4 mr-2" />
              Add Content
            </router-link>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-4 mb-6">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Film class="h-6 w-6 text-blue-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Total Movies</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ totalMovies }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Tv class="h-6 w-6 text-green-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Total Series</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ totalSeries }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Clock class="h-6 w-6 text-yellow-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Pending Approval</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ pendingApproval }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <TrendingUp class="h-6 w-6 text-purple-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Added This Month</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ addedThisMonth }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Search and Filters -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-5">
            <!-- Search -->
            <div class="sm:col-span-2">
              <label for="search" class="block text-sm font-medium text-slate-700 mb-2">
                Search Content
              </label>
              <div class="relative">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  id="search"
                  v-model="searchTerm"
                  type="text"
                  placeholder="Search by title, genre, or director..."
                  class="block w-full pl-10 pr-3 py-2 border border-slate-300 rounded-md leading-5 bg-white placeholder-slate-500 focus:outline-none focus:placeholder-slate-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                  @input="debouncedSearch"
                />
              </div>
            </div>

            <!-- Type Filter -->
            <div>
              <label for="type-filter" class="block text-sm font-medium text-slate-700 mb-2">
                Type
              </label>
              <select
                id="type-filter"
                v-model="selectedType"
                @change="applyFilters"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Types</option>
                <option value="movie">Movies</option>
                <option value="series">Series</option>
              </select>
            </div>

            <!-- Genre Filter -->
            <div>
              <label for="genre-filter" class="block text-sm font-medium text-slate-700 mb-2">
                Genre
              </label>
              <select
                id="genre-filter"
                v-model="selectedGenre"
                @change="applyFilters"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Genres</option>
                <option value="action">Action</option>
                <option value="comedy">Comedy</option>
                <option value="drama">Drama</option>
                <option value="horror">Horror</option>
                <option value="sci-fi">Sci-Fi</option>
                <option value="thriller">Thriller</option>
              </select>
            </div>

            <!-- Status Filter -->
            <div>
              <label for="status-filter" class="block text-sm font-medium text-slate-700 mb-2">
                Status
              </label>
              <select
                id="status-filter"
                v-model="selectedStatus"
                @change="applyFilters"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Status</option>
                <option value="published">Published</option>
                <option value="draft">Draft</option>
                <option value="pending">Pending</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Grid -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg leading-6 font-medium text-slate-900">
              Content Library ({{ contentItems.length }})
            </h3>
            <div class="flex items-center space-x-2">
              <button
                @click="viewMode = 'grid'"
                :class="[
                  'p-2 rounded-md',
                  viewMode === 'grid' ? 'bg-blue-100 text-blue-600' : 'text-slate-400 hover:text-slate-600'
                ]"
              >
                <Grid class="w-4 h-4" />
              </button>
              <button
                @click="viewMode = 'list'"
                :class="[
                  'p-2 rounded-md',
                  viewMode === 'list' ? 'bg-blue-100 text-blue-600' : 'text-slate-400 hover:text-slate-600'
                ]"
              >
                <List class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="isLoading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>

          <!-- Grid View -->
          <div v-else-if="viewMode === 'grid'" class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
            <div
              v-for="item in contentItems"
              :key="item.id"
              class="bg-white border border-slate-200 rounded-lg overflow-hidden hover:shadow-md transition-shadow"
            >
              <div class="aspect-w-3 aspect-h-4">
                <img
                  :src="item.poster"
                  :alt="item.title"
                  class="w-full h-48 object-cover"
                />
              </div>
              <div class="p-4">
                <div class="flex items-center justify-between mb-2">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getTypeBadgeClass(item.type)"
                  >
                    {{ item.type }}
                  </span>
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getStatusBadgeClass(item.status)"
                  >
                    {{ item.status }}
                  </span>
                </div>
                <h3 class="text-sm font-medium text-slate-900 mb-1 truncate">{{ item.title }}</h3>
                <p class="text-xs text-slate-500 mb-2">{{ item.year }} • {{ item.genre }}</p>
                <p class="text-xs text-slate-600 mb-3 line-clamp-2">{{ item.description }}</p>
                <div class="flex items-center justify-between">
                  <div class="flex items-center text-xs text-slate-500">
                    <Star class="w-3 h-3 mr-1 text-yellow-400" />
                    {{ item.rating }}
                  </div>
                  <div class="flex items-center space-x-1">
                    <router-link
                      :to="`/admin/content/edit/${item.id}`"
                      class="p-1 text-slate-400 hover:text-slate-600"
                    >
                      <Edit class="w-3 h-3" />
                    </router-link>
                    <button
                      @click="deleteContent(item)"
                      class="p-1 text-red-400 hover:text-red-600"
                    >
                      <Trash2 class="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- List View -->
          <div v-else class="overflow-hidden">
            <table class="min-w-full divide-y divide-slate-200">
              <thead class="bg-slate-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Content
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Genre
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Rating
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Added
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-slate-200">
                <tr v-for="item in contentItems" :key="item.id" class="hover:bg-slate-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-12 w-8">
                        <img
                          :src="item.poster"
                          :alt="item.title"
                          class="h-12 w-8 object-cover rounded"
                        />
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-slate-900">{{ item.title }}</div>
                        <div class="text-sm text-slate-500">{{ item.year }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getTypeBadgeClass(item.type)"
                    >
                      {{ item.type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                    {{ item.genre }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                    <div class="flex items-center">
                      <Star class="w-4 h-4 mr-1 text-yellow-400" />
                      {{ item.rating }}
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getStatusBadgeClass(item.status)"
                    >
                      {{ item.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {{ formatDate(item.createdAt) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                      <router-link
                        :to="`/admin/content/edit/${item.id}`"
                        class="text-blue-600 hover:text-blue-900"
                      >
                        <Edit class="w-4 h-4" />
                      </router-link>
                      <button
                        @click="deleteContent(item)"
                        class="text-red-600 hover:text-red-900"
                      >
                        <Trash2 class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="totalPages > 1" class="bg-white px-4 py-3 flex items-center justify-between border-t border-slate-200 sm:px-6">
            <div class="flex-1 flex justify-between sm:hidden">
              <button
                @click="prevPage"
                :disabled="!hasPrevPage"
                class="relative inline-flex items-center px-4 py-2 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Previous
              </button>
              <button
                @click="nextPage"
                :disabled="!hasNextPage"
                class="ml-3 relative inline-flex items-center px-4 py-2 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Next
              </button>
            </div>
            <div class="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
              <div class="flex items-center space-x-4">
                <p class="text-sm text-slate-700">
                  Showing
                  <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}</span>
                  to
                  <span class="font-medium">{{ Math.min(currentPage * itemsPerPage, totalItems) }}</span>
                  of
                  <span class="font-medium">{{ totalItems }}</span>
                  results
                </p>
                <div class="flex items-center space-x-2">
                  <label for="itemsPerPage" class="text-sm text-slate-700">Items per page:</label>
                  <select
                    id="itemsPerPage"
                    :value="itemsPerPage"
                    @change="changeItemsPerPage(parseInt(($event.target as HTMLSelectElement).value))"
                    class="border border-slate-300 rounded-md px-2 py-1 text-sm"
                  >
                    <option value="5">5</option>
                    <option value="10">10</option>
                    <option value="20">20</option>
                    <option value="50">50</option>
                  </select>
                </div>
              </div>
              <div>
                <nav class="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                  <button
                    @click="prevPage"
                    :disabled="!hasPrevPage"
                    class="relative inline-flex items-center px-2 py-2 rounded-l-md border border-slate-300 bg-white text-sm font-medium text-slate-500 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span class="sr-only">Previous</span>
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
                    </svg>
                  </button>
                  
                  <!-- Page numbers -->
                  <template v-for="page in Math.min(totalPages, 7)" :key="page">
                    <button
                      v-if="page === 1 || page === totalPages || (page >= currentPage - 2 && page <= currentPage + 2)"
                      @click="goToPage(page)"
                      :class="[
                        'relative inline-flex items-center px-4 py-2 border text-sm font-medium',
                        page === currentPage
                          ? 'z-10 bg-blue-50 border-blue-500 text-blue-600'
                          : 'bg-white border-slate-300 text-slate-500 hover:bg-slate-50'
                      ]"
                    >
                      {{ page }}
                    </button>
                    <span
                      v-else-if="page === currentPage - 3 || page === currentPage + 3"
                      class="relative inline-flex items-center px-4 py-2 border border-slate-300 bg-white text-sm font-medium text-slate-700"
                    >
                      ...
                    </span>
                  </template>
                  
                  <button
                    @click="nextPage"
                    :disabled="!hasNextPage"
                    class="relative inline-flex items-center px-2 py-2 rounded-r-md border border-slate-300 bg-white text-sm font-medium text-slate-500 hover:bg-slate-50 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span class="sr-only">Next</span>
                    <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
                    </svg>
                  </button>
                </nav>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="contentItems.length === 0 && !isLoading" class="text-center py-8">
            <Film class="mx-auto h-12 w-12 text-slate-400" />
            <h3 class="mt-2 text-sm font-medium text-slate-900">No content found</h3>
            <p class="mt-1 text-sm text-slate-500">
              Get started by adding your first movie or series.
            </p>
            <div class="mt-6">
              <router-link
                to="/admin/content/add"
                class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                <Plus class="w-4 h-4 mr-2" />
                Add Content
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  ArrowLeft,
  Plus,
  Film,
  Tv,
  Clock,
  TrendingUp,
  Search,
  Grid,
  List,
  Star,
  Edit,
  Trash2
} from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import type { Movie } from '@/data/mockMovies'

const movieStore = useMovieStore()

// State
const searchTerm = ref('')
const selectedType = ref('')
const selectedGenre = ref('')
const selectedStatus = ref('')
const viewMode = ref<'grid' | 'list'>('grid')
const isLoading = ref(false)

// Pagination state
const currentPage = ref(1)
const itemsPerPage = ref(10)

// Transform movies to match the admin content format
const allContentItems = computed(() => {
  return movieStore.movies.map((movie: Movie) => ({
    id: movie.id,
    title: movie.title,
    type: 'movie',
    genre: movie.genre.join(', '),
    rating: movie.lemonPieRating,
    status: 'published', // All movies are published for now
    createdAt: movie.releaseDate,
    poster: movie.poster,
    description: movie.plot,
    director: movie.director,
    year: new Date(movie.releaseDate).getFullYear()
  }))
})

// Filtered content items based on current filters (without pagination)
const filteredContentItems = computed(() => {
  let filteredMovies = movieStore.movies

  // Apply search filter
  if (searchTerm.value.trim()) {
    filteredMovies = movieStore.searchMovies(searchTerm.value)
  }

  // Apply genre filter
  if (selectedGenre.value && selectedGenre.value !== 'all') {
    filteredMovies = filteredMovies.filter(movie => 
      movie.genre.some(g => g.toLowerCase() === selectedGenre.value.toLowerCase())
    )
  }

  // Transform filtered movies to admin content format
  return filteredMovies.map((movie: Movie) => ({
    id: movie.id,
    title: movie.title,
    type: 'movie',
    genre: movie.genre.join(', '),
    rating: movie.lemonPieRating,
    status: 'published',
    createdAt: movie.releaseDate,
    poster: movie.poster,
    description: movie.plot,
    director: movie.director,
    year: new Date(movie.releaseDate).getFullYear()
  }))
})

// Paginated content items
const contentItems = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage.value
  const endIndex = startIndex + itemsPerPage.value
  return filteredContentItems.value.slice(startIndex, endIndex)
})

// Pagination computed properties
const totalItems = computed(() => filteredContentItems.value.length)
const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))
const hasNextPage = computed(() => currentPage.value < totalPages.value)
const hasPrevPage = computed(() => currentPage.value > 1)

// Computed
const totalMovies = computed(() => 
  allContentItems.value.filter(item => item.type === 'movie').length
)

const totalSeries = computed(() => 
  allContentItems.value.filter(item => item.type === 'series').length
)

const pendingApproval = computed(() => 
  allContentItems.value.filter(item => item.status === 'pending').length
)

const addedThisMonth = computed(() => 15) // Mock data

// Methods
const debouncedSearch = (() => {
  let timeout: NodeJS.Timeout
  return () => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      applyFilters()
    }, 300)
  }
})()

const applyFilters = () => {
  // Reset to first page when filters change
  currentPage.value = 1
  // Filtering is now handled by the computed property
  // This function is kept for compatibility and logging
  console.log('Applied filters:', {
    search: searchTerm.value,
    type: selectedType.value,
    genre: selectedGenre.value,
    status: selectedStatus.value,
    resultCount: filteredContentItems.value.length,
    totalPages: totalPages.value
  })
}

// Pagination methods
const goToPage = (page: number) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const nextPage = () => {
  if (hasNextPage.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (hasPrevPage.value) {
    currentPage.value--
  }
}

const changeItemsPerPage = (newItemsPerPage: number) => {
  itemsPerPage.value = newItemsPerPage
  currentPage.value = 1 // Reset to first page
}

const deleteContent = (item: any) => {
  if (confirm(`Are you sure you want to delete "${item.title}"?`)) {
    // Find the movie in the store and remove it
    const movieIndex = movieStore.movies.findIndex(m => m.id === item.id)
    if (movieIndex !== -1) {
      movieStore.movies.splice(movieIndex, 1)
      console.log(`Deleted movie: ${item.title}`)
    }
  }
}

const getTypeBadgeClass = (type: string) => {
  const classes = {
    movie: 'bg-blue-100 text-blue-800',
    series: 'bg-green-100 text-green-800'
  }
  return classes[type as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const getStatusBadgeClass = (status: string) => {
  const classes = {
    published: 'bg-green-100 text-green-800',
    draft: 'bg-yellow-100 text-yellow-800',
    pending: 'bg-orange-100 text-orange-800'
  }
  return classes[status as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

// Lifecycle
onMounted(() => {
  // Load content data
  applyFilters()
})
</script>