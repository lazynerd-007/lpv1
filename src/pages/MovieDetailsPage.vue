<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Star, Clock, Calendar, MapPin, Award, Play, Heart, Share2, MessageCircle, User } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import ReviewCard from '@/components/ui/ReviewCard.vue'

interface Props {
  id?: string
}

const props = defineProps<Props>()
const route = useRoute()
const router = useRouter()
const movieStore = useMovieStore()
const userStore = useUserStore()
const uiStore = useUIStore()

const movieId = computed(() => props.id || route.params.id as string)
const movie = computed(() => movieStore.movies.find(m => m.id === movieId.value))
const reviews = computed(() => movieStore.reviews.filter(r => r.movieId === movieId.value))
const activeTab = ref('overview')

const averageRating = computed(() => {
  if (!reviews.value.length) return movie.value?.lemonPieRating || 0
  return reviews.value.reduce((sum, review) => sum + review.lemonPieRating, 0) / reviews.value.length
})

const ratingDistribution = computed(() => {
  const dist = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
  reviews.value.forEach(review => {
    const rating = Math.ceil(review.lemonPieRating)
    if (rating >= 1 && rating <= 5) {
      dist[rating as keyof typeof dist]++
    }
  })
  return dist
})

const isInWatchlist = computed(() => {
  return userStore.isInWatchlist(movieId.value)
})

const isInFavorites = computed(() => {
  return userStore.isInFavorites(movieId.value)
})

const toggleWatchlist = async () => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (isInWatchlist.value) {
      await userStore.removeFromWatchlist(movieId.value)
    } else {
      await userStore.addToWatchlist(movieId.value)
    }
  } catch (error) {
    console.error('Error updating watchlist:', error)
  }
}

const toggleFavorites = async () => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (isInFavorites.value) {
      await userStore.removeFromFavorites(movieId.value)
    } else {
      await userStore.addToFavorites(movieId.value)
    }
  } catch (error) {
    console.error('Error updating favorites:', error)
  }
}

const playTrailer = () => {
  if (movie.value) {
    uiStore.openTrailerModal(movie.value.id, movie.value.trailerUrl || '')
  }
}

const shareMovie = async () => {
  if (navigator.share && movie.value) {
    try {
      await navigator.share({
        title: movie.value.title,
        text: `Check out ${movie.value.title} on Nollywood Movies`,
        url: window.location.href
      })
    } catch (error) {
      // Fallback to copying to clipboard
      navigator.clipboard.writeText(window.location.href)
    }
  } else {
    // Fallback to copying to clipboard
    navigator.clipboard.writeText(window.location.href)
  }
}

const handleReviewAction = async (action: string, reviewId: string) => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    switch (action) {
      case 'like':
        // Like functionality not implemented yet
        break
      case 'dislike':
        // Dislike functionality not implemented yet
        break
      case 'report':
        // Report functionality not implemented yet
        break
      case 'edit':
        router.push(`/write-review?movie=${movieId.value}&edit=${reviewId}`)
        break
      case 'delete':
        await movieStore.deleteReview(reviewId)
        break
    }
  } catch (error) {
    console.error('Error handling review action:', error)
  }
}

onMounted(async () => {
  // Set current movie for detailed view
  if (movie.value) {
    // Set current movie in store for reviews
    movieStore.currentMovie = movie.value
    uiStore.setPageTitle(`${movie.value.title} - Nollywood Movies`)
  } else {
    uiStore.setPageTitle('Movie Not Found - Nollywood Movies')
  }
})
</script>

