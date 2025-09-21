<template>
  <div class="bg-theme-background min-h-screen flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div class="bg-theme-card rounded-lg shadow-md p-8">
        <!-- Logo -->
        <div class="text-center mb-8">
          <LemonPieLogo size="lg" />
        </div>

        <!-- Login Form -->
        <div class="bg-gray-800 rounded-lg p-8 shadow-2xl">
          <h2 class="text-white text-xl font-semibold mb-6 text-center">
            Sign in to your account
          </h2>

          <!-- Error Display -->
          <div v-if="error" class="mb-6 p-4 bg-red-900/50 border border-red-500 rounded-lg">
            <div class="flex items-center">
              <svg class="w-5 h-5 text-red-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
              </svg>
              <p class="text-red-300 text-sm">{{ error }}</p>
            </div>
          </div>

          <form @submit.prevent="handleLogin" class="space-y-6">
            <!-- Email Field -->
            <div>
              <label for="email" class="block text-gray-300 text-sm font-medium mb-2">
                Email
              </label>
              <input 
                id="email"
                v-model="email" 
                type="email" 
                placeholder="admin@admin.com"
                :class="[
                  'w-full bg-gray-700 border rounded-lg px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-1 transition-colors',
                  isEmailValid ? 'border-gray-600 focus:border-orange-500 focus:ring-orange-500' : 'border-red-500 focus:border-red-500 focus:ring-red-500'
                ]"
                required
              />
              <p v-if="!isEmailValid && email" class="mt-1 text-sm text-red-400">
                Please enter a valid email address
              </p>
            </div>

            <!-- Password Field -->
            <div>
              <div class="flex justify-between items-center mb-2">
                <label for="password" class="block text-gray-300 text-sm font-medium">
                  Password
                </label>
                <router-link to="/forgot-password" class="text-orange-500 text-sm hover:text-orange-400 transition-colors">
                  Forgot your password?
                </router-link>
              </div>
              <div class="relative">
                <input 
                  id="password"
                  v-model="password" 
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="••••••••"
                  class="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 pr-12 text-white placeholder-gray-400 focus:outline-none focus:border-orange-500 focus:ring-1 focus:ring-orange-500 transition-colors" 
                  required
                />
                <button
                  type="button"
                  @click="showPassword = !showPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-300"
                >
                  <svg v-if="showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L3 3m6.878 6.878L21 21"></path>
                  </svg>
                  <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                  </svg>
                </button>
              </div>
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
              :disabled="isLoading || !isFormValid"
              :class="[
                'w-full font-semibold py-3 px-4 rounded-lg transition-colors flex items-center justify-center',
                isFormValid && !isLoading 
                  ? 'bg-orange-600 hover:bg-orange-700 text-white' 
                  : 'bg-gray-600 cursor-not-allowed text-gray-400'
              ]"
            >
              <svg v-if="isLoading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ isLoading ? 'Signing In...' : 'Sign In' }}
            </button>
            
            <!-- Testing Buttons (Development Only) -->
            <div class="mt-6 p-4 bg-gray-800 rounded-lg border border-gray-600">
              <h3 class="text-sm font-medium text-gray-300 mb-3">Quick Test Logins:</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                <button
                  type="button"
                  @click="quickLogin('admin@admin.com', 'admin123')"
                  class="px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded transition-colors"
                  :disabled="isLoading"
                >
                  ✓ Admin Login
                </button>
                <button
                  type="button"
                  @click="quickLogin('user@test.com', 'password123')"
                  class="px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
                  :disabled="isLoading"
                >
                  ✓ User Login
                </button>
                <button
                  type="button"
                  @click="quickLogin('user@test.com', 'wrongpassword')"
                  class="px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded transition-colors"
                  :disabled="isLoading"
                >
                  ✗ Wrong Password
                </button>
                <button
                  type="button"
                  @click="quickLogin('locked@test.com', 'locked123')"
                  class="px-3 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded transition-colors"
                  :disabled="isLoading"
                >
                  🔒 Locked Account
                </button>
                <button
                  type="button"
                  @click="quickLogin('inactive@test.com', 'inactive123')"
                  class="px-3 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded transition-colors"
                  :disabled="isLoading"
                >
                  ⏸ Inactive Account
                </button>
                <button
                  type="button"
                  @click="quickLogin('nonexistent@test.com', 'password')"
                  class="px-3 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded transition-colors"
                  :disabled="isLoading"
                >
                  👻 Non-existent User
                </button>
              </div>
              <p class="text-xs text-gray-400 mt-2">
                These buttons are for testing different authentication scenarios.
              </p>
            </div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { AuthError } from '@/data/mockAuth'
import LemonPieLogo from '@/components/LemonPieLogo.vue'

const router = useRouter()
const userStore = useUserStore()

const email = ref('admin@admin.com')
const password = ref('')
const rememberMe = ref(true)
const isLoading = ref(false)
const error = ref('')
const showPassword = ref(false)

// Computed properties for validation
const isEmailValid = computed(() => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return email.value === '' || emailRegex.test(email.value)
})

const isFormValid = computed(() => {
  return email.value.trim() !== '' && password.value.trim() !== '' && isEmailValid.value
})

// Error message formatting
const getErrorMessage = (authError: any) => {
  if (!authError) return ''
  
  switch (authError.type) {
    case AuthError.INVALID_CREDENTIALS:
      return authError.message + (authError.details?.attemptsRemaining ? 
        ` (${authError.details.attemptsRemaining} attempts remaining)` : '')
    case AuthError.ACCOUNT_LOCKED:
      return authError.message
    case AuthError.ACCOUNT_INACTIVE:
      return authError.message + ' Contact: ' + authError.details?.contactEmail
    case AuthError.TOO_MANY_ATTEMPTS:
      return authError.message
    case AuthError.VALIDATION_ERROR:
      return authError.message
    case AuthError.SERVER_ERROR:
      return authError.message
    default:
      return 'An unexpected error occurred. Please try again.'
  }
}

const handleLogin = async () => {
  if (!isFormValid.value) {
    error.value = 'Please fill in all fields correctly'
    return
  }
  
  isLoading.value = true
  error.value = ''
  
  try {
    const result = await userStore.login(email.value.trim(), password.value)
    
    if (result.success) {
      console.log('Login successful:', {
        user: result.user?.name,
        email: email.value,
        rememberMe: rememberMe.value
      })
      
      // Store remember me preference
      if (rememberMe.value) {
        localStorage.setItem('remember_email', email.value)
      } else {
        localStorage.removeItem('remember_email')
      }
      
      // Redirect to home or intended page
      const redirectTo = router.currentRoute.value.query.redirect as string || '/'
      router.push(redirectTo)
    } else {
      error.value = getErrorMessage(result.error)
      
      // Clear password on certain errors
      if (result.error?.type === AuthError.INVALID_CREDENTIALS || 
          result.error?.type === AuthError.ACCOUNT_LOCKED) {
        password.value = ''
      }
    }
  } catch (err) {
    console.error('Login error:', err)
    error.value = 'Network error. Please check your connection and try again.'
  } finally {
    isLoading.value = false
  }
}

// Load remembered email on component mount
const rememberedEmail = localStorage.getItem('remember_email')
if (rememberedEmail) {
  email.value = rememberedEmail
  rememberMe.value = true
}

// Quick login helpers for testing
const quickLogin = (testEmail: string, testPassword: string) => {
  email.value = testEmail
  password.value = testPassword
  handleLogin()
}
</script>