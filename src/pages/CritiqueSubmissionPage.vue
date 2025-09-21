<template>
  <div class="critique-submission-page min-h-screen bg-gray-50 dark:bg-gray-900 py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Submit Professional Critique</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">
          Share your professional analysis and insights about Nollywood films
        </p>
      </div>

      <!-- Role Verification -->
      <RoleBasedAccess required-role="critic">
        <CritiqueSubmission />
      </RoleBasedAccess>

      <!-- Access Denied Message -->
      <div v-if="!userStore.isCritic()" class="bg-white dark:bg-gray-800 shadow rounded-lg p-8 text-center">
        <div class="mb-6">
          <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L4.082 16.5c-.77.833.192 2.5 1.732 2.5z" />
          </svg>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Access Restricted</h2>
          <p class="text-gray-600 dark:text-gray-400 mb-6">
            This feature is exclusively available to users with the 'Critic' role. 
            Professional critique submission requires special permissions to maintain content quality.
          </p>
          <div class="space-y-4">
            <p class="text-sm text-gray-500 dark:text-gray-400">
              If you believe you should have critic access, please contact an administrator.
            </p>
            <div class="flex justify-center space-x-4">
              <router-link 
                to="/movies" 
                class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md font-medium transition-colors"
              >
                Browse Movies
              </router-link>
              <router-link 
                to="/settings" 
                class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-2 rounded-md font-medium transition-colors"
              >
                Account Settings
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import CritiqueSubmission from '@/components/CritiqueSubmission.vue'
import RoleBasedAccess from '@/components/RoleBasedAccess.vue'

const userStore = useUserStore()
const uiStore = useUIStore()

onMounted(() => {
  uiStore.setPageTitle('Submit Critique - LemonNPie')
})
</script>

<style scoped>
.critique-submission-page {
  /* Page-specific styles if needed */
}
</style>