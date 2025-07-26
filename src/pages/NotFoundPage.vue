<template>
  <div class="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 flex items-center justify-center p-4">
    <div class="text-center">
      <!-- 404 Illustration -->
      <div class="mb-8">
        <div class="text-9xl font-bold text-primary opacity-20 mb-4">404</div>
        <div class="relative">
          <Film class="w-24 h-24 mx-auto text-primary mb-4" />
          <div class="absolute -top-2 -right-2">
            <AlertCircle class="w-8 h-8 text-error" />
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div class="max-w-md mx-auto mb-8">
        <h1 class="text-4xl font-bold text-base-content mb-4">
          Oops! Movie Not Found
        </h1>
        <p class="text-lg text-base-content/70 mb-6">
          The page you're looking for seems to have gone off-screen. 
          Maybe it's taking a break between scenes?
        </p>
        <p class="text-base text-base-content/60">
          Don't worry, there are plenty of other great Nollywood movies to discover!
        </p>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <router-link to="/" class="btn btn-primary btn-lg">
          <Home class="w-5 h-5 mr-2" />
          Back to Home
        </router-link>
        
        <router-link to="/browse" class="btn btn-outline btn-lg">
          <Search class="w-5 h-5 mr-2" />
          Browse Movies
        </router-link>
      </div>

      <!-- Helpful Links -->
      <div class="mt-12">
        <p class="text-sm text-base-content/60 mb-4">Or try one of these:</p>
        <div class="flex flex-wrap gap-2 justify-center">
          <router-link to="/search" class="link link-primary text-sm">
            Search Movies
          </router-link>
          <span class="text-base-content/40">•</span>
          <router-link to="/write-review" class="link link-primary text-sm">
            Write a Review
          </router-link>
          <span class="text-base-content/40">•</span>
          <router-link to="/about" class="link link-primary text-sm">
            About Us
          </router-link>
        </div>
      </div>

      <!-- Fun Nollywood Quote -->
      <div class="mt-12 max-w-lg mx-auto">
        <div class="card bg-base-200 shadow-sm">
          <div class="card-body py-6">
            <Quote class="w-6 h-6 text-primary mx-auto mb-2" />
            <p class="text-sm italic text-base-content/80">
              "Even the best directors sometimes lose their way, but they always find their path back to great storytelling."
            </p>
            <p class="text-xs text-base-content/60 mt-2">- Nollywood Wisdom</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Film, AlertCircle, Home, Search, Quote } from 'lucide-vue-next'
</script>

<style scoped>
/* Additional custom styles if needed */
</style>