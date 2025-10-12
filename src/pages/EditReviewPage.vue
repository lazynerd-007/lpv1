<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-bold mb-6">Edit Your Review</h1>
      
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="loading loading-spinner loading-lg"></div>
      </div>
      
      <div v-else-if="error" class="alert alert-error shadow-lg mb-6">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>{{ error }}</span>
        </div>
      </div>
      
      <div v-else-if="!review" class="alert alert-warning shadow-lg mb-6">
        <div>
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
          <span>Review not found or you don't have permission to edit it.</span>
        </div>
        <div class="flex-none">
          <router-link :to="{ name: 'home' }" class="btn btn-sm">Go Home</router-link>
        </div>
      </div>
      
      <div v-else>
        <div class="card bg-base-100 shadow-xl mb-6">
          <div class="card-body">
            <h2 class="card-title text-xl mb-4">
              Editing review for: {{ movieTitle }}
            </h2>
            
            <ReviewForm 
              :movie-id="movieId" 
              :movie-title="movieTitle"
              :edit-review="review"
              @submit="handleSubmit"
              @cancel="handleCancel"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movieStore'
import { useAuthStore } from '@/stores/authStore'
import ReviewForm from '@/components/ReviewForm.vue'
import type { Review } from '@/data/mockMovies'

const route = useRoute()
const router = useRouter()
const movieStore = useMovieStore()
const authStore = useAuthStore()

const reviewId = computed(() => route.params.reviewId as string)
const movieId = ref('')
const movieTitle = ref('')
const review = ref<Review | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    // Get the review data
    // Find the review in the reviews array
    const foundReview = movieStore.reviews.find(r => r.id === reviewId.value)
    
    if (!foundReview) {
      error.value = 'Review not found'
      loading.value = false
      return
    }
    
    // Check if the current user is the author of the review
    if (foundReview.userId !== authStore.user?.id) {
      error.value = 'You do not have permission to edit this review'
      loading.value = false
      return
    }
    
    // Get the movie details
    const movie = movieStore.getMovieById(foundReview.movieId)
    if (movie) {
      movieId.value = movie.id
      movieTitle.value = movie.title
    }
    
    // Set the review data
    review.value = foundReview
  } catch (err) {
    error.value = 'An error occurred while loading the review'
    console.error(err)
  } finally {
    loading.value = false
  }
})

const handleSubmit = async (updatedReview: Omit<Review, 'id' | 'createdAt'>) => {
  try {
    // Update the review in the store
    const reviewToUpdate = {
      ...review.value,
      ...updatedReview,
      id: reviewId.value,
      createdAt: review.value?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    await movieStore.updateReview(reviewToUpdate)
    
    // Redirect to the movie details page
    router.push({ 
      name: 'movie-details', 
      params: { id: movieId.value },
      query: { reviewUpdated: 'true' }
    })
  } catch (err) {
    error.value = 'Failed to update review'
    console.error(err)
  }
}

const handleCancel = () => {
  router.back()
}
</script>