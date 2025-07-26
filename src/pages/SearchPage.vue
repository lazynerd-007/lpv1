<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Search, Filter, SlidersHorizontal, X } from 'lucide-vue-next';
import MovieCard from '@/components/MovieCard.vue';
import LemonPieRating from '@/components/LemonPieRating.vue';
import { mockMovies, type Movie } from '@/data/mockMovies';

const route = useRoute();
const router = useRouter();

// Search state
const searchQuery = ref('');
const searchResults = ref<Movie[]>([]);
const isLoading = ref(false);
const showFilters = ref(false);

// Filter state
const filters = ref({
  genre: '',
  year: '',
  rating: '',
  language: '',
  productionState: ''
});

// Filter options
const genreOptions = ['Comedy', 'Drama', 'Action', 'Romance', 'Thriller', 'Crime'];
const yearOptions = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017'];
const ratingOptions = [
  { label: 'All Ratings', value: '' },
  { label: 'Pies (7-10)', value: 'pie' },
  { label: 'Neutral (4-6)', value: 'neutral' },
  { label: 'Lemons (1-3)', value: 'lemon' }
];
const languageOptions = ['English', 'Yoruba', 'Igbo', 'Hausa'];
const stateOptions = ['Lagos', 'Enugu', 'Kano', 'Abuja', 'Rivers'];

// Computed
const filteredResults = computed(() => {
  let results = searchResults.value;
  
  if (filters.value.genre) {
    results = results.filter(movie => 
      movie.genre.some(g => g.toLowerCase().includes(filters.value.genre.toLowerCase()))
    );
  }
  
  if (filters.value.year) {
    results = results.filter(movie => 
      movie.releaseDate.startsWith(filters.value.year)
    );
  }
  
  if (filters.value.rating) {
    results = results.filter(movie => {
      const rating = movie.lemonPieRating;
      switch (filters.value.rating) {
        case 'pie': return rating >= 7;
        case 'neutral': return rating >= 4 && rating < 7;
        case 'lemon': return rating < 4;
        default: return true;
      }
    });
  }
  
  if (filters.value.language) {
    results = results.filter(movie => 
      movie.language.some(l => l.toLowerCase().includes(filters.value.language.toLowerCase()))
    );
  }
  
  if (filters.value.productionState) {
    results = results.filter(movie => 
      movie.productionState.toLowerCase().includes(filters.value.productionState.toLowerCase())
    );
  }
  
  return results;
});

const hasActiveFilters = computed(() => {
  return Object.values(filters.value).some(value => value !== '');
});

// Methods
const performSearch = () => {
  if (!searchQuery.value.trim()) {
    searchResults.value = [];
    return;
  }
  
  isLoading.value = true;
  
  // Simulate API call delay
  setTimeout(() => {
    const query = searchQuery.value.toLowerCase();
    searchResults.value = mockMovies.filter(movie => 
      movie.title.toLowerCase().includes(query) ||
      movie.localTitle?.toLowerCase().includes(query) ||
      movie.director.toLowerCase().includes(query) ||
      movie.cast.some(actor => actor.toLowerCase().includes(query)) ||
      movie.genre.some(genre => genre.toLowerCase().includes(query))
    );
    isLoading.value = false;
  }, 500);
};

const clearFilters = () => {
  filters.value = {
    genre: '',
    year: '',
    rating: '',
    language: '',
    productionState: ''
  };
};

const updateURL = () => {
  const query: any = {};
  if (searchQuery.value) query.q = searchQuery.value;
  if (hasActiveFilters.value) {
    Object.entries(filters.value).forEach(([key, value]) => {
      if (value) query[key] = value;
    });
  }
  router.replace({ query });
};

// Watchers
watch(searchQuery, () => {
  performSearch();
  updateURL();
});

watch(filters, () => {
  updateURL();
}, { deep: true });

// Lifecycle
onMounted(() => {
  // Initialize from URL query
  const query = route.query;
  if (query.q) {
    searchQuery.value = query.q as string;
  }
  
  // Initialize filters from URL
  Object.keys(filters.value).forEach(key => {
    if (query[key]) {
      (filters.value as any)[key] = query[key];
    }
  });
  
  if (searchQuery.value) {
    performSearch();
  }
});
</script>

