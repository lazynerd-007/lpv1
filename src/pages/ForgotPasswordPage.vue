<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center p-4">
    <!-- LemonNPie Logo -->
    <div class="absolute top-8 left-1/2 transform -translate-x-1/2 z-10">
      <LemonPieLogo size="lg" />
    </div>

    <!-- Main Content -->
    <div class="w-full max-w-md">
      <!-- Form Container -->
      <div class="bg-gray-800 rounded-lg p-8 shadow-xl">
        <!-- Header Text -->
        <div class="mb-6">
          <p class="text-gray-300 text-sm leading-relaxed">
            Enter your email address below and we will send you a link to reset or create your password.
          </p>
        </div>

        <!-- Form -->
        <form @submit.prevent="handleForgotPassword" class="space-y-6">
          <!-- Email Field -->
          <div>
            <label class="block text-gray-300 text-sm font-medium mb-2">
              Email
            </label>
            <input
              v-model="email"
              type="email"
              class="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
              placeholder="Enter your email"
              required
            />
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full bg-orange-500 hover:bg-orange-600 text-white font-medium py-3 px-4 rounded-lg transition-colors duration-200 focus:outline-none"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></span>
            {{ isLoading ? 'Sending...' : 'Continue' }}
          </button>
        </form>
      </div>

      <!-- Sign Up Link -->
      <div class="text-center mt-6">
        <p class="text-gray-400 text-sm">
          Don't have an account?
          <router-link to="/register" class="text-orange-500 hover:text-orange-400 font-medium">
            Sign up.
          </router-link>
        </p>
      </div>

      <!-- Footer -->
      <div class="text-center mt-16">
        <p class="text-gray-500 text-xs">© LemonNPie</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import LemonPieLogo from '@/components/LemonPieLogo.vue'

const router = useRouter()
const email = ref('')
const isLoading = ref(false)

const handleForgotPassword = async () => {
  isLoading.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock successful password reset request
    console.log('Password reset email sent to:', email.value)
    alert('Password reset link has been sent to your email!')
    
    // Redirect to login
    router.push('/login')
  } catch (error) {
    console.error('Error sending password reset email:', error)
    alert('Failed to send password reset email. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>