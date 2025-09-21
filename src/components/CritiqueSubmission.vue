<template>
  <div class="critique-submission">
    <!-- Access Control Check -->
    <div v-if="!userStore.canSubmitCritique()" class="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4 mb-6">
      <div class="flex items-center">
        <svg class="w-5 h-5 text-yellow-600 dark:text-yellow-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
        </svg>
        <div>
          <h3 class="text-sm font-medium text-yellow-800 dark:text-yellow-200">Access Restricted</h3>
          <p class="text-sm text-yellow-700 dark:text-yellow-300 mt-1">
            Only users with the 'Critic' role can submit critiques. Contact an administrator to request critic access.
          </p>
        </div>
      </div>
    </div>

    <!-- Critique Submission Form -->
    <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div class="flex items-center mb-6">
        <div class="bg-purple-100 dark:bg-purple-900/30 p-2 rounded-lg mr-3">
          <svg class="w-6 h-6 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
          </svg>
        </div>
        <div>
          <h2 class="text-xl font-bold text-gray-900 dark:text-white">Submit Professional Critique</h2>
          <p class="text-sm text-gray-600 dark:text-gray-400">Share your expert analysis and professional review</p>
        </div>
      </div>

      <form @submit.prevent="submitCritique" class="space-y-6">
        <!-- Movie Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Movie/Series</label>
          <select 
            v-model="critiqueData.movieId" 
            required
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
          >
            <option value="">Select a movie or series...</option>
            <option value="inception">Inception (2010)</option>
            <option value="dark-knight">The Dark Knight (2008)</option>
            <option value="pulp-fiction">Pulp Fiction (1994)</option>
            <option value="godfather">The Godfather (1972)</option>
          </select>
        </div>

        <!-- Critique Title -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Critique Title</label>
          <input
            v-model="critiqueData.title"
            type="text"
            required
            placeholder="Enter a compelling title for your critique"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white"
          />
        </div>

        <!-- Professional Rating -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Professional Rating</label>
          <div class="flex items-center space-x-4">
            <input
              v-model.number="critiqueData.rating"
              type="range"
              min="1"
              max="10"
              step="0.1"
              class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            />
            <span class="text-lg font-semibold text-purple-600 dark:text-purple-400 min-w-[3rem]">
              {{ critiqueData.rating }}/10
            </span>
          </div>
        </div>

        <!-- Critique Categories -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">Critique Focus Areas</label>
          <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
            <label v-for="category in critiqueCategories" :key="category.id" class="flex items-center">
              <input
                v-model="critiqueData.categories"
                :value="category.id"
                type="checkbox"
                class="rounded border-gray-300 text-purple-600 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50"
              />
              <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">{{ category.label }}</span>
            </label>
          </div>
        </div>

        <!-- Critique Content -->
        <div>
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Professional Analysis</label>
          <textarea
            v-model="critiqueData.content"
            required
            rows="8"
            placeholder="Provide your detailed professional critique, including technical analysis, artistic merit, and industry perspective..."
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 dark:bg-gray-700 dark:text-white resize-vertical"
          ></textarea>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Minimum 200 characters. Current: {{ critiqueData.content.length }}
          </p>
        </div>

        <!-- Spoiler Warning -->
        <div class="flex items-center">
          <input
            v-model="critiqueData.containsSpoilers"
            type="checkbox"
            id="spoilers"
            class="rounded border-gray-300 text-purple-600 shadow-sm focus:border-purple-300 focus:ring focus:ring-purple-200 focus:ring-opacity-50"
          />
          <label for="spoilers" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
            This critique contains spoilers
          </label>
        </div>

        <!-- Submit Button -->
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="resetForm"
            class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-200 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200"
          >
            Reset
          </button>
          <button
            type="submit"
            :disabled="!isFormValid || isSubmitting"
            class="px-6 py-2 text-sm font-medium text-white bg-purple-600 border border-transparent rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            <span v-if="isSubmitting" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Submitting...
            </span>
            <span v-else>Submit Critique</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useNotificationStore } from '@/stores/notificationStore'

const userStore = useUserStore()
const notificationStore = useNotificationStore()

const isSubmitting = ref(false)

const critiqueData = reactive({
  movieId: '',
  title: '',
  rating: 7.5,
  categories: [] as string[],
  content: '',
  containsSpoilers: false
})

const critiqueCategories = [
  { id: 'cinematography', label: 'Cinematography' },
  { id: 'acting', label: 'Acting Performance' },
  { id: 'direction', label: 'Direction' },
  { id: 'screenplay', label: 'Screenplay' },
  { id: 'editing', label: 'Editing' },
  { id: 'sound', label: 'Sound Design' },
  { id: 'production', label: 'Production Design' },
  { id: 'music', label: 'Musical Score' },
  { id: 'technical', label: 'Technical Aspects' }
]

const isFormValid = computed(() => {
  return critiqueData.movieId && 
         critiqueData.title.trim() && 
         critiqueData.content.trim().length >= 200 &&
         critiqueData.categories.length > 0
})

const submitCritique = async () => {
  if (!userStore.canSubmitCritique()) {
    notificationStore.addNotification({
      title: 'Access Denied',
      message: 'You do not have permission to submit critiques.',
      type: 'error',
      isRead: false
    })
    return
  }

  if (!isFormValid.value) {
    notificationStore.addNotification({
      title: 'Form Incomplete',
      message: 'Please fill in all required fields and ensure your critique is at least 200 characters.',
      type: 'warning',
      isRead: false
    })
    return
  }

  isSubmitting.value = true

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Here you would typically send the critique to your backend
    console.log('Submitting critique:', critiqueData)
    
    notificationStore.addNotification({
      title: 'Critique Submitted Successfully',
      message: `Your professional critique "${critiqueData.title}" has been submitted for review.`,
      type: 'success',
      isRead: false
    })
    
    resetForm()
  } catch (error) {
    notificationStore.addNotification({
      title: 'Submission Failed',
      message: 'There was an error submitting your critique. Please try again.',
      type: 'error',
      isRead: false
    })
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  critiqueData.movieId = ''
  critiqueData.title = ''
  critiqueData.rating = 7.5
  critiqueData.categories = []
  critiqueData.content = ''
  critiqueData.containsSpoilers = false
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>