<template>
  <div class="min-h-screen bg-base-100">
    <!-- Search Header -->
    <section class="bg-gradient-to-r from-nollywood-gold to-vibrant-orange py-12">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <h1 class="text-4xl font-bold text-white mb-4">
            🔍 Search Nollywood Movies
          </h1>
          <p class="text-xl text-cream-white/90 mb-8">
            Discover your next favorite Nigerian film
          </p>
          
          <!-- Search Bar -->
          <div class="form-control w-full">
            <div class="input-group justify-center">
              <input 
                v-model="searchQuery"
                type="text" 
                placeholder="Search movies, actors, directors..."
                class="input input-bordered input-lg w-full max-w-2xl"
                @keyup.enter="performSearch"
              />
              <button 
                class="btn btn-primary btn-lg"
                @click="performSearch"
                :disabled="isLoading"
              >
                <Search class="w-5 h-5" />
                <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
                <span v-else>Search</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Filters Section -->
    <section class="py-6 bg-base-200">
      <div class="container mx-auto px-4">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-4">
            <button 
              @click="showFilters = !showFilters"
              class="btn btn-outline gap-2"
            >
              <SlidersHorizontal class="w-4 h-4" />
              Filters
              <span v-if="hasActiveFilters" class="badge badge-primary badge-sm">{{ Object.values(filters).filter(v => v).length }}</span>
            </button>
            
            <button 
              v-if="hasActiveFilters"
              @click="clearFilters"
              class="btn btn-ghost btn-sm gap-1"
            >
              <X class="w-3 h-3" />
              Clear Filters
            </button>
          </div>
          
          <div v-if="searchQuery" class="text-sm text-gray-600">
            {{ filteredResults.length }} results for "{{ searchQuery }}"
          </div>
        </div>
        
        <!-- Filter Controls -->
        <div v-if="showFilters" class="mt-6 p-6 bg-base-100 rounded-lg shadow-sm">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <!-- Genre Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium">Genre</span>
              </label>
              <select v-model="filters.genre" class="select select-bordered">
                <option value="">All Genres</option>
                <option v-for="genre in genreOptions" :key="genre" :value="genre">
                  {{ genre }}
                </option>
              </select>
            </div>
            
            <!-- Year Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium">Year</span>
              </label>
              <select v-model="filters.year" class="select select-bordered">
                <option value="">All Years</option>
                <option v-for="year in yearOptions" :key="year" :value="year">
                  {{ year }}
                </option>
              </select>
            </div>
            
            <!-- Rating Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium">Rating</span>
              </label>
              <select v-model="filters.rating" class="select select-bordered">
                <option v-for="option in ratingOptions" :key="option.value" :value="option.value">
                  {{ option.label }}
                </option>
              </select>
            </div>
            
            <!-- Language Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium">Language</span>
              </label>
              <select v-model="filters.language" class="select select-bordered">
                <option value="">All Languages</option>
                <option v-for="language in languageOptions" :key="language" :value="language">
                  {{ language }}
                </option>
              </select>
            </div>
            
            <!-- Production State Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-medium">State</span>
              </label>
              <select v-model="filters.productionState" class="select select-bordered">
                <option value="">All States</option>
                <option v-for="state in stateOptions" :key="state" :value="state">
                  {{ state }}
                </option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Results Section -->
    <section class="py-12">
      <div class="container mx-auto px-4">
        <!-- Loading State -->
        <div v-if="isLoading" class="text-center py-12">
          <span class="loading loading-spinner loading-lg"></span>
          <p class="mt-4 text-gray-600">Searching Nollywood movies...</p>
        </div>
        
        <!-- No Query State -->
        <div v-else-if="!searchQuery" class="text-center py-12">
          <div class="text-6xl mb-4">🎬</div>
          <h2 class="text-2xl font-bold mb-2">Start Your Search</h2>
          <p class="text-gray-600">Enter a movie title, actor, or director to begin</p>
        </div>
        
        <!-- No Results State -->
        <div v-else-if="filteredResults.length === 0" class="text-center py-12">
          <div class="text-6xl mb-4">😔</div>
          <h2 class="text-2xl font-bold mb-2">No Results Found</h2>
          <p class="text-gray-600 mb-4">
            No movies found for "{{ searchQuery }}"
            <span v-if="hasActiveFilters">with the selected filters</span>
          </p>
          <div class="flex gap-2 justify-center">
            <button 
              v-if="hasActiveFilters"
              @click="clearFilters"
              class="btn btn-outline"
            >
              Clear Filters
            </button>
            <router-link to="/browse" class="btn btn-primary">
              Browse All Movies
            </router-link>
          </div>
        </div>
        
        <!-- Results Grid -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <MovieCard 
            v-for="movie in filteredResults" 
            :key="movie.id" 
            :movie="movie"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* Additional custom styles if needed */
</style>