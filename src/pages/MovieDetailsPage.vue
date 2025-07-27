<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Star, Clock, Calendar, MapPin, Award, Play, Heart, Share2, MessageCircle, User, Plus } from 'lucide-vue-next'
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
const activeTab = ref('images')

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
    <!-- Hero Video Section -->
    <div class="relative w-full h-[500px] mb-8">
      <div class="relative group cursor-pointer bg-gray-800 w-full h-full overflow-hidden">
        <img 
          src="/src/assets/vue.svg" 
          :alt="`${movie.title} trailer`" 
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center group-hover:bg-opacity-60 transition-all duration-300">
          <div class="bg-orange-500 hover:bg-orange-600 rounded-full p-6 transform group-hover:scale-110 transition-transform duration-300">
            <Play class="w-12 h-12 text-white" />
          </div>
        </div>
        <div class="absolute bottom-6 left-6 bg-black bg-opacity-75 text-white px-4 py-3 rounded">
          <h4 class="text-xl font-semibold">{{ movie.title }} - Official Trailer</h4>
          <p class="text-sm text-gray-300">2:34</p>
        </div>
        <!-- Movie Info Overlay -->
        <div class="absolute top-6 right-6 bg-black bg-opacity-75 text-white px-4 py-3 rounded">
          <div class="flex items-center gap-2 mb-2">
            <Star class="w-5 h-5 text-yellow-400 fill-current" />
            <span class="text-lg font-bold">{{ averageRating.toFixed(1) }}</span>
            <span class="text-gray-300">/ 10</span>
          </div>
          <p class="text-sm text-gray-300">{{ movie.releaseDate }} • PG • 1hr 37min</p>
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column - Movie Poster -->
        <div class="lg:col-span-1">
          <div class="sticky top-8">
            <img
              :src="movie.poster"
              :alt="movie.title"
              class="w-full rounded-lg shadow-2xl"
            />
            
            <!-- Action Buttons -->
            <div class="mt-6 space-y-3">
              <button
                @click="playTrailer"
                class="w-full bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
              >
                <Play class="w-5 h-5" />
                Add to watchlist
              </button>
              <button
                @click="shareMovie"
                class="w-full bg-transparent text-white border border-gray-600 hover:bg-gray-800 px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
              >
                <Share2 class="w-5 h-5" />
                Share
              </button>
            </div>
            
            <!-- Movie Info Sidebar -->
            <div class="mt-8 space-y-4 text-sm">
              <div>
                <span class="text-gray-400">Original language</span>
                <p class="text-white">{{ movie.language }}</p>
              </div>
              <div>
                <span class="text-gray-400">Budget</span>
                <p class="text-white">$200,000,000.00</p>
              </div>
              <div>
                <span class="text-gray-400">Revenue</span>
                <p class="text-white">$318,000,000.00</p>
              </div>
              <div>
                <span class="text-gray-400">Production countries</span>
                <p class="text-white">{{ movie.productionState }}</p>
              </div>
              <div>
                <span class="text-gray-400">Keywords</span>
                <div class="flex flex-wrap gap-1 mt-1">
                  <span v-for="genre in movie.genre" :key="genre" class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs">{{ genre }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column - Movie Details -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Movie Title and Basic Info -->
          <div>
            <h1 class="text-4xl md:text-5xl font-bold mb-4">{{ movie.title }}</h1>
            <div class="flex items-center gap-4 mb-4 text-sm">
              <span class="text-gray-400">{{ movie.releaseDate }}</span>
              <span class="text-gray-400">•</span>
              <span class="text-gray-400">PG • 1hr 37min</span>
              <div class="flex items-center gap-1">
                <span v-for="genre in movie.genre.slice(0, 3)" :key="genre" class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs">{{ genre }}</span>
              </div>
            </div>
            
            <!-- Rating -->
            <div class="flex items-center gap-6 mb-6">
              <div class="flex items-center gap-2">
                <Star class="w-6 h-6 text-yellow-400 fill-current" />
                <span class="text-2xl font-bold">{{ averageRating.toFixed(1) }}</span>
                <span class="text-gray-400">/ 10</span>
              </div>
              <button class="text-blue-400 hover:text-blue-300 text-sm font-medium flex items-center gap-1">
                <Star class="w-4 h-4" />
                Rate this
              </button>
            </div>
            
            <!-- Plot Summary -->
            <p class="text-gray-300 leading-relaxed mb-6">{{ movie.plotSummary }}</p>
            
            <!-- Hero Image Gallery -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Movie Stills</h3>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="relative group cursor-pointer overflow-hidden rounded-lg">
                  <img 
                    :src="movie.poster" 
                    :alt="`${movie.title} still 1`" 
                    class="w-full h-24 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                </div>
                <div class="relative group cursor-pointer overflow-hidden rounded-lg">
                  <img 
                    :src="movie.poster" 
                    :alt="`${movie.title} still 2`" 
                    class="w-full h-24 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                </div>
                <div class="relative group cursor-pointer overflow-hidden rounded-lg">
                  <img 
                    :src="movie.poster" 
                    :alt="`${movie.title} still 3`" 
                    class="w-full h-24 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                </div>
                <div class="relative group cursor-pointer overflow-hidden rounded-lg">
                  <img 
                    :src="movie.poster" 
                    :alt="`${movie.title} still 4`" 
                    class="w-full h-24 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                </div>
              </div>
            </div>
            
            <!-- Director and Writers -->
            <div class="space-y-2 text-sm mb-8">
              <div class="flex">
                <span class="text-gray-400 w-20">Director</span>
                <span class="text-blue-400 hover:text-blue-300 cursor-pointer">{{ movie.director }}</span>
              </div>
              <div class="flex">
                <span class="text-gray-400 w-20">Writers</span>
                <span class="text-blue-400 hover:text-blue-300 cursor-pointer">{{ movie.director }}</span>
              </div>
              <div class="flex">
                <span class="text-gray-400 w-20">Stars</span>
                <div class="flex flex-wrap gap-1">
                  <span v-for="(actor, index) in movie.cast.slice(0, 3)" :key="actor" class="text-blue-400 hover:text-blue-300 cursor-pointer">
                    {{ actor }}<span v-if="index < movie.cast.slice(0, 3).length - 1">, </span>
                  </span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Content Tabs -->
          <div>
            <div class="flex border-b border-gray-700 mb-6">
              <button 
                @click="activeTab = 'images'"
                :class="[
                  'px-4 py-2 font-medium transition-colors border-b-2 text-sm',
                  activeTab === 'images'
                    ? 'border-orange-500 text-orange-500'
                    : 'border-transparent text-gray-400 hover:text-white'
                ]"
              >Images</button>
              <button 
                @click="activeTab = 'reviews'"
                :class="[
                  'px-4 py-2 font-medium transition-colors border-b-2 text-sm',
                  activeTab === 'reviews'
                    ? 'border-orange-500 text-orange-500'
                    : 'border-transparent text-gray-400 hover:text-white'
                ]"
              >
                Reviews ({{ reviews.length }})
              </button>
            </div>
            
            <!-- Images Tab -->
            <div v-if="activeTab === 'images'" class="space-y-4">
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <img v-for="i in 8" :key="i" :src="`https://via.placeholder.com/200x300`" :alt="`Image ${i}`" class="w-full h-32 object-cover rounded-lg cursor-pointer hover:opacity-80 transition-opacity" />
              </div>
            </div>
            
            <!-- Reviews Tab -->
            <div v-if="activeTab === 'reviews'" class="space-y-6">
              <div class="flex justify-between items-center">
                <div class="flex items-center gap-4">
                  <div class="flex items-center gap-2">
                    <Star class="w-5 h-5 text-yellow-400 fill-current" />
                    <span class="text-xl font-bold">{{ averageRating.toFixed(1) }}</span>
                    <span class="text-gray-400">/ 10</span>
                  </div>
                  <span class="text-gray-400">{{ reviews.length }} Reviews</span>
                </div>
                <button 
                  @click="router.push(`/write-review?movie=${movieId}`)"
                  class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors text-sm"
                >
                  Add Review
                </button>
              </div>
              
              <!-- Account Required Message -->
              <div class="bg-gray-800 border border-gray-700 rounded-lg p-6 text-center">
                <h3 class="text-lg font-semibold mb-2">Account required</h3>
                <p class="text-gray-400 mb-4">Please sign in or create account to add a review</p>
              </div>
              
              <!-- Sample Review -->
              <div class="bg-gray-800 rounded-lg p-6">
                <div class="flex items-start gap-4">
                  <div class="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center">
                    <User class="w-6 h-6 text-gray-400" />
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="font-semibold">Logan Roberts</span>
                      <span class="text-gray-400 text-sm">4 days ago</span>
                    </div>
                    <div class="flex items-center gap-1 mb-3">
                      <Star v-for="i in 5" :key="i" class="w-4 h-4 text-yellow-400 fill-current" />
                      <span class="text-sm text-gray-400 ml-2">9 / 10</span>
                    </div>
                    <h4 class="font-semibold mb-2">Action-Packed and Exciting</h4>
                    <p class="text-gray-300 leading-relaxed">This movie is a thrilling adventure from start to finish. The action sequences are mind-blowing, and the excitement never lets up. The characters are well-developed and the story is engaging throughout.</p>
                    <div class="flex items-center gap-4 mt-4 text-sm">
                      <span class="text-gray-400">Was this review helpful?</span>
                      <button class="text-blue-400 hover:text-blue-300">YES</button>
                      <button class="text-blue-400 hover:text-blue-300">NO</button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="reviews.length === 0" class="text-center py-8 text-gray-400">
                <MessageCircle class="w-12 h-12 mx-auto mb-4 text-gray-500" />
                <p>No reviews yet. Be the first to review this movie!</p>
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
        class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
      >
        Go Home
      </router-link>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles if needed */
</style>