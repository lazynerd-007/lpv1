<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 flex items-center justify-center">
    <div class="container mx-auto px-4 py-8">
      <div class="max-w-md mx-auto">
        <!-- Logo/Brand -->
        <div class="text-center mb-8">
          <h1 class="text-4xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-yellow-600 to-orange-600 mb-2">
            LemonNPie
          </h1>
          <p class="text-gray-600">Welcome back to Nollywood's home!</p>
        </div>

        <!-- Login Form -->
        <div class="card bg-white shadow-xl">
          <div class="card-body">
            <h2 class="card-title text-2xl mb-6 justify-center text-gray-800">
              <LogIn class="w-6 h-6" />
              Sign In
            </h2>

            <form @submit.prevent="handleLogin">
              <!-- Email Field -->
              <div class="form-control mb-4">
                <label class="label">
                  <span class="label-text font-semibold">Email Address</span>
                </label>
                <div class="input-group">
                  <span class="bg-gray-100 border border-r-0 border-gray-300 px-3 flex items-center rounded-l-lg">
                    <Mail class="w-4 h-4 text-gray-500" />
                  </span>
                  <input 
                    v-model="email" 
                    type="email" 
                    placeholder="your@email.com" 
                    class="input input-bordered flex-1 rounded-l-none" 
                    required
                  />
                </div>
              </div>

              <!-- Password Field -->
              <div class="form-control mb-6">
                <label class="label">
                  <span class="label-text font-semibold">Password</span>
                </label>
                <div class="input-group">
                  <span class="bg-gray-100 border border-r-0 border-gray-300 px-3 flex items-center rounded-l-lg">
                    <Lock class="w-4 h-4 text-gray-500" />
                  </span>
                  <input 
                    v-model="password" 
                    :type="showPassword ? 'text' : 'password'" 
                    placeholder="Enter your password" 
                    class="input input-bordered flex-1 rounded-none" 
                    required
                  />
                  <button 
                    type="button"
                    @click="showPassword = !showPassword"
                    class="bg-gray-100 border border-l-0 border-gray-300 px-3 flex items-center rounded-r-lg hover:bg-gray-200"
                  >
                    <Eye v-if="!showPassword" class="w-4 h-4 text-gray-500" />
                    <EyeOff v-else class="w-4 h-4 text-gray-500" />
                  </button>
                </div>
              </div>

              <!-- Remember Me & Forgot Password -->
              <div class="flex justify-between items-center mb-6">
                <label class="cursor-pointer label">
                  <input 
                    v-model="rememberMe" 
                    type="checkbox" 
                    class="checkbox checkbox-primary checkbox-sm" 
                  />
                  <span class="label-text ml-2">Remember me</span>
                </label>
                <a href="#" class="link link-primary text-sm">Forgot password?</a>
              </div>

              <!-- Submit Button -->
              <button 
                type="submit" 
                class="btn btn-primary w-full mb-4"
                :disabled="isLoading"
              >
                <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
                <LogIn v-else class="w-4 h-4 mr-2" />
                {{ isLoading ? 'Signing In...' : 'Sign In' }}
              </button>
            </form>

            <!-- Divider -->
            <div class="divider">OR</div>

            <!-- Social Login -->
            <div class="space-y-3">
              <button class="btn btn-outline w-full">
                <svg class="w-4 h-4 mr-2" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Continue with Google
              </button>
              
              <button class="btn btn-outline w-full">
                <Facebook class="w-4 h-4 mr-2" />
                Continue with Facebook
              </button>
            </div>

            <!-- Sign Up Link -->
            <div class="text-center mt-6">
              <p class="text-gray-600">
                Don't have an account? 
                <router-link to="/register" class="link link-primary font-semibold">
                  Sign up here
                </router-link>
              </p>
            </div>
          </div>
        </div>

        <!-- Features -->
        <div class="mt-8 text-center">
          <p class="text-gray-600 mb-4">Join thousands of Nollywood fans!</p>
          <div class="flex justify-center gap-6 text-sm text-gray-500">
            <div class="flex items-center gap-1">
              <Star class="w-4 h-4 text-yellow-500" />
              <span>Rate Movies</span>
            </div>
            <div class="flex items-center gap-1">
              <MessageSquare class="w-4 h-4 text-blue-500" />
              <span>Write Reviews</span>
            </div>
            <div class="flex items-center gap-1">
              <Users class="w-4 h-4 text-green-500" />
              <span>Connect with Fans</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { 
  LogIn, 
  Mail, 
  Lock, 
  Eye, 
  EyeOff, 
  Star, 
  MessageSquare, 
  Users,
  Facebook 
} from 'lucide-vue-next'

const router = useRouter()

const email = ref('')
const password = ref('')
const rememberMe = ref(false)
const showPassword = ref(false)
const isLoading = ref(false)

const handleLogin = async () => {
  isLoading.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    // Mock successful login
    console.log('Login successful:', { email: email.value, rememberMe: rememberMe.value })
    
    // Redirect to dashboard or home
    router.push('/')
  } catch (error) {
    console.error('Login failed:', error)
    alert('Login failed. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>