<template>
  <div class="min-h-screen bg-theme-background">
    
    <!-- DEBUG SECTION - REMOVE AFTER TESTING -->
    <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded m-4" role="alert">
      <strong class="font-bold">DEBUG INFO (Remove after testing):</strong>
      <div class="mt-2 text-sm">
        <p><strong>Is Authenticated:</strong> {{ userStore.isAuthenticated }}</p>
        <p><strong>Current User:</strong> {{ userStore.currentUser ? JSON.stringify(userStore.currentUser, null, 2) : 'null' }}</p>
        <p><strong>User Role:</strong> {{ userStore.currentUser?.role || 'No role' }}</p>
        <p><strong>Has Critic Role:</strong> {{ userStore.hasRole('critic') }}</p>
        <p><strong>Is Critic (method):</strong> {{ userStore.isCritic() }}</p>
      </div>
    </div>
    <!-- END DEBUG SECTION -->
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
          <div class="text-center md:text-left text-white flex-1">
            <div class="flex flex-col md:flex-row items-center md:items-start gap-3 mb-2">
              <h1 class="text-4xl font-bold">{{ user.name }}</h1>
              <CriticBadge 
                v-if="userStore.hasRole('critic')" 
                :isVerified="true" 
                size="large" 
                class="mt-1"
              />
            </div>
            <p class="text-xl text-yellow-100 mb-4">{{ user.bio || 'Nollywood Movie Enthusiast' }}</p>
            <div class="flex flex-wrap justify-center md:justify-start gap-4 text-sm mb-4">
              <div class="flex items-center gap-2">
                <Calendar class="w-4 h-4" />
                <span>Joined {{ formatDate(user.joinDate) }}</span>
              </div>
              <div class="flex items-center gap-2">
                <MapPin class="w-4 h-4" />
                <span>{{ user.location || 'Nigeria' }}</span>
              </div>
            </div>
            
            <!-- Favorite Genres -->
            <div v-if="favoriteGenres.length > 0" class="mb-4">
              <h3 class="text-sm font-semibold text-yellow-200 mb-2">Favorite Genres</h3>
              <div class="flex flex-wrap gap-2">
                <span 
                  v-for="genre in favoriteGenres.slice(0, 5)" 
                  :key="genre.name"
                  class="bg-white/20 backdrop-blur-sm px-3 py-1 rounded-full text-sm font-medium text-white"
                >
                  {{ genre.name }} ({{ genre.count }})
                </span>
              </div>
            </div>
            
            <!-- Quick Stats -->
            <div class="flex flex-wrap justify-center md:justify-start gap-6 text-sm">
              <div class="text-center">
                <div class="text-2xl font-bold">{{ userStats.totalReviews }}</div>
                <div class="text-yellow-200">Reviews</div>
              </div>
              <div class="text-center">
                <div class="text-2xl font-bold">{{ userStats.averageRating.toFixed(1) }}</div>
                <div class="text-yellow-200">Avg Rating</div>
              </div>

            </div>
          </div>
          
          <!-- Follow Button (for other users) -->
          <div v-if="!isOwnProfile" class="flex flex-col items-center gap-4">
            <FollowButton :user-id="user.id" size="lg" />
            <div class="text-center text-white/80">
              <div class="text-sm">Member since</div>
              <div class="font-semibold">{{ formatDate(user.joinDate) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <!-- Enhanced Stats Cards -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        <div class="bg-theme-card rounded-lg p-4 text-center hover:shadow-lg transition-shadow">
          <div class="text-2xl font-bold text-yellow-400">{{ userStats.totalReviews }}</div>
          <div class="text-xs text-theme-secondary">Reviews</div>
        </div>
        <div class="bg-theme-card rounded-lg p-4 text-center hover:shadow-lg transition-shadow">
          <div class="text-2xl font-bold text-green-400">{{ userStats.averageRating.toFixed(1) }}</div>
          <div class="text-xs text-theme-secondary">Avg Rating</div>
        </div>
        <div class="bg-theme-card rounded-lg p-4 text-center hover:shadow-lg transition-shadow">
          <div class="text-2xl font-bold text-blue-400">{{ userStats.totalLikes }}</div>
          <div class="text-xs text-theme-secondary">Likes</div>
        </div>
        <div class="bg-theme-card rounded-lg p-4 text-center hover:shadow-lg transition-shadow">
          <div class="text-2xl font-bold text-purple-400">{{ userStats.moviesWatched }}</div>
          <div class="text-xs text-theme-secondary">Movies</div>
        </div>
        <div class="bg-theme-card rounded-lg p-4 text-center hover:shadow-lg transition-shadow">
          <div class="text-2xl font-bold text-red-400">{{ userStats.highRatedMovies }}</div>
          <div class="text-xs text-theme-secondary">8+ Rated</div>
        </div>
        <div class="bg-theme-card rounded-lg p-4 text-center hover:shadow-lg transition-shadow">
          <div class="text-2xl font-bold text-indigo-400">{{ userStats.recentActivity }}</div>
          <div class="text-xs text-theme-secondary">This Month</div>
        </div>

      </div>
      
      <!-- Bio Section -->
      <div v-if="user.bio && user.bio !== 'Nollywood Movie Enthusiast'" class="bg-theme-card rounded-lg p-6 mb-8">
        <h2 class="text-xl font-bold text-theme-text mb-3 flex items-center gap-2">
          <User class="w-5 h-5 text-orange-500" />
          About
        </h2>
        <p class="text-theme-secondary leading-relaxed">{{ user.bio }}</p>
      </div>
      
      <!-- Favorite Genres Section -->
       <div v-if="favoriteGenres.length > 0" class="bg-theme-card rounded-lg p-6 mb-8">
         <h2 class="text-xl font-bold text-theme-text mb-4 flex items-center gap-2">
           <Heart class="w-5 h-5 text-red-500" />
           Favorite Genres
         </h2>
         <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
           <div 
             v-for="genre in favoriteGenres" 
             :key="genre.name"
             class="bg-theme-surface rounded-lg p-3 text-center hover:bg-theme-surface-hover transition-colors"
           >
             <div class="font-semibold text-theme-text">{{ genre.name }}</div>
             <div class="text-sm text-theme-secondary">{{ genre.count }} movies</div>
           </div>
         </div>
       </div>
       
       <!-- Follow Suggestions Section -->
       <div v-if="followSuggestions.length > 0" class="bg-theme-card rounded-lg p-6 mb-8">
         <h2 class="text-xl font-bold text-theme-text mb-4 flex items-center gap-2">
           <Users class="w-5 h-5 text-blue-500" />
           Suggested Users to Follow
         </h2>
         <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
           <div 
             v-for="suggestion in followSuggestions" 
             :key="suggestion.id"
             class="bg-theme-surface rounded-lg p-4 hover:bg-theme-surface-hover transition-colors"
           >
             <div class="flex items-center justify-between mb-3">
               <div class="flex items-center gap-3">
                 <div class="w-10 h-10 bg-gradient-to-br from-orange-400 to-red-500 rounded-full flex items-center justify-center text-white font-bold">
                   {{ suggestion.name.charAt(0).toUpperCase() }}
                 </div>
                 <div>
                   <div class="font-semibold text-theme-text">{{ suggestion.name }}</div>
                   <div class="text-sm text-theme-secondary">{{ suggestion.reviewCount }} reviews</div>
                 </div>
               </div>
               <FollowButton :userId="suggestion.id" variant="small" />
             </div>
             <div class="text-sm text-theme-secondary mb-2">
               <span class="font-medium">Similar interests:</span>
             </div>
             <div class="flex flex-wrap gap-1">
               <span 
                 v-for="genre in suggestion.commonGenres.slice(0, 3)" 
                 :key="genre"
                 class="px-2 py-1 bg-theme-card rounded text-xs text-theme-secondary"
               >
                 {{ genre }}
               </span>
             </div>
           </div>
         </div>
       </div>

      <!-- Tabs -->
      <div class="bg-theme-surface rounded-lg p-2 mb-8 flex flex-wrap gap-2">
        <button 
          @click="activeTab = 'reviews'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
            activeTab === 'reviews' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
          ]"
        >
          <MessageSquare class="w-4 h-4" />
          My Reviews
        </button>
        <button 
          v-if="userStore.hasRole('critic')"
          @click="activeTab = 'critiques'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
            activeTab === 'critiques' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
          ]"
        >
          <PenTool class="w-4 h-4" />
          My Critiques
        </button>
        <button 
          @click="activeTab = 'watchlist'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
            activeTab === 'watchlist' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
          ]"
        >
          <Bookmark class="w-4 h-4" />
          Watchlist
        </button>
        <button 
          @click="activeTab = 'favorites'"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
            activeTab === 'favorites' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
          ]"
        >
          <Heart class="w-4 h-4" />
          Favorites
        </button>



      </div>

      <!-- Tab Content -->
      <div class="min-h-96">
        <!-- Reviews Tab -->
        <div v-if="activeTab === 'reviews'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-theme-text">My Reviews ({{ userReviews.length }})</h2>
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
              class="bg-theme-card rounded-lg p-6 hover:bg-theme-card-hover transition-colors duration-200"
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

        <!-- My Critiques Tab -->
        <div v-if="activeTab === 'critiques'">
          <div class="flex justify-between items-center mb-6">
            <h2 class="text-2xl font-bold text-theme-text">My Critiques (0)</h2>
            <button 
              class="bg-yellow-500 text-black px-4 py-2 rounded-lg font-medium hover:bg-yellow-400 transition-colors flex items-center gap-2"
            >
              <PenTool class="w-4 h-4" />
              Write New Critique
            </button>
          </div>
          
          <div class="text-center py-16">
            <div class="text-6xl mb-4">🎭</div>
            <h3 class="text-2xl font-bold text-theme-text mb-2">No critiques yet</h3>
            <p class="text-theme-secondary mb-6">Share your professional analysis and insights on Nollywood films!</p>
            <button 
              class="bg-yellow-500 text-black px-6 py-3 rounded-lg font-medium hover:bg-yellow-400 transition-colors"
            >
              Write Your First Critique
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






      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User, Calendar, MapPin, MessageSquare, Bookmark, Heart, Settings,
  Plus, X, Edit, Trash2, MoreVertical, ThumbsUp, ThumbsDown, Users, UserCheck, Star, Eye, PenTool
} from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import MovieCard from '@/components/MovieCard.vue'
import LemonPieRating from '@/components/LemonPieRating.vue'
import FollowButton from '@/components/FollowButton.vue'
import CriticBadge from '@/components/CriticBadge.vue'
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
const followingUsers = computed(() => userStore.followingUsers)
const followerUsers = computed(() => userStore.followerUsers)

