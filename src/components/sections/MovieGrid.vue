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
      await userStore.addToWatchlist(movie.id)
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
      await userStore.addToFavorites(movie.id)
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
  <section class="py-8">
    <div class="container mx-auto px-4">
      <!-- Loading State -->
      <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="i in itemsPerPage" 
          :key="i" 
          class="card bg-base-100 shadow-lg animate-pulse"
        >
          <div class="bg-gray-300 h-64 rounded-t-lg"></div>
          <div class="card-body">
            <div class="bg-gray-300 h-4 rounded mb-2"></div>
            <div class="bg-gray-300 h-3 rounded w-3/4 mb-2"></div>
            <div class="bg-gray-300 h-3 rounded w-1/2"></div>
          </div>
        </div>
      </div>

      <!-- Movies Grid -->
      <div v-else-if="paginatedMovies.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div 
          v-for="movie in paginatedMovies" 
          :key="movie.id"
          class="card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300 group cursor-pointer"
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
                class="btn btn-circle btn-primary opacity-0 group-hover:opacity-100 transition-all duration-300 transform scale-75 group-hover:scale-100"
              >
                <Play class="w-6 h-6" />
              </button>
            </div>
            
            <!-- Movie Type Badge -->
            <div class="absolute top-2 left-2">
              <div :class="['badge', getMovieTypeBadge(movie), 'gap-1']">
                <span>{{ getMovieTypeIcon(movie) }}</span>
                <span class="capitalize">{{ movie.genre[0] || 'Movie' }}</span>
              </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="absolute top-2 right-2 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300">
              <button 
                @click.stop="toggleWatchlist(movie)"
                :class="[
                  'btn btn-sm btn-circle',
                  userStore.isInWatchlist(movie.id) ? 'btn-warning' : 'btn-ghost bg-black bg-opacity-50 text-white'
                ]"
                :title="userStore.isInWatchlist(movie.id) ? 'Remove from Watchlist' : 'Add to Watchlist'"
              >
                <Bookmark class="w-4 h-4" />
              </button>
              
              <button 
                @click.stop="toggleFavorite(movie)"
                :class="[
                  'btn btn-sm btn-circle',
                  userStore.isInFavorites(movie.id) ? 'btn-error' : 'btn-ghost bg-black bg-opacity-50 text-white'
                ]"
                :title="userStore.isInFavorites(movie.id) ? 'Remove from Favorites' : 'Add to Favorites'"
              >
                <Heart class="w-4 h-4" />
              </button>
            </div>
            
            <!-- Rating Badge -->
            <div class="absolute bottom-2 left-2">
              <div class="badge badge-neutral gap-1">
                <Star class="w-3 h-3 fill-yellow-400 text-yellow-400" />
                <span>{{ movie.lemonPieRating.toFixed(1) }}</span>
              </div>
            </div>
          </figure>
          
          <!-- Movie Info -->
          <div class="card-body p-4">
            <h3 class="card-title text-sm font-bold line-clamp-2 group-hover:text-primary transition-colors">
              {{ movie.title }}
            </h3>
            
            <div class="flex items-center justify-between text-xs text-gray-600 mt-2">
              <span>{{ movie.year }}</span>
              <span class="flex items-center gap-1">
                <Eye class="w-3 h-3" />
                {{ movie.reviewCount || 0 }} reviews
              </span>
            </div>
            
            <div class="flex flex-wrap gap-1 mt-2">
              <span 
                v-for="genre in movie.genre.slice(0, 2)" 
                :key="genre"
                class="badge badge-outline badge-xs"
              >
                {{ genre }}
              </span>
              <span 
                v-if="movie.genre.length > 2"
                class="badge badge-outline badge-xs"
              >
                +{{ movie.genre.length - 2 }}
              </span>
            </div>
            
            <!-- Production State -->
            <div v-if="movie.productionState" class="mt-2">
              <span class="text-xs text-gray-500">{{ movie.productionState }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <div class="text-6xl mb-4">🎬</div>
        <h3 class="text-xl font-bold mb-2">No movies found</h3>
        <p class="text-gray-600 mb-4">Try adjusting your search criteria or filters</p>
      </div>

      <!-- Pagination -->
      <div v-if="showPagination && totalPages > 1 && !loading" class="flex justify-center mt-8">
        <div class="join">
          <button 
            @click="onPageChange(currentPage - 1)"
            :disabled="currentPage === 1"
            class="join-item btn btn-outline"
          >
            Previous
          </button>
          
          <button 
            v-for="page in Math.min(totalPages, 5)" 
            :key="page"
            @click="onPageChange(page)"
            :class="[
              'join-item btn',
              page === currentPage ? 'btn-primary' : 'btn-outline'
            ]"
          >
            {{ page }}
          </button>
          
          <button 
            v-if="totalPages > 5"
            class="join-item btn btn-outline btn-disabled"
          >
            ...
          </button>
          
          <button 
            @click="onPageChange(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="join-item btn btn-outline"
          >
            Next
          </button>
        </div>
      </div>
      
      <!-- Results Summary -->
      <div v-if="!loading" class="text-center mt-4 text-sm text-gray-600">
        Showing {{ paginatedMovies.length }} of {{ movies.length }} movies
        <span v-if="showPagination && totalPages > 1">
          (Page {{ currentPage }} of {{ totalPages }})
        </span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>