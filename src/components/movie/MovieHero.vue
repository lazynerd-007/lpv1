<script setup lang="ts">
import { computed } from 'vue'
import { Star, Clock, Calendar, MapPin, Play, Heart, Share2 } from 'lucide-vue-next'
import type { Movie } from '@/data/mockMovies'

interface Props {
  movie: Movie
  averageRating: number
  isInWatchlist: boolean
  isInFavorites: boolean
}

interface Emits {
  playTrailer: []
  toggleWatchlist: []
  toggleFavorites: []
  shareMovie: []
}

defineProps<Props>()
defineEmits<Emits>()
</script>

<template>
  <div class="relative h-screen">
    <div class="absolute inset-0">
      <img
        :src="movie.poster"
        :alt="movie.title"
        class="w-full h-full object-cover"
      />
      <div class="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/60 to-transparent"></div>
    </div>
    
    <div class="relative z-10 flex items-end h-full">
      <div class="container mx-auto px-4 pb-20">
        <div class="max-w-4xl">
          <h1 class="text-5xl md:text-7xl font-bold mb-4">{{ movie.title }}</h1>
          <div class="flex items-center gap-6 mb-6 text-lg">
            <div class="flex items-center gap-2">
              <Clock class="w-5 h-5" />
              <span>{{ movie.runtime }} min</span>
            </div>
            <div class="flex items-center gap-2">
              <Calendar class="w-5 h-5" />
              <span>{{ movie.releaseDate }}</span>
            </div>
            <div class="flex items-center gap-2">
              <MapPin class="w-5 h-5" />
              <span>{{ movie.productionState }}</span>
            </div>
            <div class="flex items-center gap-2">
              <Star class="w-5 h-5 text-yellow-400" />
              <span>{{ averageRating.toFixed(1) }}/5</span>
            </div>
          </div>
          <p class="text-xl mb-8 max-w-2xl leading-relaxed">{{ movie.plotSummary }}</p>
          
          <!-- Action Buttons -->
          <div class="flex items-center gap-4">
            <button
              @click="$emit('playTrailer')"
              class="bg-yellow-500 hover:bg-yellow-600 text-black px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
            >
              <Play class="w-5 h-5" />
              Watch Trailer
            </button>
            <button
              @click="$emit('toggleWatchlist')"
              :class="[
                'border-2 px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors',
                isInWatchlist
                  ? 'border-red-500 text-red-500 hover:bg-red-500 hover:text-white'
                  : 'border-white text-white hover:bg-white hover:text-black'
              ]"
            >
              <Heart :class="{ 'fill-current': isInWatchlist }" class="w-5 h-5" />
              {{ isInWatchlist ? 'Remove from Watchlist' : 'Add to Watchlist' }}
            </button>
            <button
              @click="$emit('toggleFavorites')"
              :class="[
                'border-2 px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors',
                isInFavorites
                  ? 'border-yellow-500 text-yellow-500 hover:bg-yellow-500 hover:text-black'
                  : 'border-white text-white hover:bg-white hover:text-black'
              ]"
            >
              <Star :class="{ 'fill-current': isInFavorites }" class="w-5 h-5" />
              {{ isInFavorites ? 'Remove from Favorites' : 'Add to Favorites' }}
            </button>
            <button
              @click="$emit('shareMovie')"
              class="border-2 border-white text-white hover:bg-white hover:text-black px-8 py-3 rounded-lg font-semibold flex items-center gap-2 transition-colors"
            >
              <Share2 class="w-5 h-5" />
              Share
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>