// Check if viewing own profile
const isOwnProfile = computed(() => {
  // For now, always true since we're viewing current user's profile
  // In a real app, this would compare route params with current user ID
  return true
})

// Calculate favorite genres based on user's high-rated reviews
const favoriteGenres = computed(() => {
  const genreCount = new Map<string, number>()
  
  userReviews.value.forEach(review => {
    if (review.lemonPieRating >= 7) { // Only count high-rated movies
      const movie = movieStore.movies.find(m => m.id === review.movieId)
      if (movie) {
        movie.genre.forEach(genre => {
          genreCount.set(genre, (genreCount.get(genre) || 0) + 1)
        })
      }
    }
  })
  
  return Array.from(genreCount.entries())
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 8) // Top 8 genres
})

// Generate follow suggestions based on similar movie preferences
const followSuggestions = computed(() => {
  if (!userStore.currentUser) return []
  
  // Get current user's favorite genres
  const userGenres = new Set(favoriteGenres.value.map(g => g.name))
  
  // Mock suggested users with similar interests
  const mockSuggestions = [
    {
      id: 'user-suggestion-1',
      name: 'Adunni Ade',
      reviewCount: 45,
      commonGenres: ['Drama', 'Romance', 'Comedy']
    },
    {
      id: 'user-suggestion-2', 
      name: 'Kunle Afolayan',
      reviewCount: 67,
      commonGenres: ['Drama', 'Thriller', 'Action']
    },
    {
      id: 'user-suggestion-3',
      name: 'Genevieve Nnaji',
      reviewCount: 89,
      commonGenres: ['Romance', 'Drama', 'Comedy']
    },
    {
      id: 'user-suggestion-4',
      name: 'Ramsey Nouah',
      reviewCount: 52,
      commonGenres: ['Action', 'Thriller', 'Drama']
    }
  ]
  
  // Filter out users already being followed and current user
  const currentFollowingIds = new Set(followingUsers.value.map(u => u.id))
  
  return mockSuggestions
    .filter(user => 
      user.id !== userStore.currentUser?.id && 
      !currentFollowingIds.has(user.id) &&
      user.commonGenres.some(genre => userGenres.has(genre))
    )
    .slice(0, 6) // Limit to 6 suggestions
})

const userStats = computed(() => ({
  totalReviews: userReviews.value.length,
  averageRating: userReviews.value.length > 0 
    ? userReviews.value.reduce((sum, review) => sum + review.lemonPieRating, 0) / userReviews.value.length 
    : 0,
  totalLikes: userReviews.value.reduce((sum, review) => sum + review.helpfulnessScore, 0),
  moviesWatched: new Set(userReviews.value.map(r => r.movieId)).size,
  followingCount: followingUsers.value.length,
  followersCount: followerUsers.value.length,
  // Additional stats
  highRatedMovies: userReviews.value.filter(r => r.lemonPieRating >= 8).length,
  recentActivity: userReviews.value.filter(r => {
    const reviewDate = new Date(r.createdAt)
    const thirtyDaysAgo = new Date()
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
    return reviewDate >= thirtyDaysAgo
  }).length
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