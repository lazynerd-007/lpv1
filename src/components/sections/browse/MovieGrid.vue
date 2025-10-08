<script setup lang="ts">
import { computed } from 'vue'
import { Play, Star, Heart, Bookmark, Eye } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movieStore'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import type { Movie } from '@/data/mockMovies'

interface Props {
  movies: Movie[]
  loading?: boolean
  showPagination?: boolean
  itemsPerPage?: number
  currentPage?: number
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  showPagination: true,
  itemsPerPage: 12,
  currentPage: 1
})

const emit = defineEmits<{
  pageChange: [page: number]
  playTrailer: [movie: Movie]
}>()

const router = useRouter()
const movieStore = useMovieStore()
const userStore = useUserStore()
const uiStore = useUIStore()

const totalPages = computed(() => {
  return Math.ceil(props.movies.length / props.itemsPerPage)
})

const paginatedMovies = computed(() => {
  if (!props.showPagination) return props.movies
  
  const start = (props.currentPage - 1) * props.itemsPerPage
  const end = start + props.itemsPerPage
  return props.movies.slice(start, end)
})

const navigateToMovie = (movie: Movie) => {
  router.push(`/movie/${movie.id}`)
}

const playTrailer = (movie: Movie) => {
  emit('playTrailer', movie)
}

const toggleWatchlist = async (movie: Movie) => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (userStore.isInWatchlist(movie.id)) {
      await userStore.removeFromWatchlist(movie.id)
    } else {
      await userStore.addToWatchlistWithActivity(movie.id)
    }
  } catch (error) {
    console.error('Error updating watchlist:', error)
  }
}

const toggleFavorite = async (movie: Movie) => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (userStore.isInFavorites(movie.id)) {
      await userStore.removeFromFavorites(movie.id)
    } else {
      await userStore.addToFavoritesWithActivity(movie.id)
    }
  } catch (error) {
    console.error('Error updating favorites:', error)
  }
}

const onPageChange = (page: number) => {
  emit('pageChange', page)
}

const getMovieTypeIcon = (movie: Movie) => {
  if (movie.genre.includes('Comedy')) return '🥧'
  if (movie.genre.includes('Drama')) return '🍋'
  return '🎬'
}