<template>
  <div v-if="movie" class="min-h-screen bg-gray-900 text-white">
    <!-- Hero Section -->
    <div class="relative h-screen">
      <div class="absolute inset-0">
        <img
          :src="movie.poster"
          :alt="movie.title"
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/60 to-transparent"></div>
      </div>
      
      <div class="relative z-10 flex items-end h-full">
        <div class="container mx-auto px-4 pb-20">
          <div class="max-w-4xl">
            <h1 class="text-5xl md:text-7xl font-bold mb-4">{{ movie.title }}</h1>
            <div class="flex items-center gap-6 mb-6 text-lg">
              <div class="flex items-center gap-2">
                <Clock class="w-5 h-5" />
                <span>{{ movie.runtime }} min</span>
              </div>
              <div class="flex items-center gap-2">
                <Calendar class="w-5 h-5" />
                <span>{{ movie.releaseDate }}</span>
              </div>
              <div class="flex items-center gap-2">
                <MapPin class="w-5 h-5" />
                <span>{{ movie.productionState }}</span>
              </div>
              <div class="flex items-center gap-2">
                <Star class="w-5 h-5 text-yellow-400" />
                <span>{{ averageRating.toFixed(1) }}/5</span>
              </div>
            </div>
            <p class="text-xl mb-8 max-w-2xl leading-relaxed">{{ movie.plotSummary }}</p>
            
            <!-- Action Buttons -->
            <div class="flex items-center gap-4">
              <button
                @click="playTrailer"
                class="bg-yellow-500 hover:bg-yellow-600 text-black px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
              >
                <Play class="w-5 h-5" />
                Watch Trailer
              </button>
              <button
                @click="toggleWatchlist"
                :class="[
                  'border-2 px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors',
                  isInWatchlist
                    ? 'border-red-500 text-red-500 hover:bg-red-500 hover:text-white'
                    : 'border-white text-white hover:bg-white hover:text-black'
                ]"
              >
                <Heart :class="{ 'fill-current': isInWatchlist }" class="w-5 h-5" />
                {{ isInWatchlist ? 'Remove from Watchlist' : 'Add to Watchlist' }}
              </button>
              <button
                @click="toggleFavorites"
                :class="[
                  'border-2 px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors',
                  isInFavorites
                    ? 'border-yellow-500 text-yellow-500 hover:bg-yellow-500 hover:text-black'
                    : 'border-white text-white hover:bg-white hover:text-black'
                ]"
              >
                <Star :class="{ 'fill-current': isInFavorites }" class="w-5 h-5" />
                {{ isInFavorites ? 'Remove from Favorites' : 'Add to Favorites' }}
              </button>
              <button
                @click="shareMovie"
                class="border-2 border-white text-white hover:bg-white hover:text-black px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
              >
                <Share2 class="w-5 h-5" />
                Share
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Content Tabs -->
    <div class="container mx-auto px-4 py-8">
      <div class="flex border-b border-gray-700 mb-8">
        <button 
          @click="activeTab = 'overview'"
          :class="[
            'px-6 py-3 font-semibold transition-colors border-b-2',
            activeTab === 'overview'
              ? 'border-yellow-500 text-yellow-500'
              : 'border-transparent text-gray-400 hover:text-white'
          ]"
        >
          Overview
        </button>
        <button 
          @click="activeTab = 'reviews'"
          :class="[
            'px-6 py-3 font-semibold transition-colors border-b-2',
            activeTab === 'reviews'
              ? 'border-yellow-500 text-yellow-500'
              : 'border-transparent text-gray-400 hover:text-white'
          ]"
        >
          Reviews ({{ reviews.length }})
        </button>
        <button 
          @click="activeTab = 'cast'"
          :class="[
            'px-6 py-3 font-semibold transition-colors border-b-2',
            activeTab === 'cast'
              ? 'border-yellow-500 text-yellow-500'
              : 'border-transparent text-gray-400 hover:text-white'
          ]"
        >
          Cast & Crew
        </button>
      </div>
      
      <!-- Overview Tab -->
      <div v-if="activeTab === 'overview'" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2">
          <div class="bg-gray-800 rounded-lg p-6 mb-6">
            <h2 class="text-2xl font-bold mb-4">Plot Summary</h2>
            <p class="text-lg leading-relaxed text-gray-300">{{ movie.plotSummary }}</p>
          </div>
          
          <div class="bg-gray-800 rounded-lg p-6">
            <h2 class="text-2xl font-bold mb-4">Additional Details</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 class="font-semibold text-lg mb-2 text-yellow-400">Genre</h3>
                <div class="flex flex-wrap gap-2">
                  <span v-for="genre in movie.genre" :key="genre" class="bg-yellow-500 text-black px-3 py-1 rounded-full text-sm font-medium">{{ genre }}</span>
                </div>
              </div>
              <div>
                <h3 class="font-semibold text-lg mb-2 text-yellow-400">Language</h3>
                <p class="text-gray-300">{{ movie.language }}</p>
              </div>
              <div>
                <h3 class="font-semibold text-lg mb-2 text-yellow-400">Director</h3>
                <p class="text-gray-300">{{ movie.director }}</p>
              </div>
              <div>
                <h3 class="font-semibold text-lg mb-2 text-yellow-400">Production State</h3>
                <p class="text-gray-300">{{ movie.productionState }}</p>
              </div>
              <div>
                <h3 class="font-semibold text-lg mb-2 text-yellow-400">Release Date</h3>
                <p class="text-gray-300">{{ movie.releaseDate }}</p>
              </div>
              <div>
                <h3 class="font-semibold text-lg mb-2 text-yellow-400">Runtime</h3>
                <p class="text-gray-300">{{ movie.runtime }} minutes</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Rating Distribution -->
          <div class="bg-gray-800 rounded-lg p-6">
            <h3 class="text-xl font-bold mb-4">Rating Distribution</h3>
            <div class="space-y-3">
              <div v-for="(count, rating) in ratingDistribution" :key="rating" class="flex items-center gap-3">
                <div class="flex items-center gap-1 w-12">
                  <Star class="w-4 h-4 text-yellow-400" />
                  <span class="text-sm font-medium">{{ rating }}</span>
                </div>
                <div class="flex-1 bg-gray-700 rounded-full h-2">
                  <div 
                    class="bg-yellow-500 h-2 rounded-full transition-all duration-300"
                    :style="{ width: `${reviews.length > 0 ? (count / Math.max(...Object.values(ratingDistribution))) * 100 : 0}%` }"
                  ></div>
                </div>
                <span class="w-8 text-sm text-right text-gray-300">{{ count }}</span>
              </div>
            </div>
            
            <div class="border-t border-gray-700 mt-6 pt-6">
              <div class="text-center">
                <div class="text-3xl font-bold text-yellow-400">{{ averageRating.toFixed(1) }}</div>
                <div class="text-sm text-gray-400">Average Rating</div>
                <div class="text-sm text-gray-400">{{ reviews.length }} reviews</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Reviews Tab -->
      <div v-if="activeTab === 'reviews'" class="space-y-6">
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold">User Reviews</h2>
          <button 
            @click="router.push(`/write-review?movie=${movieId}`)"
            class="bg-yellow-500 hover:bg-yellow-600 text-black px-6 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
          >
            <MessageCircle class="w-5 h-5" />
            Write Review
          </button>
        </div>
        
        <div v-if="reviews.length === 0" class="text-center py-12 bg-gray-800 rounded-lg">
          <MessageCircle class="w-16 h-16 mx-auto text-gray-400 mb-4" />
          <h3 class="text-xl font-semibold mb-2">No reviews yet</h3>
          <p class="text-gray-400 mb-4">Be the first to share your thoughts about this movie!</p>
          <button 
            @click="router.push(`/write-review?movie=${movieId}`)"
            class="bg-yellow-500 hover:bg-yellow-600 text-black px-6 py-3 rounded-lg font-semibold transition-colors"
          >
            Write the first review
          </button>
        </div>
        
        <div v-else class="space-y-4">
          <ReviewCard 
            v-for="review in reviews" 
            :key="review.id" 
            :review="review"
            :show-movie-title="false"
            @action="handleReviewAction"
          />
        </div>
      </div>
      
      <!-- Cast & Crew Tab -->
      <div v-if="activeTab === 'cast'" class="space-y-8">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Cast -->
          <div class="bg-gray-800 rounded-lg p-6">
            <h2 class="text-2xl font-bold mb-6">Cast</h2>
            <div class="space-y-4">
              <div v-for="actor in movie.cast" :key="actor" class="flex items-center gap-4 p-3 bg-gray-700 rounded-lg">
                <div class="w-16 h-16 rounded-full overflow-hidden bg-gray-600 flex items-center justify-center">
                  <User class="w-8 h-8 text-gray-400" />
                </div>
                <div class="flex-1">
                  <h3 class="font-semibold text-lg text-white">{{ actor }}</h3>
                  <p class="text-gray-400">Actor</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Crew -->
          <div class="bg-gray-800 rounded-lg p-6">
            <h2 class="text-2xl font-bold mb-6">Crew</h2>
            <div class="space-y-4">
              <div class="flex justify-between items-center p-3 bg-gray-700 rounded-lg">
                <span class="font-semibold text-yellow-400">Director:</span>
                <span class="text-gray-300">{{ movie.director }}</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-gray-700 rounded-lg">
                <span class="font-semibold text-yellow-400">Producer:</span>
                <span class="text-gray-300">{{ movie.producer || 'N/A' }}</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-gray-700 rounded-lg">
                <span class="font-semibold text-yellow-400">Screenplay:</span>
                <span class="text-gray-300">N/A</span>
              </div>
              <div class="flex justify-between items-center p-3 bg-gray-700 rounded-lg">
                <span class="font-semibold text-yellow-400">Cinematography:</span>
                <span class="text-gray-300">N/A</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Movie Not Found -->
  <div v-else class="min-h-screen flex items-center justify-center bg-gray-900 text-white">
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">Movie Not Found</h1>
      <p class="text-gray-400 mb-8">The movie you're looking for doesn't exist or has been removed.</p>
      <router-link 
        to="/" 
        class="bg-yellow-500 hover:bg-yellow-600 text-black px-6 py-3 rounded-lg font-semibold transition-colors"
      >
        Go Home
      </router-link>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles if needed */
</style>