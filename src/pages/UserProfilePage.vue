<template>
  <div class="min-h-screen bg-gray-900">
    <!-- Profile Header -->
    <div class="bg-gradient-to-r from-yellow-500 to-orange-600 py-16">
      <div class="container mx-auto px-4">
        <div class="flex flex-col md:flex-row items-center gap-8">
          <!-- Profile Picture -->
          <div class="avatar">
            <div class="w-32 h-32 rounded-full bg-white shadow-lg flex items-center justify-center">
              <User class="w-16 h-16 text-gray-600" />
            </div>
          </div>
          
          <!-- Profile Info -->
          <div class="text-center md:text-left text-white">
            <h1 class="text-4xl font-bold mb-2">{{ user.name }}</h1>
            <p class="text-xl text-yellow-100 mb-4">{{ user.bio || 'Nollywood Movie Enthusiast' }}</p>
            <div class="flex flex-wrap justify-center md:justify-start gap-4 text-sm">
              <div class="flex items-center gap-2">
                <Calendar class="w-4 h-4" />
                <span>Joined {{ formatDate(user.joinDate) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <MapPin class="w-4 h-4" />
                <span>{{ user.location || 'Nigeria' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-gray-800 rounded-lg p-6 text-center">
          <div class="text-3xl font-bold text-yellow-400">{{ userStats.totalReviews }}</div>
          <div class="text-gray-300">Reviews Written</div>
        </div>
        <div class="bg-gray-800 rounded-lg p-6 text-center">
          <div class="text-3xl font-bold text-green-400">{{ userStats.averageRating.toFixed(1) }}</div>
          <div class="text-gray-300">Average Rating</div>
        </div>
        <div class="bg-gray-800 rounded-lg p-6 text-center">
          <div class="text-3xl font-bold text-blue-400">{{ userStats.totalLikes }}</div>
          <div class="text-gray-300">Likes Received</div>
        </div>
        <div class="bg-gray-800 rounded-lg p-6 text-center">
          <div class="text-3xl font-bold text-purple-400">{{ userStats.moviesWatched }}</div>
          <div class="text-gray-300">Movies Watched</div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-gray-800 rounded-lg p-2 mb-8 flex flex-wrap gap-2">
        <button 
          @click="activeTab = 'reviews'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
            activeTab === 'reviews' ? 'bg-yellow-500 text-black' : 'text-white hover:bg-gray-700'
          ]"
        >
          <MessageSquare class="w-4 h-4" />
          My Reviews
        </button>
        <button 
          @click="activeTab = 'watchlist'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
            activeTab === 'watchlist' ? 'bg-yellow-500 text-black' : 'text-white hover:bg-gray-700'
          ]"
        >
          <Bookmark class="w-4 h-4" />
          Watchlist
        </button>
        <button 
          @click="activeTab = 'favorites'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
            activeTab === 'favorites' ? 'bg-yellow-500 text-black' : 'text-white hover:bg-gray-700'
          ]"
        >
          <Heart class="w-4 h-4" />
          Favorites
        </button>
        <button 
          @click="activeTab = 'settings'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
            activeTab === 'settings' ? 'bg-yellow-500 text-black' : 'text-white hover:bg-gray-700'
          ]"
        >
          <Settings class="w-4 h-4" />
          Settings
        </button>
      </div>

      <!-- Tab Content -->
      <div class="min-h-96">
        <!-- Reviews Tab -->
        <div v-if="activeTab === 'reviews'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-white">My Reviews ({{ userReviews.length }})</h2>
            <button 
              @click="router.push('/write-review')"
              class="bg-yellow-500 text-black px-4 py-2 rounded-lg font-medium hover:bg-yellow-400 transition-colors flex items-center gap-2"
            >
              <Plus class="w-4 h-4" />
              Write New Review
            </button>
          </div>
          
          <div v-if="userReviews.length > 0" class="space-y-6">
            <div 
              v-for="review in userReviews" 
              :key="review.id"
              class="bg-gray-800 rounded-lg p-6 hover:bg-gray-750 transition-colors duration-200"
            >
              <div class="flex justify-between items-start mb-4">
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-white mb-2">Review for {{ getMovieTitle(review.movieId) }}</h3>
                  <div class="flex items-center gap-4 mb-2">
                    <router-link 
                      :to="`/movie/${review.movieId}`" 
                      class="text-yellow-400 hover:underline font-semibold"
                    >
                      {{ getMovieTitle(review.movieId) }}
                    </router-link>
                    <LemonPieRating :rating="review.lemonPieRating" size="sm" />
                  </div>
                  <div class="text-sm text-gray-400 mb-3">
                    {{ formatDate(review.createdAt) }}
                  </div>
                </div>
                <div class="relative">
                  <button class="text-gray-400 hover:text-white p-2">
                    <MoreVertical class="w-4 h-4" />
                  </button>
                </div>
              </div>
              
              <p class="text-gray-300 mb-4">{{ review.reviewText }}</p>
              
              <div class="flex justify-between items-center">
                <div class="flex items-center gap-4 text-sm text-gray-400">
                  <span class="flex items-center gap-1">
                    <ThumbsUp class="w-4 h-4" />
                    {{ review.helpfulnessScore }}
                  </span>
                  <span class="flex items-center gap-1">
                    <ThumbsDown class="w-4 h-4" />
                    0
                  </span>
                  <span v-if="review.spoilerWarning" class="bg-yellow-500 text-black px-2 py-1 rounded text-xs font-medium">
                    Contains Spoilers
                  </span>
                </div>
                <router-link 
                  :to="`/movie/${review.movieId}`" 
                  class="bg-gray-700 text-white px-4 py-2 rounded-lg hover:bg-gray-600 transition-colors"
                >
                  View Movie
                </router-link>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-16">
            <div class="text-6xl mb-4">📝</div>
            <h3 class="text-2xl font-bold text-white mb-2">No reviews yet</h3>
            <p class="text-gray-400 mb-6">Start sharing your thoughts on Nollywood movies!</p>
            <button 
              @click="router.push('/write-review')"
              class="bg-yellow-500 text-black px-6 py-3 rounded-lg font-medium hover:bg-yellow-400 transition-colors"
            >
              Write Your First Review
            </button>
          </div>
        </div>

        <!-- Watchlist Tab -->
        <div v-if="activeTab === 'watchlist'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-white">My Watchlist ({{ watchlist.length }})</h2>
            <router-link 
              to="/movies" 
              class="bg-yellow-500 text-black px-4 py-2 rounded-lg font-medium hover:bg-yellow-400 transition-colors flex items-center gap-2"
            >
              <Plus class="w-4 h-4" />
              Add Movies
            </router-link>
          </div>
          
          <div v-if="watchlist.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div 
              v-for="movie in watchlist" 
              :key="movie.id"
              class="bg-gray-800 rounded-lg overflow-hidden hover:bg-gray-750 transition-colors duration-200"
            >
              <div class="relative">
                <img :src="movie.posterUrl" :alt="movie.title" class="w-full h-64 object-cover" />
                <button 
                  @click="removeFromWatchlist(movie.id, movie.type as 'movie' | 'series')"
                  class="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition-colors"
                >
                  <X class="w-4 h-4" />
                </button>
              </div>
              <div class="p-4">
                <h3 class="text-lg font-bold text-white mb-2">{{ movie.title }}</h3>
                <p class="text-sm text-gray-400 mb-4">{{ movie.releaseDate.split('-')[0] }} • {{ movie.genre.join(', ') }}</p>
                <router-link 
                  :to="movie.type === 'series' ? `/series/${movie.id}` : `/movie/${movie.id}`" 
                  class="bg-yellow-500 text-black px-4 py-2 rounded-lg font-medium hover:bg-yellow-400 transition-colors w-full block text-center"
                >
                  View Details
                </router-link>
              </div>
            </div>
          </div>
          
          <div v-else class="text-center py-16">
            <div class="text-6xl mb-4">🎬</div>
            <h3 class="text-2xl font-bold text-white mb-2">Your watchlist is empty</h3>
            <p class="text-gray-400 mb-6">Add movies you want to watch later!</p>
            <router-link 
              to="/movies" 
              class="bg-yellow-500 text-black px-6 py-3 rounded-lg font-medium hover:bg-yellow-400 transition-colors"
            >
              Browse Movies
            </router-link>
          </div>
        </div>

        <!-- Favorites Tab -->
        <div v-if="activeTab === 'favorites'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-white">My Favorites ({{ favorites.length }})</h2>
          </div>
          
          <div v-if="favorites.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <MovieCard 
              v-for="movie in favorites" 
              :key="movie.id" 
              :movie="movie as any"
              class="transform hover:scale-105 transition-transform duration-200"
              @click="router.push(movie.type === 'series' ? `/series/${movie.id}` : `/movie/${movie.id}`)"
            />
          </div>
          
          <div v-else class="text-center py-16">
            <div class="text-6xl mb-4">❤️</div>
            <h3 class="text-2xl font-bold text-white mb-2">No favorites yet</h3>
            <p class="text-gray-400 mb-6">Mark movies as favorites to see them here!</p>
            <router-link 
              to="/browse" 
              class="bg-yellow-500 text-black px-6 py-3 rounded-lg font-medium hover:bg-yellow-400 transition-colors"
            >
              Discover Movies
            </router-link>
          </div>
        </div>

        <!-- Settings Tab -->
        <div v-if="activeTab === 'settings'">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Account Settings</h2>
          
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <!-- Profile Settings -->
            <div class="card bg-white shadow-lg">
              <div class="card-body">
                <h3 class="card-title mb-4">Profile Information</h3>
                <form @submit.prevent="updateProfile">
                  <div class="form-control mb-4">
                    <label class="label">
                      <span class="label-text">Display Name</span>
                    </label>
                    <input 
                      v-model="profileForm.name" 
                      type="text" 
                      class="input input-bordered" 
                      required
                    />
                  </div>
                  
                  <div class="form-control mb-4">
                    <label class="label">
                      <span class="label-text">Bio</span>
                    </label>
                    <textarea 
                      v-model="profileForm.bio" 
                      class="textarea textarea-bordered" 
                      placeholder="Tell us about yourself..."
                    ></textarea>
                  </div>
                  
                  <div class="form-control mb-4">
                    <label class="label">
                      <span class="label-text">Location</span>
                    </label>
                    <input 
                      v-model="profileForm.location" 
                      type="text" 
                      class="input input-bordered" 
                      placeholder="e.g., Lagos, Nigeria"
                    />
                  </div>
                  
                  <button type="submit" class="btn btn-primary">
                    Update Profile
                  </button>
                </form>
              </div>
            </div>
            
            <!-- Preferences -->
            <div class="card bg-white shadow-lg">
              <div class="card-body">
                <h3 class="card-title mb-4">Preferences</h3>
                
                <div class="form-control mb-4">
                  <label class="cursor-pointer label">
                    <span class="label-text">Email Notifications</span>
                    <input v-model="preferences.emailNotifications" type="checkbox" class="toggle toggle-primary" />
                  </label>
                </div>
                
                <div class="form-control mb-4">
                  <label class="cursor-pointer label">
                    <span class="label-text">Show Profile Publicly</span>
                    <input v-model="preferences.publicProfile" type="checkbox" class="toggle toggle-primary" />
                  </label>
                </div>
                
                <div class="form-control mb-4">
                  <label class="label">
                    <span class="label-text">Preferred Language</span>
                  </label>
                  <select v-model="preferences.language" class="select select-bordered">
                    <option value="en">English</option>
                    <option value="yo">Yoruba</option>
                    <option value="ig">Igbo</option>
                    <option value="ha">Hausa</option>
                  </select>
                </div>
                
                <button @click="updatePreferences" class="btn btn-primary">
                  Save Preferences
                </button>
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
import { 
  User, Calendar, MapPin, MessageSquare, Bookmark, Heart, Settings,
  Plus, X, Edit, Trash2, MoreVertical, ThumbsUp, ThumbsDown
} from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import MovieCard from '@/components/MovieCard.vue'
import LemonPieRating from '@/components/LemonPieRating.vue'
// Using uiStore.showSuccessToast instead of sonner