const getMovieTypeBadge = (movie: Movie) => {
  if (movie.genre.includes('Comedy')) return 'badge-success'
  if (movie.genre.includes('Drama')) return 'badge-warning'
  return 'badge-primary'
}
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
    <!-- Loading State -->
    <template v-if="loading">
      <div 
        v-for="i in itemsPerPage" 
        :key="i" 
        class="bg-theme-surface rounded-lg shadow-md animate-pulse border border-theme-border"
      >
        <div class="bg-theme-border h-64 rounded-t-lg"></div>
        <div class="p-4">
          <div class="bg-theme-border h-4 rounded mb-2"></div>
          <div class="bg-theme-border h-3 rounded w-3/4 mb-2"></div>
          <div class="bg-theme-border h-3 rounded w-1/2"></div>
        </div>
      </div>
    </template>

    <!-- Movies Grid -->
    <template v-else-if="paginatedMovies.length > 0">
        <div 
          v-for="movie in paginatedMovies" 
          :key="movie.id"
          class="bg-theme-surface rounded-lg shadow-md hover:shadow-lg transition-all duration-300 group cursor-pointer border border-theme-border"
          @click="navigateToMovie(movie)"
        >
          <!-- Movie Poster -->
          <figure class="relative overflow-hidden">
            <img 
              :src="movie.poster" 
              :alt="movie.title"
              class="w-full h-64 object-cover transition-transform duration-300 group-hover:scale-105"
            />
            
            <!-- Overlay -->
            <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 flex items-center justify-center">
              <button 
                @click.stop="playTrailer(movie)"
                class="w-12 h-12 bg-orange-500 hover:bg-orange-600 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 transform scale-75 group-hover:scale-100"
              >
                <Play class="w-6 h-6" />
              </button>
            </div>
            
            <!-- Movie Type Badge -->
            <div class="absolute top-2 left-2">
              <div class="bg-orange-500 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1">
                <span>{{ getMovieTypeIcon(movie) }}</span>
                <span class="capitalize">{{ movie.genre[0] || 'Movie' }}</span>
              </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="absolute top-2 right-2 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300">
              <button 
                @click.stop="toggleWatchlist(movie)"
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center transition-colors',
                  userStore.isInWatchlist(movie.id) ? 'bg-orange-500 text-white' : 'bg-black bg-opacity-50 text-white hover:bg-opacity-70'
                ]"
                :title="userStore.isInWatchlist(movie.id) ? 'Remove from Watchlist' : 'Add to Watchlist'"
              >
                <Bookmark class="w-4 h-4" />
              </button>
              
              <button 
                @click.stop="toggleFavorite(movie)"
                :class="[
                  'w-8 h-8 rounded-full flex items-center justify-center transition-colors',
                  userStore.isInFavorites(movie.id) ? 'bg-red-500 text-white' : 'bg-black bg-opacity-50 text-white hover:bg-opacity-70'
                ]"
                :title="userStore.isInFavorites(movie.id) ? 'Remove from Favorites' : 'Add to Favorites'"
              >
                <Heart class="w-4 h-4" />
              </button>
            </div>
            
            <!-- Rating Badge -->
            <div class="absolute bottom-2 left-2">
              <div class="bg-black bg-opacity-70 text-white px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1">
                <Star class="w-3 h-3 fill-orange-400 text-orange-400" />
                <span>{{ movie.lemonPieRating.toFixed(1) }}</span>
              </div>
            </div>
          </figure>
          
          <!-- Movie Info -->
          <div class="p-4">
            <h3 class="text-sm font-bold line-clamp-2 group-hover:text-orange-600 transition-colors text-theme-primary">
              {{ movie.title }}
            </h3>
            
            <div class="flex items-center justify-between text-xs text-theme-text-secondary mt-2">
              <span>{{ movie.year }}</span>
            </div>
            

            

          </div>
        </div>
    </template>

    <!-- Empty State -->
    <div v-else class="col-span-full text-center py-12">
      <div class="text-6xl mb-4">🎬</div>
      <h3 class="text-xl font-bold mb-2 text-theme-primary">No movies found</h3>
      <p class="text-theme-text-secondary mb-4">Try adjusting your search criteria or filters</p>
    </div>
  </div>

  <!-- Pagination -->
  <div v-if="showPagination && totalPages > 1 && !loading" class="flex justify-center mt-8">
    <div class="flex gap-2">
      <button 
        @click="onPageChange(currentPage - 1)"
        :disabled="currentPage === 1"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors border',
          currentPage === 1
            ? 'bg-theme-surface text-theme-text-secondary border-theme-border cursor-not-allowed'
            : 'bg-theme-surface text-theme-text border-theme-border hover:bg-theme-surface-hover'
        ]"
      >
        Previous
      </button>
      
      <button 
        v-for="page in Math.min(totalPages, 5)" 
        :key="page"
        @click="onPageChange(page)"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors border',
          page === currentPage
            ? 'bg-orange-500 text-white border-orange-500'
            : 'bg-theme-surface text-theme-text border-theme-border hover:bg-theme-surface-hover'
        ]"
      >
        {{ page }}
      </button>
      
      <button 
        v-if="totalPages > 5"
        class="px-4 py-2 rounded-lg font-medium bg-theme-surface text-theme-text-secondary border border-theme-border cursor-not-allowed"
        disabled
      >
        ...
      </button>
      
      <button 
        @click="onPageChange(currentPage + 1)"
        :disabled="currentPage === totalPages"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors border',
          currentPage === totalPages
            ? 'bg-theme-surface text-theme-text-secondary border-theme-border cursor-not-allowed'
            : 'bg-theme-surface text-theme-text border-theme-border hover:bg-theme-surface-hover'
        ]"
      >
        Next
      </button>
    </div>
  </div>
  
  <!-- Results Summary -->
  <div v-if="!loading" class="text-center mt-4 text-sm text-theme-text-secondary">
    Showing {{ paginatedMovies.length }} of {{ movies.length }} movies
    <span v-if="showPagination && totalPages > 1">
      (Page {{ currentPage }} of {{ totalPages }})
    </span>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>