<script setup lang="ts">
import { computed } from 'vue'
import { Play, Star, Heart, Bookmark, Eye } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useSeriesStore } from '@/stores/seriesStore'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import type { TVShow } from '@/data/mockMovies'

interface Props {
  series: TVShow[]
  loading?: boolean
  showPagination?: boolean
  itemsPerPage?: number
  currentPage?: number
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
  showPagination: true,
  itemsPerPage: 12,
  currentPage: 1
})

const router = useRouter()
const seriesStore = useSeriesStore()
const userStore = useUserStore()
const uiStore = useUIStore()

// Generate loading skeleton items
const loadingItems = computed(() => {
  return Array.from({ length: props.itemsPerPage }, (_, index) => ({ id: `loading-${index}` }))
})

const handleSeriesClick = (series: TVShow) => {
  router.push(`/series/${series.id}`)
}

const handlePlayTrailer = (event: Event, series: TVShow) => {
  event.stopPropagation()
  if (series.trailerUrl) {
    window.open(series.trailerUrl, '_blank')
  }
}

const toggleWatchlist = async (event: Event, seriesId: string) => {
  event.stopPropagation()
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (userStore.isInWatchlist(seriesId)) {
      await userStore.removeFromWatchlist(seriesId)
    } else {
      await userStore.addToWatchlistWithActivity(seriesId)
    }
  } catch (error) {
    console.error('Error updating watchlist:', error)
  }
}

const toggleFavorite = async (event: Event, seriesId: string) => {
  event.stopPropagation()
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (userStore.isInFavorites(seriesId)) {
      await userStore.removeFromFavorites(seriesId)
    } else {
      await userStore.addToFavoritesWithActivity(seriesId)
    }
  } catch (error) {
    console.error('Error updating favorites:', error)
  }
}

const formatRating = (rating: number) => {
  return rating.toFixed(1)
}

const getStatusColor = (status: string) => {
  switch (status) {
    case 'ongoing':
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
    case 'completed':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
    case 'cancelled':
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-800 dark:text-gray-200'
  }
}
</script>

<template>
  <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
    <!-- Loading Skeleton -->
    <template v-if="loading">
      <div 
        v-for="item in loadingItems" 
        :key="item.id"
        class="bg-theme-surface rounded-lg shadow-md overflow-hidden animate-pulse border border-theme-border"
      >
        <div class="aspect-[2/3] bg-theme-border"></div>
        <div class="p-4">
          <div class="h-4 bg-theme-border rounded mb-2"></div>
          <div class="h-3 bg-theme-border rounded mb-2 w-3/4"></div>
          <div class="h-3 bg-theme-border rounded w-1/2"></div>
        </div>
      </div>
    </template>

    <!-- Series Grid -->
    <template v-else>
      <div 
        v-for="show in series" 
        :key="show.id"
        @click="handleSeriesClick(show)"
        class="group bg-theme-surface rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer transform hover:-translate-y-1 border border-theme-border"
      >
        <!-- Poster -->
        <div class="relative aspect-[2/3] overflow-hidden">
          <img 
            :src="show.posterUrl" 
            :alt="show.title" 
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            loading="lazy"
          />
          
          <!-- Overlay -->
          <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-300 flex items-center justify-center">
            <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex gap-2">
              <button 
                @click="handlePlayTrailer($event, show)"
                class="bg-white bg-opacity-90 hover:bg-opacity-100 text-gray-900 p-2 rounded-full transition-all duration-200 hover:scale-110"
                :disabled="!show.trailerUrl"
              >
                <Play class="w-4 h-4" />
              </button>
              <button 
                @click="toggleWatchlist($event, show.id)"
                class="bg-white bg-opacity-90 hover:bg-opacity-100 text-gray-900 p-2 rounded-full transition-all duration-200 hover:scale-110"
              >
                <Bookmark class="w-4 h-4" />
              </button>
              <button 
                @click="toggleFavorite($event, show.id)"
                class="bg-white bg-opacity-90 hover:bg-opacity-100 text-gray-900 p-2 rounded-full transition-all duration-200 hover:scale-110"
              >
                <Heart class="w-4 h-4" />
              </button>
            </div>
          </div>
          
          <!-- Rating Badge -->
          <div class="absolute top-2 left-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded-md text-xs font-semibold flex items-center gap-1">
            <Star class="w-3 h-3 fill-current text-yellow-400" />
            {{ formatRating(show.lemonPieRating) }}
          </div>
          
          <!-- Status Badge -->
          <div :class="['absolute top-2 right-2 px-2 py-1 rounded-md text-xs font-semibold capitalize', getStatusColor(show.status)]">
            {{ show.status }}
          </div>
        </div>
        
        <!-- Content -->
        <div class="p-4">
          <h3 class="font-bold text-sm line-clamp-2 group-hover:text-orange-600 transition-colors text-theme-primary">
            {{ show.title }}
          </h3>
          
          <div class="flex items-center gap-2 text-xs text-theme-text-secondary mt-1">
            <Star class="w-3 h-3 fill-orange-400 text-orange-400" />
            <span>{{ show.lemonPieRating.toFixed(1) }}</span>
          </div>
          
          <div class="text-xs text-theme-text-secondary mt-1">
            {{ show.releaseDate.split('-')[0] }} • {{ show.seasons }} Season{{ show.seasons > 1 ? 's' : '' }}
          </div>
          
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-1 text-sm">
              <span class="text-orange-500 font-semibold">{{ formatRating(show.lemonPieRating) }}</span>
              <span class="text-theme-text-secondary">/10</span>
            </div>
            <div class="flex items-center gap-1 text-xs text-theme-text-secondary">
              <Eye class="w-3 h-3" />
              <span>{{ show.reviewCount }}</span>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>