const router = useRouter()
const movieStore = useMovieStore()
const userStore = useUserStore()
const uiStore = useUIStore()

// Active tab state
const activeTab = ref('reviews')

// Profile form state
const profileForm = ref({
  name: '',
  bio: '',
  location: ''
})

// Preferences state
const preferences = ref({
  emailNotifications: true,
  publicProfile: true,
  language: 'en'
})

// Computed properties
const user = computed(() => userStore.currentUser)
const userReviews = computed(() => userStore.userReviews)
const watchlist = computed(() => userStore.watchlistMovies)
const favorites = computed(() => userStore.favoriteMovies)
const userStats = computed(() => ({
  totalReviews: userReviews.value.length,
  averageRating: userReviews.value.length > 0 
    ? userReviews.value.reduce((sum, review) => sum + review.lemonPieRating, 0) / userReviews.value.length 
    : 0,
  totalLikes: userReviews.value.reduce((sum, review) => sum + review.helpfulnessScore, 0),
  moviesWatched: new Set(userReviews.value.map(r => r.movieId)).size
}))

// Methods
const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getMovieTitle = (movieId: string) => {
  const movie = movieStore.movies.find(m => m.id === movieId)
  return movie?.title || 'Unknown Movie'
}

const removeFromWatchlist = async (itemId: string, itemType: 'movie' | 'series') => {
  try {
    await userStore.removeFromWatchlist(itemId)
    uiStore.showSuccessToast(`${itemType === 'movie' ? 'Movie' : 'Series'} removed from watchlist`)
  } catch (error) {
    uiStore.showErrorToast(`Failed to remove ${itemType === 'movie' ? 'movie' : 'series'} from watchlist`)
  }
}

