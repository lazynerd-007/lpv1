<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50">
    <!-- Header Section -->
    <div class="bg-gradient-to-r from-yellow-400 to-orange-500 py-12">
      <div class="container mx-auto px-4">
        <h1 class="text-4xl font-bold text-white mb-4">Write a Review</h1>
        <p class="text-xl text-yellow-100">Share your thoughts on Nollywood movies</p>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <!-- Movie Selection -->
        <div class="card bg-white shadow-lg mb-8">
          <div class="card-body">
            <h2 class="card-title text-2xl mb-6 text-gray-800">
              <Film class="w-6 h-6" />
              Select Movie
            </h2>
            
            <div class="form-control mb-4">
              <label class="label">
                <span class="label-text font-semibold">Search for a movie</span>
              </label>
              <div class="input-group">
                <input 
                  v-model="movieSearch" 
                  @input="searchMovies"
                  type="text" 
                  placeholder="Type movie title..." 
                  class="input input-bordered flex-1"
                />
                <button class="btn btn-square btn-primary">
                  <Search class="w-4 h-4" />
                </button>
              </div>
            </div>

            <!-- Movie Search Results -->
            <div v-if="movieSearch && searchResults.length > 0" class="mb-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div 
                  v-for="movie in searchResults" 
                  :key="movie.id"
                  @click="selectMovie(movie)"
                  :class="[
                    'card bg-base-100 shadow cursor-pointer transition-all duration-200 hover:shadow-lg',
                    selectedMovie?.id === movie.id ? 'ring-2 ring-primary' : ''
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
                        <h3 class="font-bold">{{ movie.title }}</h3>
                        <p class="text-sm text-gray-600">{{ movie.year }} • {{ movie.genre }}</p>
                        <p class="text-sm text-gray-500">{{ movie.director }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Selected Movie Display -->
            <div v-if="selectedMovie" class="alert alert-success">
              <CheckCircle class="w-6 h-6" />
              <div>
                <h3 class="font-bold">Selected: {{ selectedMovie.title }}</h3>
                <div class="text-xs">{{ selectedMovie.year }} • {{ selectedMovie.genre }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Review Form -->
        <div v-if="selectedMovie" class="card bg-white shadow-lg">
          <div class="card-body">
            <h2 class="card-title text-2xl mb-6 text-gray-800">
              <PenTool class="w-6 h-6" />
              Your Review
            </h2>

            <form @submit.prevent="submitReview">
              <!-- Rating Section -->
              <div class="form-control mb-6">
                <label class="label">
                  <span class="label-text font-semibold text-lg">Your Lemon 🍋 or Pie 🥧 Rating</span>
                </label>
                <div class="flex flex-col gap-4">
                  <!-- Rating Slider -->
                  <div class="flex items-center gap-4">
                    <span class="text-2xl">🍋</span>
                    <input 
                      v-model="rating" 
                      type="range" 
                      min="1" 
                      max="10" 
                      class="range range-warning flex-1" 
                      step="1"
                    />
                    <span class="text-2xl">🥧</span>
                  </div>
                  
                  <!-- Rating Display -->
                  <div class="text-center">
                    <div class="text-4xl mb-2">
                      {{ rating <= 5 ? '🍋' : '🥧' }}
                    </div>
                    <div class="text-xl font-bold">
                      {{ rating }}/10 - {{ getRatingLabel(rating) }}
                    </div>
                    <div class="text-sm text-gray-600">
                      {{ rating <= 5 ? 'Fresh Lemon' : 'Delicious Pie' }}
                    </div>
                  </div>
                </div>
              </div>

              <!-- Review Title -->
              <div class="form-control mb-4">
                <label class="label">
                  <span class="label-text font-semibold">Review Title</span>
                </label>
                <input 
                  v-model="reviewTitle" 
                  type="text" 
                  placeholder="Give your review a catchy title..." 
                  class="input input-bordered" 
                  required
                />
              </div>

              <!-- Review Content -->
              <div class="form-control mb-6">
                <label class="label">
                  <span class="label-text font-semibold">Your Review</span>
                  <span class="label-text-alt">{{ reviewContent.length }}/1000 characters</span>
                </label>
                <textarea 
                  v-model="reviewContent" 
                  class="textarea textarea-bordered h-32" 
                  placeholder="Share your thoughts about the movie. What did you like or dislike? How was the acting, plot, cinematography?..."
                  maxlength="1000"
                  required
                ></textarea>
              </div>

              <!-- Spoiler Warning -->
              <div class="form-control mb-6">
                <label class="cursor-pointer label">
                  <span class="label-text font-semibold">Contains Spoilers</span>
                  <input 
                    v-model="containsSpoilers" 
                    type="checkbox" 
                    class="toggle toggle-warning" 
                  />
                </label>
                <div class="label">
                  <span class="label-text-alt text-gray-500">
                    Check this if your review reveals important plot points
                  </span>
                </div>
              </div>

              <!-- Reviewer Info -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Your Name</span>
                  </label>
                  <input 
                    v-model="reviewerName" 
                    type="text" 
                    placeholder="Enter your name" 
                    class="input input-bordered" 
                    required
                  />
                </div>
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Email (optional)</span>
                  </label>
                  <input 
                    v-model="reviewerEmail" 
                    type="email" 
                    placeholder="your@email.com" 
                    class="input input-bordered"
                  />
                </div>
              </div>

              <!-- Submit Buttons -->
              <div class="flex flex-col sm:flex-row gap-4 justify-end">
                <button 
                  type="button" 
                  @click="resetForm" 
                  class="btn btn-outline btn-warning"
                >
                  <RotateCcw class="w-4 h-4 mr-2" />
                  Reset Form
                </button>
                <button 
                  type="submit" 
                  class="btn btn-primary"
                  :disabled="!isFormValid"
                >
                  <Send class="w-4 h-4 mr-2" />
                  Submit Review
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Guidelines -->
        <div class="card bg-gradient-to-r from-blue-50 to-indigo-50 shadow-lg mt-8">
          <div class="card-body">
            <h3 class="card-title text-xl mb-4 text-blue-800">
              <Info class="w-5 h-5" />
              Review Guidelines
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <h4 class="font-semibold text-blue-700 mb-2">✅ Do:</h4>
                <ul class="space-y-1 text-blue-600">
                  <li>• Be honest and constructive</li>
                  <li>• Focus on the movie's content</li>
                  <li>• Respect different opinions</li>
                  <li>• Use appropriate language</li>
                </ul>
              </div>
              <div>
                <h4 class="font-semibold text-red-700 mb-2">❌ Don't:</h4>
                <ul class="space-y-1 text-red-600">
                  <li>• Include personal attacks</li>
                  <li>• Post spam or irrelevant content</li>
                  <li>• Reveal major spoilers without warning</li>
                  <li>• Use offensive language</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Film, Search, CheckCircle, PenTool, RotateCcw, Send, Info } from 'lucide-vue-next'
import { mockMovies } from '@/data/mockMovies'
import type { Movie } from '@/data/mockMovies'

const router = useRouter()

// Form data
const movieSearch = ref('')
const selectedMovie = ref<Movie | null>(null)
const rating = ref(5)
const reviewTitle = ref('')
const reviewContent = ref('')
const containsSpoilers = ref(false)
const reviewerName = ref('')
const reviewerEmail = ref('')

// Search results
const searchResults = ref<Movie[]>([])

// Computed properties
const isFormValid = computed(() => {
  return selectedMovie.value && 
         reviewTitle.value.trim() && 
         reviewContent.value.trim() && 
         reviewerName.value.trim()
})

// Methods
const searchMovies = () => {
  if (!movieSearch.value.trim()) {
    searchResults.value = []
    return
  }
  
  const query = movieSearch.value.toLowerCase()
  searchResults.value = mockMovies.filter(movie => 
    movie.title.toLowerCase().includes(query) ||
    movie.director.toLowerCase().includes(query) ||
    movie.cast.some(actor => actor.toLowerCase().includes(query))
  ).slice(0, 6) // Limit to 6 results
}

const selectMovie = (movie: Movie) => {
  selectedMovie.value = movie
  movieSearch.value = movie.title
  searchResults.value = []
}

const getRatingLabel = (rating: number): string => {
  if (rating <= 2) return 'Terrible'
  if (rating <= 4) return 'Poor'
  if (rating <= 5) return 'Average'
  if (rating <= 6) return 'Good'
  if (rating <= 8) return 'Great'
  if (rating <= 9) return 'Excellent'
  return 'Masterpiece'
}

const resetForm = () => {
  movieSearch.value = ''
  selectedMovie.value = null
  rating.value = 5
  reviewTitle.value = ''
  reviewContent.value = ''
  containsSpoilers.value = false
  reviewerName.value = ''
  reviewerEmail.value = ''
  searchResults.value = []
}

const submitReview = () => {
  if (!isFormValid.value) return
  
  // Create review object
  const newReview = {
    id: Date.now().toString(),
    movieId: selectedMovie.value!.id,
    title: reviewTitle.value,
    content: reviewContent.value,
    rating: rating.value,
    containsSpoilers: containsSpoilers.value,
    reviewer: {
      name: reviewerName.value,
      email: reviewerEmail.value || undefined
    },
    date: new Date().toISOString(),
    likes: 0,
    dislikes: 0
  }
  
  // In a real app, this would be sent to an API
  console.log('Submitting review:', newReview)
  
  // Show success message (you could use a toast library here)
  alert('Review submitted successfully! Thank you for sharing your thoughts.')
  
  // Redirect to movie details page
  router.push(`/movie/${selectedMovie.value!.id}`)
}

// Set page title
onMounted(() => {
  document.title = 'Write Review - LemonNPie'
})
</script>

<style scoped>
/* Custom range styling */
.range::-webkit-slider-thumb {
  background: linear-gradient(45deg, #fbbf24, #f59e0b);
}

.range::-moz-range-thumb {
  background: linear-gradient(45deg, #fbbf24, #f59e0b);
  border: none;
}
</style>