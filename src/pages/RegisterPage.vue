<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 flex items-center justify-center p-4">
    <div class="card w-full max-w-md bg-base-100 shadow-xl">
      <div class="card-body">
        <!-- Header -->
        <div class="text-center mb-6">
          <h1 class="text-3xl font-bold text-primary mb-2">Join Lemon & Pie</h1>
          <p class="text-base-content/70">Create your account to start reviewing Nollywood movies</p>
        </div>

        <!-- Registration Form -->
        <form @submit.prevent="handleRegister" class="space-y-4">
          <!-- Full Name -->
          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Full Name</span>
            </label>
            <input
              v-model="form.fullName"
              type="text"
              placeholder="Enter your full name"
              class="input input-bordered w-full"
              required
            />
          </div>

          <!-- Email -->
          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Email</span>
            </label>
            <input
              v-model="form.email"
              type="email"
              placeholder="Enter your email"
              class="input input-bordered w-full"
              required
            />
          </div>

          <!-- Username -->
          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Username</span>
            </label>
            <input
              v-model="form.username"
              type="text"
              placeholder="Choose a username"
              class="input input-bordered w-full"
              required
            />
          </div>

          <!-- Password -->
          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Password</span>
            </label>
            <div class="relative">
              <input
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                placeholder="Create a password"
                class="input input-bordered w-full pr-12"
                required
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-base-content/50 hover:text-base-content"
              >
                <Eye v-if="!showPassword" class="w-5 h-5" />
                <EyeOff v-else class="w-5 h-5" />
              </button>
            </div>
          </div>

          <!-- Confirm Password -->
          <div class="form-control">
            <label class="label">
              <span class="label-text font-medium">Confirm Password</span>
            </label>
            <input
              v-model="form.confirmPassword"
              type="password"
              placeholder="Confirm your password"
              class="input input-bordered w-full"
              required
            />
          </div>

          <!-- Terms and Conditions -->
          <div class="form-control">
            <label class="label cursor-pointer justify-start gap-3">
              <input
                v-model="form.agreeToTerms"
                type="checkbox"
                class="checkbox checkbox-primary"
                required
              />
              <span class="label-text">
                I agree to the
                <a href="#" class="link link-primary">Terms of Service</a>
                and
                <a href="#" class="link link-primary">Privacy Policy</a>
              </span>
            </label>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="btn btn-primary w-full"
            :disabled="isLoading"
          >
            <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
            {{ isLoading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="divider">or</div>

        <!-- Social Registration -->
        <div class="space-y-3">
          <button class="btn btn-outline w-full">
            <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
              <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
              <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
              <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
              <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Continue with Google
          </button>
          
          <button class="btn btn-outline w-full">
            <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
              <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
            </svg>
            Continue with Facebook
          </button>
        </div>

        <!-- Login Link -->
        <div class="text-center mt-6">
          <p class="text-base-content/70">
            Already have an account?
            <router-link to="/login" class="link link-primary font-medium">
              Sign in here
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()

const form = ref({
  fullName: '',
  email: '',
  username: '',
  password: '',
  confirmPassword: '',
  agreeToTerms: false
})

const showPassword = ref(false)
const isLoading = ref(false)

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    alert('Passwords do not match!')
    return
  }

  if (!form.value.agreeToTerms) {
    alert('Please agree to the terms and conditions')
    return
  }

  isLoading.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Mock successful registration
    console.log('Registration successful:', form.value)
    
    // Redirect to login or dashboard
    router.push('/login')
  } catch (error) {
    console.error('Registration failed:', error)
    alert('Registration failed. Please try again.')
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>