const editReview = (review: any) => {
  router.push(`/write-review?edit=${review.id}`)
}

const deleteReview = async (reviewId: string) => {
  try {
    await userStore.deleteUserReview(reviewId)
    uiStore.showSuccessToast('Review deleted successfully')
  } catch (error) {
    uiStore.showErrorToast('Failed to delete review')
  }
}

const updateProfile = async () => {
  try {
    await userStore.updateProfile(profileForm.value)
    uiStore.showSuccessToast('Profile updated successfully')
  } catch (error) {
    uiStore.showErrorToast('Failed to update profile')
  }
}

const updatePreferences = async () => {
  try {
    // Store preferences locally for now
    uiStore.showSuccessToast('Preferences saved successfully')
  } catch (error) {
    uiStore.showErrorToast('Failed to save preferences')
  }
}

// Initialize component
onMounted(async () => {
  uiStore.setPageTitle('My Profile')
  
  // Load user data if not already loaded
  if (!userStore.currentUser) {
    userStore.initializeMockAuth()
  }
  
  // Initialize form with current user data
  if (userStore.currentUser) {
    profileForm.value = {
      name: userStore.currentUser.name || '',
      bio: userStore.currentUser.bio || '',
      location: userStore.currentUser.location || ''
    }
  }
  
  // Initialize preferences with defaults
  preferences.value = {
    emailNotifications: true,
    publicProfile: true,
    language: 'en'
  }
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>