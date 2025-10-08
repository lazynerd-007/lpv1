<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore, type UserActivity } from '@/stores/userStore'
import { useMovieStore } from '@/stores/movieStore'
import { useUIStore } from '@/stores/uiStore'
import ActivityFeed from '@/components/ActivityFeed.vue'
import MovieCard from '@/components/MovieCard.vue'
import { 
  User, 
  Star, 
  Heart, 
  Bookmark, 
  MessageSquare, 
  TrendingUp,
  Calendar,
  Award,
  Users,
  Eye
} from 'lucide-vue-next'

const router = useRouter()
const userStore = useUserStore()
const movieStore = useMovieStore()
const uiStore = useUIStore()

// Redirect if not authenticated
if (!userStore.isAuthenticated) {
  router.push('/login')
}

const currentUser = computed(() => userStore.currentUser)
const userActivities = computed(() => {
    return userStore.userActivities.filter(activity => activity.userId === userStore.currentUser?.id)
  })
const recentActivities = computed(() => userActivities.value.slice(0, 5))

// User Statistics
const userStats = computed(() => {
  const userId = currentUser.value?.id
  if (!userId) return null
  
  const reviews = userStore.userReviews
  const watchlist = userStore.watchlist
  const favorites = userStore.favorites
  const following = userStore.following
  const followers = userStore.followers
  
  const totalRatings = reviews.reduce((sum, review) => sum + review.lemonPieRating, 0)
  const averageRating = reviews.length > 0 ? totalRatings / reviews.length : 0
  
  return {
    reviewsCount: reviews.length,
    averageRating,
    watchlistCount: watchlist.length,
    favoritesCount: favorites.length,
    followingCount: following.length,
    followersCount: followers.length
  }
})

// Recent Reviews
const recentReviews = computed(() => {
    return userStore.userReviews.slice(0, 3)
  })

// Recommended Movies (based on user's favorite genres)
const recommendedMovies = computed(() => {
  const userId = currentUser.value?.id
  if (!userId) return []
  
  const userReviews = userStore.userReviews
  const favoriteGenres = new Map<string, number>()
  
  // Count genre preferences from user's high-rated reviews
  userReviews.forEach(review => {
    if (review.lemonPieRating >= 7) {
      const movie = movieStore.getMovieById(review.movieId)
      if (movie) {
        movie.genre.forEach(genre => {
          favoriteGenres.set(genre, (favoriteGenres.get(genre) || 0) + 1)
        })
      }
    }
  })
  
  // Get top 3 favorite genres
  const topGenres = Array.from(favoriteGenres.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([genre]) => genre)
  
  if (topGenres.length === 0) {
    // If no preferences, return trending movies
    return movieStore.movies
      .filter(movie => movie.lemonPieRating >= 7.5)
      .slice(0, 6)
  }
  
  // Find movies in favorite genres that user hasn't reviewed
  const reviewedMovieIds = new Set(userReviews.map(r => r.movieId))
  
  return movieStore.movies
    .filter(movie => 
      !reviewedMovieIds.has(movie.id) &&
      movie.genre.some(genre => topGenres.includes(genre)) &&
      movie.lemonPieRating >= 7.0
    )
    .sort((a, b) => b.lemonPieRating - a.lemonPieRating)
    .slice(0, 6)
})

const navigateToProfile = () => {
  if (currentUser.value) {
    router.push(`/profile/${currentUser.value.id}`)
  }
}

const navigateToReviews = () => {
  if (currentUser.value) {
    router.push(`/profile/${currentUser.value.id}?tab=reviews`)
  }
}

