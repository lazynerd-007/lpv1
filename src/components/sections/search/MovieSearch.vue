<template>
  <div class="card bg-gray-800 shadow-lg mb-8">
    <div class="card-body">
      <h2 class="card-title text-2xl mb-6 text-white">
        <Film class="w-6 h-6" />
        Select Movie
      </h2>
      
      <div class="form-control mb-4">
        <label class="label">
          <span class="label-text font-semibold text-gray-300">Search for a movie</span>
        </label>
        <div class="input-group">
          <input 
            v-model="searchQuery" 
            @input="handleSearch"
            type="text" 
            placeholder="Type movie title..." 
            class="input input-bordered flex-1 bg-gray-700 text-white border-gray-600"
          />
          <button class="btn btn-square bg-yellow-500 hover:bg-yellow-400 border-yellow-500">
            <Search class="w-4 h-4 text-black" />
          </button>
        </div>
      </div>

      <!-- Movie Search Results -->
      <div v-if="searchQuery && searchResults.length > 0" class="mb-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div 
            v-for="movie in searchResults" 
            :key="movie.id"
            @click="selectMovie(movie)"
            :class="[
              'card bg-gray-700 shadow cursor-pointer transition-all duration-200 hover:shadow-lg hover:bg-gray-600',
              selectedMovie?.id === movie.id ? 'ring-2 ring-yellow-500' : ''
            ]"
          >
            <div class="card-body p-4">
              <div class="flex gap-3">
                <img 
                  :src="movie.poster" 
                  :alt="movie.title" 
                  class="w-16 h-24 object-cover rounded"
                />
                <div class="flex-1">
                  <h3 class="font-bold text-white">{{ movie.title }}</h3>
                  <p class="text-sm text-gray-300">{{ movie.year }} • {{ movie.genre }}</p>
                  <p class="text-sm text-gray-400">{{ movie.director }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Selected Movie Display -->
      <div v-if="selectedMovie" class="alert bg-green-600 border-green-500">
        <CheckCircle class="w-6 h-6 text-white" />
        <div>
          <h3 class="font-bold text-white">Selected: {{ selectedMovie.title }}</h3>
          <div class="text-xs text-green-100">{{ selectedMovie.year }} • {{ selectedMovie.genre }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Film, Search, CheckCircle } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import type { Movie } from '@/data/mockMovies'

interface Props {
  selectedMovie?: Movie | null
}

interface Emits {
  (e: 'movie-selected', movie: Movie): void
}

const props = withDefaults(defineProps<Props>(), {
  selectedMovie: null
})

const emit = defineEmits<Emits>()

const movieStore = useMovieStore()

const searchQuery = ref('')
const searchResults = ref<Movie[]>([])

const handleSearch = () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }
  
  const query = searchQuery.value.toLowerCase()
  searchResults.value = movieStore.searchMovies(query).slice(0, 6)
}

const selectMovie = (movie: Movie) => {
  searchQuery.value = movie.title
  searchResults.value = []
  emit('movie-selected', movie)
}

// Watch for external changes to selectedMovie
watch(() => props.selectedMovie, (newMovie) => {
  if (newMovie) {
    searchQuery.value = newMovie.title
  }
})
</script>