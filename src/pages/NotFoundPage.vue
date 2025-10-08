<template>
  <div class="min-h-screen bg-gradient-to-br from-theme-primary/5 via-theme-background to-theme-secondary/5 flex items-center justify-center p-4">
    <div class="text-center">
      <!-- 404 Illustration -->
      <div class="mb-8">
        <div class="text-9xl font-bold text-theme-primary/20 mb-4">404</div>
        <div class="relative">
          <div class="flex items-center justify-center mb-4">
            <Film class="w-20 h-20 text-theme-primary mr-2" />
            <div class="text-4xl font-bold text-theme-primary">🍋🥧</div>
          </div>
          <div class="absolute -top-2 -right-2">
            <AlertCircle class="w-8 h-8 text-red-500" />
          </div>
        </div>
      </div>

      <!-- Error Message -->
      <div class="max-w-lg mx-auto mb-8">
        <h1 class="text-4xl font-bold text-theme-text mb-4">
          Oya! This Page Don Disappear! 🎬
        </h1>
        <p class="text-lg text-theme-text-muted mb-6">
          The page you're looking for has vanished like a Nollywood plot twist! 
          Maybe it went to shoot a new scene in Asaba? 🎭
        </p>
        <p class="text-base text-theme-text-muted">
          No wahala! LemonNPie has plenty of sweet Nollywood content waiting for you to discover.
        </p>
        <div class="mt-4 p-4 bg-theme-primary/10 rounded-lg border border-theme-primary/20">
          <p class="text-sm text-theme-text-muted italic">
            "In Nollywood, every ending is just the beginning of another story!" 🌟
          </p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
        <router-link to="/" class="bg-theme-primary text-white px-6 py-3 rounded-lg font-semibold hover:bg-theme-primary/90 transition-colors flex items-center">
          <Home class="w-5 h-5 mr-2" />
          Return to LemonNPie Home
        </router-link>
        
        <router-link to="/movies" class="border-2 border-theme-primary text-theme-primary px-6 py-3 rounded-lg font-semibold hover:bg-theme-primary hover:text-white transition-colors flex items-center">
          <Search class="w-5 h-5 mr-2" />
          Discover Nollywood Movies
        </router-link>
      </div>

      <!-- Helpful Links -->
      <div class="mt-12">
        <p class="text-sm text-theme-text-muted mb-6">Or explore these sweet options:</p>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto">
          <router-link to="/search" class="bg-theme-surface border border-theme-border rounded-lg p-4 hover:bg-theme-primary/5 transition-colors group">
            <Search class="w-6 h-6 text-theme-primary mx-auto mb-2" />
            <p class="text-sm font-medium text-theme-text group-hover:text-theme-primary">Search Movies</p>
            <p class="text-xs text-theme-text-muted mt-1">Find your favorite Nollywood films</p>
          </router-link>
          
          <router-link to="/write-review" class="bg-theme-surface border border-theme-border rounded-lg p-4 hover:bg-theme-primary/5 transition-colors group">
            <PenTool class="w-6 h-6 text-theme-primary mx-auto mb-2" />
            <p class="text-sm font-medium text-theme-text group-hover:text-theme-primary">Write Review</p>
            <p class="text-xs text-theme-text-muted mt-1">Share your movie experience</p>
          </router-link>
          
          <router-link to="/about" class="bg-theme-surface border border-theme-border rounded-lg p-4 hover:bg-theme-primary/5 transition-colors group">
            <Users class="w-6 h-6 text-theme-primary mx-auto mb-2" />
            <p class="text-sm font-medium text-theme-text group-hover:text-theme-primary">About LemonNPie</p>
            <p class="text-xs text-theme-text-muted mt-1">Learn about our mission</p>
          </router-link>
        </div>
      </div>

      <!-- Fun Nollywood Quote -->
      <div class="mt-12 max-w-lg mx-auto">
        <div class="bg-gradient-to-r from-theme-primary/10 to-theme-secondary/10 border border-theme-primary/20 rounded-lg shadow-sm">
          <div class="p-6">
            <Quote class="w-6 h-6 text-theme-primary mx-auto mb-3" />
            <p class="text-sm italic text-theme-text-muted leading-relaxed">
              "No be every story get happy ending, but every ending na beginning of another story. Na so Nollywood dey work!"
            </p>
            <p class="text-xs text-theme-text-muted mt-3 font-medium">- Nigerian Film Wisdom 🎭</p>
            <div class="mt-4 flex items-center justify-center space-x-2">
              <Star class="w-4 h-4 text-yellow-400 fill-current" />
              <Star class="w-4 h-4 text-yellow-400 fill-current" />
              <Star class="w-4 h-4 text-yellow-400 fill-current" />
              <Star class="w-4 h-4 text-yellow-400 fill-current" />
              <Star class="w-4 h-4 text-yellow-400 fill-current" />
              <span class="text-xs text-theme-text-muted ml-2">5-Star Nollywood Experience</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Film, AlertCircle, Home, Search, Quote, PenTool, Users, Star } from 'lucide-vue-next'

// Set page title
if (typeof document !== 'undefined') {
  document.title = '404 - Page Not Found | LemonNPie - Your Sweet Spot for Nollywood Reviews'
}
</script>

<style scoped>
/* Additional custom styles if needed */
</style>