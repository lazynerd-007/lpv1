<template>
  <div class="min-h-screen bg-gray-900 flex items-center justify-center px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="flex items-center justify-center gap-2 text-2xl font-bold mb-2">
          <span class="text-white">MTDB</span>
        </div>
      </div>

      <!-- Login Form -->
      <div class="bg-gray-800 rounded-lg p-8 shadow-2xl">
        <h2 class="text-white text-xl font-semibold mb-6 text-center">
          Sign in to your account
        </h2>

        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Email Field -->
          <div>
            <label class="block text-gray-300 text-sm font-medium mb-2">
              Email
            </label>
            <input 
              v-model="email" 
              type="email" 
              placeholder="admin@admin.com"
              class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-colors" 
              required
            />
          </div>

          <!-- Password Field -->
          <div>
            <div class="flex justify-between items-center mb-2">
              <label class="block text-gray-300 text-sm font-medium">
                Password
              </label>
              <router-link to="/forgot-password" class="text-orange-500 text-sm hover:text-orange-400 transition-colors">
                Forgot your password?
              </router-link>
            </div>
            <input 
              v-model="password" 
              type="password" 
              placeholder="••••••••"
              class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-colors" 
              required
            />
          </div>

          <!-- Remember Me -->
          <div class="flex items-center">
            <input 
              v-model="rememberMe" 
              type="checkbox" 
              id="remember"
              class="w-4 h-4 text-orange-500 bg-gray-700 border-gray-600 rounded focus:ring-orange-500 focus:ring-2"
            />
            <label for="remember" class="ml-2 text-sm text-gray-300">
              Stay signed in for a month
            </label>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit" 
            class="w-full bg-orange-500 hover:bg-orange-600 text-white font-medium py-3 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-gray-800"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></span>
            {{ isLoading ? 'Signing In...' : 'Continue' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="my-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-600"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-gray-800 text-gray-400">Or sign in with</span>
            </div>
          </div>
        </div>

        <!-- Social Login -->
        <div class="grid grid-cols-3 gap-3">
          <button class="flex justify-center items-center px-4 py-2 border border-gray-600 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors">
            <svg class="w-5 h-5 text-white" viewBox="0 0 24 24">
              <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
          </button>
          
          <button class="flex justify-center items-center px-4 py-2 border border-gray-600 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
          </button>
          
          <button class="flex justify-center items-center px-4 py-2 border border-gray-600 rounded-lg bg-gray-700 hover:bg-gray-600 transition-colors">
            <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Sign Up Link -->
      <div class="text-center mt-6">
        <p class="text-gray-400">
          Don't have an account? 
          <router-link to="/register" class="text-orange-500 hover:text-orange-400 transition-colors font-medium">
            Sign up
          </router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('admin@admin.com')
const password = ref('')
const rememberMe = ref(true)
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Mock successful login
    console.log('Login successful:', { email: email.value, rememberMe: rememberMe.value })
    
    // Redirect to home
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
    alert('Login failed. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>