const navigateToWatchlist = () => {
  router.push('/watchlist')
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

const getMovieTitle = (movieId: string) => {
  const movie = movieStore.getMovieById(movieId)
  return movie?.title || 'Unknown Movie'
}

const getActivityTitle = (activity: UserActivity) => {
  const movieTitle = getMovieTitle(activity.targetId)
  
  switch (activity.type) {
    case 'review':
      return `Reviewed "${movieTitle}"`
    case 'rating':
      return `Rated "${movieTitle}" ${activity.rating}/10`
    case 'watchlist_add':
      return `Added "${movieTitle}" to watchlist`
    case 'favorite_add':
      return `Added "${movieTitle}" to favorites`
    case 'follow':
      return `Started following a user`
    default:
      return activity.content || 'Unknown activity'
  }
}

onMounted(() => {
  uiStore.setPageTitle('Dashboard')
})
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header Section -->
    <div class="bg-gradient-to-r from-orange-500 to-yellow-500 py-8">
      <div class="container mx-auto px-4">
        <div class="flex items-center gap-6">
          <div class="w-20 h-20 rounded-full overflow-hidden border-4 border-white shadow-lg">
            <img 
              :src="currentUser?.avatar || 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=default%20user%20avatar%20profile%20picture&image_size=square'"
              :alt="currentUser?.name || 'User'"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="text-white">
            <h1 class="text-3xl font-bold mb-2">Welcome back, {{ currentUser?.name }}!</h1>
            <p class="text-orange-100">Here's what's happening in your Nollywood world</p>
          </div>
        </div>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <!-- Statistics Cards -->
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
        <div class="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow">
          <MessageSquare class="w-8 h-8 text-blue-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">{{ userStats?.reviewsCount || 0 }}</div>
          <div class="text-sm text-gray-600">Reviews</div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow">
          <Star class="w-8 h-8 text-yellow-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">{{ userStats?.averageRating.toFixed(1) || '0.0' }}</div>
          <div class="text-sm text-gray-600">Avg Rating</div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow cursor-pointer" @click="navigateToWatchlist">
          <Bookmark class="w-8 h-8 text-green-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">{{ userStats?.watchlistCount || 0 }}</div>
          <div class="text-sm text-gray-600">Watchlist</div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow">
          <Heart class="w-8 h-8 text-red-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">{{ userStats?.favoritesCount || 0 }}</div>
          <div class="text-sm text-gray-600">Favorites</div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow cursor-pointer" @click="navigateToProfile">
          <Users class="w-8 h-8 text-purple-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">{{ userStats?.followingCount || 0 }}</div>
          <div class="text-sm text-gray-600">Following</div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6 text-center hover:shadow-lg transition-shadow cursor-pointer" @click="navigateToProfile">
          <User class="w-8 h-8 text-indigo-500 mx-auto mb-2" />
          <div class="text-2xl font-bold text-gray-900">{{ userStats?.followersCount || 0 }}</div>
          <div class="text-sm text-gray-600">Followers</div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Recent Activity -->
        <div class="lg:col-span-2">
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex items-center justify-between mb-6">
              <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
                <TrendingUp class="w-5 h-5 text-orange-500" />
                Recent Activity
              </h2>
              <button 
                @click="navigateToProfile"
                class="text-orange-500 hover:text-orange-600 text-sm font-medium"
              >
                View All
              </button>
            </div>
            
            <div v-if="recentActivities.length > 0" class="space-y-4">
              <div 
                v-for="activity in recentActivities" 
                :key="activity.id"
                class="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div class="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center flex-shrink-0">
                  <MessageSquare v-if="activity.type === 'review'" class="w-4 h-4 text-orange-600" />
                  <Star v-else-if="activity.type === 'rating'" class="w-4 h-4 text-orange-600" />
                  <Bookmark v-else-if="activity.type === 'watchlist_add'" class="w-4 h-4 text-orange-600" />
                  <Heart v-else-if="activity.type === 'favorite_add'" class="w-4 h-4 text-orange-600" />
                  <Users v-else-if="activity.type === 'follow'" class="w-4 h-4 text-orange-600" />
                </div>
                <div class="flex-1 min-w-0">
                  <p class="text-sm text-gray-900">{{ getActivityTitle(activity) }}</p>
                  <p class="text-xs text-gray-500 mt-1">{{ formatDate(activity.timestamp) }}</p>
                </div>
              </div>
            </div>
            
            <div v-else class="text-center py-8">
              <TrendingUp class="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p class="text-gray-500">No recent activity</p>
              <p class="text-sm text-gray-400 mt-1">Start reviewing movies to see your activity here</p>
            </div>
          </div>
        </div>

        <!-- Quick Stats & Recent Reviews -->
        <div class="space-y-6">
          <!-- Recent Reviews -->
          <div class="bg-white rounded-lg shadow-md p-6">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2">
                <MessageSquare class="w-5 h-5 text-blue-500" />
                Recent Reviews
              </h3>
              <button 
                @click="navigateToReviews"
                class="text-orange-500 hover:text-orange-600 text-sm font-medium"
              >
                View All
              </button>
            </div>
            
            <div v-if="recentReviews.length > 0" class="space-y-3">
              <div 
                v-for="review in recentReviews" 
                :key="review.id"
                class="border-l-4 border-orange-200 pl-3 py-2"
              >
                <div class="flex items-center justify-between mb-1">
                  <h4 class="font-medium text-sm text-gray-900 truncate">{{ getMovieTitle(review.movieId) }}</h4>
                  <div class="flex items-center gap-1">
                    <Star class="w-3 h-3 text-yellow-400 fill-current" />
                    <span class="text-xs font-medium">{{ review.lemonPieRating }}/10</span>
                  </div>
                </div>
                <p class="text-xs text-gray-600 line-clamp-2">{{ review.reviewText }}</p>
                <p class="text-xs text-gray-400 mt-1">{{ formatDate(review.createdAt) }}</p>
              </div>
            </div>
            
            <div v-else class="text-center py-6">
              <MessageSquare class="w-8 h-8 text-gray-300 mx-auto mb-2" />
              <p class="text-sm text-gray-500">No reviews yet</p>
              <router-link to="/write-review" class="text-xs text-orange-500 hover:text-orange-600">
                Write your first review
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Recommended Movies -->
      <div class="mt-8">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
              <Award class="w-5 h-5 text-orange-500" />
              Recommended for You
            </h2>
            <router-link 
              to="/browse"
              class="text-orange-500 hover:text-orange-600 text-sm font-medium"
            >
              Browse All
            </router-link>
          </div>
          
          <div v-if="recommendedMovies.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <MovieCard 
              v-for="movie in recommendedMovies" 
              :key="movie.id"
              :movie="movie"
              variant="compact"
            />
          </div>
          
          <div v-else class="text-center py-8">
            <Award class="w-12 h-12 text-gray-300 mx-auto mb-3" />
            <p class="text-gray-500">No recommendations yet</p>
            <p class="text-sm text-gray-400 mt-1">Rate some movies to get personalized recommendations</p>
          </div>
        </div>
      </div>
    </div>
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