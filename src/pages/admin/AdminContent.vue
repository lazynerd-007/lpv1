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

// State
const searchTerm = ref('')
const selectedType = ref('')
const selectedGenre = ref('')
const selectedStatus = ref('')
const viewMode = ref<'grid' | 'list'>('grid')
const isLoading = ref(false)

// Mock data
const contentItems = ref([
  {
    id: '1',
    title: 'The Dark Knight',
    type: 'movie',
    genre: 'Action',
    year: 2008,
    rating: 9.0,
    status: 'published',
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=dark%20knight%20movie%20poster&image_size=portrait_4_3',
    description: 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham...',
    createdAt: '2024-01-10T10:00:00Z'
  },
  {
    id: '2',
    title: 'Breaking Bad',
    type: 'series',
    genre: 'Drama',
    year: 2008,
    rating: 9.5,
    status: 'published',
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=breaking%20bad%20tv%20series%20poster&image_size=portrait_4_3',
    description: 'A high school chemistry teacher diagnosed with inoperable lung cancer...',
    createdAt: '2024-01-08T14:30:00Z'
  },
  {
    id: '3',
    title: 'Inception',
    type: 'movie',
    genre: 'Sci-Fi',
    year: 2010,
    rating: 8.8,
    status: 'draft',
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=inception%20movie%20poster%20dream%20layers&image_size=portrait_4_3',
    description: 'A thief who steals corporate secrets through the use of dream-sharing technology...',
    createdAt: '2024-01-12T09:15:00Z'
  }
])

// Computed
const totalMovies = computed(() => 
  contentItems.value.filter(item => item.type === 'movie').length
)

const totalSeries = computed(() => 
  contentItems.value.filter(item => item.type === 'series').length
)

const pendingApproval = computed(() => 
  contentItems.value.filter(item => item.status === 'pending').length
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
  // TODO: Implement filtering logic
  console.log('Applying filters:', {
    search: searchTerm.value,
    type: selectedType.value,
    genre: selectedGenre.value,
    status: selectedStatus.value
  })
}

const deleteContent = (item: any) => {
  if (confirm(`Are you sure you want to delete "${item.title}"?`)) {
    const index = contentItems.value.findIndex(i => i.id === item.id)
    if (index !== -1) {
      contentItems.value.splice(index, 1)
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