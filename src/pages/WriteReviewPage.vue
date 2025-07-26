<template>
  <div class="min-h-screen bg-gray-900">
    <!-- Header Section -->
    <div class="bg-gradient-to-r from-yellow-500 to-orange-600 py-12">
      <div class="container mx-auto px-4">
        <h1 class="text-4xl font-bold text-white mb-4">Write a Review</h1>
        <p class="text-xl text-yellow-100">Share your thoughts on Nollywood movies</p>
      </div>
    </div>

    <div class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <!-- Movie Selection -->
        <MovieSearch 
          :selected-movie="selectedMovie" 
          @movie-selected="handleMovieSelected" 
        />

        <!-- Review Form -->
        <div v-if="selectedMovie">
          <ReviewForm 
            ref="reviewFormRef"
            :selected-movie="selectedMovie" 
            @submit="handleReviewSubmit"
            @reset="handleFormReset"
          />
        </div>

        <!-- Guidelines -->
        <ReviewGuidelines />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movieStore'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import MovieSearch from '@/components/sections/search/MovieSearch.vue'
import ReviewForm from '@/components/sections/movie/ReviewForm.vue'
import ReviewGuidelines from '@/components/sections/movie/ReviewGuidelines.vue'
import type { Movie } from '@/data/mockMovies'

const router = useRouter()
const movieStore = useMovieStore()
const userStore = useUserStore()
const uiStore = useUIStore()

const selectedMovie = ref<Movie | null>(null)
const reviewFormRef = ref()

const handleMovieSelected = (movie: Movie) => {
  selectedMovie.value = movie
}

const handleReviewSubmit = (formData: any) => {
  if (!selectedMovie.value) return
  
  // Create review object matching the Review interface
  const newReview = {
    userId: userStore.currentUser?.id || 'guest',
    movieId: selectedMovie.value.id,
    userName: formData.reviewerName,
    userAvatar: userStore.currentUser?.avatar || 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=default%20user%20avatar%20profile%20picture&image_size=square',
    lemonPieRating: formData.rating,
    reviewText: formData.content,
    reviewLanguage: 'en',
    spoilerWarning: formData.containsSpoilers,
    culturalAuthenticityRating: formData.rating, // Default to same as overall rating
    productionQualityRating: formData.rating, // Default to same as overall rating
    nollywoodTags: [], // Could be enhanced to allow user selection
    helpfulnessScore: 0,
    createdAt: new Date().toISOString(),
    isVerifiedCritic: false
  }
  
  // Add review to store
  movieStore.addReview(newReview)
  
  // Show success message
  uiStore.showSuccessToast('Review submitted successfully! Thank you for sharing your thoughts.')
  
  // Redirect to movie details page
  router.push(`/movie/${selectedMovie.value.id}`)
}

const handleFormReset = () => {
  selectedMovie.value = null
}

// Set page title
onMounted(() => {
  uiStore.setPageTitle('Write Review')
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