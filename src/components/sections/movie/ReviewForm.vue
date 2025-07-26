<template>
  <div class="card bg-gray-800 shadow-lg">
    <div class="card-body">
      <h2 class="card-title text-2xl mb-6 text-white">
        <PenTool class="w-6 h-6" />
        Your Review
      </h2>

      <form @submit.prevent="handleSubmit">
        <!-- Rating Section -->
        <RatingSelector 
          :rating="formData.rating" 
          @update:rating="formData.rating = $event" 
        />

        <!-- Review Title -->
        <div class="form-control mb-4">
          <label class="label">
            <span class="label-text font-semibold text-gray-300">Review Title</span>
          </label>
          <input 
            v-model="formData.title" 
            type="text" 
            placeholder="Give your review a catchy title..." 
            class="input input-bordered bg-gray-700 text-white border-gray-600" 
            required
          />
        </div>

        <!-- Review Content -->
        <div class="form-control mb-6">
          <label class="label">
            <span class="label-text font-semibold text-gray-300">Your Review</span>
            <span class="label-text-alt text-gray-400">{{ formData.content.length }}/1000 characters</span>
          </label>
          <textarea 
            v-model="formData.content" 
            class="textarea textarea-bordered h-32 bg-gray-700 text-white border-gray-600" 
            placeholder="Share your thoughts about the movie. What did you like or dislike? How was the acting, plot, cinematography?..."
            maxlength="1000"
            required
          ></textarea>
        </div>

        <!-- Spoiler Warning -->
        <div class="form-control mb-6">
          <label class="cursor-pointer label">
            <span class="label-text font-semibold text-gray-300">Contains Spoilers</span>
            <input 
              v-model="formData.containsSpoilers" 
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
              <span class="label-text font-semibold text-gray-300">Your Name</span>
            </label>
            <input 
              v-model="formData.reviewerName" 
              type="text" 
              placeholder="Enter your name" 
              class="input input-bordered bg-gray-700 text-white border-gray-600" 
              required
            />
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text font-semibold text-gray-300">Email (optional)</span>
            </label>
            <input 
              v-model="formData.reviewerEmail" 
              type="email" 
              placeholder="your@email.com" 
              class="input input-bordered bg-gray-700 text-white border-gray-600"
            />
          </div>
        </div>

        <!-- Submit Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-end">
          <button 
            type="button" 
            @click="handleReset" 
            class="btn btn-outline border-yellow-500 text-yellow-500 hover:bg-yellow-500 hover:text-black"
          >
            <RotateCcw class="w-4 h-4 mr-2" />
            Reset Form
          </button>
          <button 
            type="submit" 
            class="btn bg-yellow-500 hover:bg-yellow-400 text-black border-yellow-500"
            :disabled="!isFormValid"
          >
            <Send class="w-4 h-4 mr-2" />
            Submit Review
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive } from 'vue'
import { PenTool, RotateCcw, Send } from 'lucide-vue-next'
import RatingSelector from './RatingSelector.vue'
import type { Movie } from '@/data/mockMovies'

interface ReviewFormData {
  rating: number
  title: string
  content: string
  containsSpoilers: boolean
  reviewerName: string
  reviewerEmail: string
}

interface Props {
  selectedMovie: Movie | null
}

interface Emits {
  (e: 'submit', data: ReviewFormData): void
  (e: 'reset'): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const formData = reactive<ReviewFormData>({
  rating: 5,
  title: '',
  content: '',
  containsSpoilers: false,
  reviewerName: '',
  reviewerEmail: ''
})

const isFormValid = computed(() => {
  return formData.title.trim() && 
         formData.content.trim() && 
         formData.reviewerName.trim()
})

const handleSubmit = () => {
  if (!isFormValid.value) return
  emit('submit', { ...formData })
}

const handleReset = () => {
  formData.rating = 5
  formData.title = ''
  formData.content = ''
  formData.containsSpoilers = false
  formData.reviewerName = ''
  formData.reviewerEmail = ''
  emit('reset')
}

// Expose reset method for parent component
defineExpose({
  reset: handleReset
})
</script>