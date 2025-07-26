<script setup lang="ts">
import { computed } from 'vue'
import { Star, ThumbsUp, ThumbsDown, Flag, MoreHorizontal, Calendar, User } from 'lucide-vue-next'
import { useUserStore } from '@/stores/userStore'
import { useMovieStore } from '@/stores/movieStore'
import type { Review } from '@/data/mockMovies'

interface Props {
  review: Review
  showMovieTitle?: boolean
  compact?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showMovieTitle: false,
  compact: false
})

const emit = defineEmits<{
  like: [reviewId: string]
  dislike: [reviewId: string]
  report: [reviewId: string]
  edit: [reviewId: string]
  delete: [reviewId: string]
}>()

const userStore = useUserStore()
const movieStore = useMovieStore()

const isOwnReview = computed(() => {
  return userStore.currentUser?.id === props.review.userId
})

const movie = computed(() => {
  if (!props.showMovieTitle) return null
  return movieStore.movies.find(m => m.id === props.review.movieId)
})

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getRatingStars = (rating: number) => {
  return Array.from({ length: 5 }, (_, i) => i < rating)
}

const handleLike = () => {
  if (!userStore.isAuthenticated) return
  emit('like', props.review.id)
}

const handleDislike = () => {
  if (!userStore.isAuthenticated) return
  emit('dislike', props.review.id)
}

const handleReport = () => {
  if (!userStore.isAuthenticated) return
  emit('report', props.review.id)
}

const handleEdit = () => {
  emit('edit', props.review.id)
}

const handleDelete = () => {
  emit('delete', props.review.id)
}
</script>

<template>
  <div :class="[
    'card bg-base-100 shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200',
    compact ? 'card-compact' : ''
  ]">
    <div :class="compact ? 'card-body p-4' : 'card-body'">
      <!-- Header -->
      <div class="flex items-start justify-between">
        <div class="flex items-center gap-3">
          <!-- User Avatar -->
          <div class="avatar placeholder">
            <div class="bg-primary text-primary-content rounded-full w-10 h-10">
              <span class="text-sm font-bold">
                {{ review.userName.charAt(0).toUpperCase() }}
              </span>
            </div>
          </div>
          
          <!-- User Info -->
          <div>
            <div class="flex items-center gap-2">
              <h4 class="font-semibold text-sm">{{ review.userName }}</h4>
              <div class="flex items-center gap-1">
                <Star 
                  v-for="(filled, index) in getRatingStars(review.lemonPieRating)" 
                  :key="index"
                  :class="[
                    'w-3 h-3',
                    filled ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'
                  ]"
                />
              </div>
              <span class="text-xs text-gray-500">{{ review.lemonPieRating }}/5</span>
            </div>
            
            <div class="flex items-center gap-2 text-xs text-gray-500 mt-1">
              <Calendar class="w-3 h-3" />
              <span>{{ formatDate(review.createdAt) }}</span>
              
              <!-- Movie Title (if shown) -->
              <template v-if="showMovieTitle && movie">
                <span>•</span>
                <span class="font-medium">{{ movie.title }}</span>
              </template>
            </div>
          </div>
        </div>
        
        <!-- Actions Menu -->
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-sm btn-circle">
            <MoreHorizontal class="w-4 h-4" />
          </label>
          <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
            <li v-if="isOwnReview">
              <button @click="handleEdit" class="text-sm">
                <span>Edit Review</span>
              </button>
            </li>
            <li v-if="isOwnReview">
              <button @click="handleDelete" class="text-sm text-error">
                <span>Delete Review</span>
              </button>
            </li>
            <li v-if="!isOwnReview">
              <button @click="handleReport" class="text-sm">
                <Flag class="w-4 h-4" />
                <span>Report Review</span>
              </button>
            </li>
          </ul>
        </div>
      </div>
      
      <!-- Review Content -->
      <div class="mt-3">
        <p :class="[
          'text-gray-700 leading-relaxed',
          compact ? 'text-sm' : 'text-base'
        ]">
          {{ review.reviewText }}
        </p>
      </div>
      
      <!-- Review Actions -->
      <div class="flex items-center justify-between mt-4 pt-3 border-t border-gray-100">
        <div class="flex items-center gap-4">
          <!-- Like Button -->
          <button 
            @click="handleLike"
            :class="[
              'btn btn-ghost btn-sm gap-1',
              false ? 'text-success' : 'text-gray-500'
            ]"
            :disabled="!userStore.isAuthenticated"
          >
            <ThumbsUp class="w-4 h-4" />
            <span class="text-xs">{{ review.helpfulnessScore || 0 }}</span>
          </button>
          
          <!-- Dislike Button -->
          <button 
            @click="handleDislike"
            :class="[
              'btn btn-ghost btn-sm gap-1',
              false ? 'text-error' : 'text-gray-500'
            ]"
            :disabled="!userStore.isAuthenticated"
          >
            <ThumbsDown class="w-4 h-4" />
            <span class="text-xs">0</span>
          </button>
        </div>
        
        <!-- Helpful Indicator -->
        <div v-if="(review.helpfulnessScore || 0) > 0" class="text-xs text-gray-500">
          {{ review.helpfulnessScore }} {{ (review.helpfulnessScore || 0) === 1 ? 'person found' : 'people found' }} this helpful
        </div>
      </div>
    </div>
  </div>
</template>