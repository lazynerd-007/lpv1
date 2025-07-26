<script setup lang="ts">
import { computed } from 'vue'
import { Play, Star, Heart, Bookmark, Eye, Calendar, MapPin } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import type { Movie } from '@/data/mockMovies'

interface Props {
  movie: Movie
  size?: 'sm' | 'md' | 'lg'
  showPlayButton?: boolean
  showActions?: boolean
  showDetails?: boolean
  clickable?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  showPlayButton: true,
  showActions: true,
  showDetails: true,
  clickable: true
})

const emit = defineEmits<{
  playTrailer: [movie: Movie]
  click: [movie: Movie]
}>()

const router = useRouter()
const userStore = useUserStore()
const uiStore = useUIStore()

const cardClasses = computed(() => {
  const base = 'card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300 group'
  const sizeClasses = {
    sm: 'w-48',
    md: 'w-full',
    lg: 'w-full max-w-sm'
  }
  const clickableClass = props.clickable ? 'cursor-pointer' : ''
  
  return `${base} ${sizeClasses[props.size]} ${clickableClass}`
})

const imageClasses = computed(() => {
  const sizeClasses = {
    sm: 'h-48',
    md: 'h-64',
    lg: 'h-80'
  }
  
  return `w-full object-cover transition-transform duration-300 group-hover:scale-105 ${sizeClasses[props.size]}`
})

const handleCardClick = () => {
  if (props.clickable) {
    emit('click', props.movie)
    router.push(`/movie/${props.movie.id}`)
  }
}

const handlePlayTrailer = (event: Event) => {
  event.stopPropagation()
  emit('playTrailer', props.movie)
}

const toggleWatchlist = async (event: Event) => {
  event.stopPropagation()
  
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (userStore.isInWatchlist(props.movie.id)) {
      await userStore.removeFromWatchlist(props.movie.id)
    } else {
      await userStore.addToWatchlist(props.movie.id)
    }
  } catch (error) {
    console.error('Error updating watchlist:', error)
  }
}

const toggleFavorite = async (event: Event) => {
  event.stopPropagation()
  
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (userStore.isInFavorites(props.movie.id)) {
      await userStore.removeFromFavorites(props.movie.id)
    } else {
      await userStore.addToFavorites(props.movie.id)
    }
  } catch (error) {
    console.error('Error updating favorites:', error)
  }
}

const getMovieTypeIcon = (movie: Movie) => {
  if (movie.genre.includes('Comedy')) return '🥧'
  if (movie.genre.includes('Drama')) return '🍋'
  return '🎬'
}

const getMovieTypeBadge = (movie: Movie) => {
  if (movie.genre.includes('Comedy')) return 'badge-success'
  if (movie.genre.includes('Drama')) return 'badge-warning'
  return 'badge-primary'
}
</script>

<template>
  <div :class="cardClasses" @click="handleCardClick">
    <!-- Movie Poster -->
    <figure class="relative overflow-hidden">
      <img 
        :src="movie.poster" 
        :alt="movie.title"
        :class="imageClasses"
      />
      
      <!-- Overlay -->
      <div 
        v-if="showPlayButton"
        class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-60 transition-all duration-300 flex items-center justify-center"
      >
        <button 
          @click="handlePlayTrailer"
          class="btn btn-circle btn-primary opacity-0 group-hover:opacity-100 transition-all duration-300 transform scale-75 group-hover:scale-100"
        >
          <Play class="w-6 h-6" />
        </button>
      </div>
      
      <!-- Movie Type Badge -->
      <div class="absolute top-2 left-2">
        <div :class="['badge', getMovieTypeBadge(movie), 'gap-1']">
          <span>{{ getMovieTypeIcon(movie) }}</span>
          <span class="capitalize">{{ movie.genre[0] || 'Movie' }}</span>
        </div>
      </div>
      
      <!-- Action Buttons -->
      <div 
        v-if="showActions"
        class="absolute top-2 right-2 flex flex-col gap-2 opacity-0 group-hover:opacity-100 transition-all duration-300"
      >
        <button 
          @click="toggleWatchlist"
          :class="[
            'btn btn-sm btn-circle',
            userStore.isInWatchlist(movie.id) ? 'btn-warning' : 'btn-ghost bg-black bg-opacity-50 text-white'
          ]"
          :title="userStore.isInWatchlist(movie.id) ? 'Remove from Watchlist' : 'Add to Watchlist'"
        >
          <Bookmark class="w-4 h-4" />
        </button>
        
        <button 
          @click="toggleFavorite"
          :class="[
            'btn btn-sm btn-circle',
            userStore.isInFavorites(movie.id) ? 'btn-error' : 'btn-ghost bg-black bg-opacity-50 text-white'
          ]"
          :title="userStore.isInFavorites(movie.id) ? 'Remove from Favorites' : 'Add to Favorites'"
        >
          <Heart class="w-4 h-4" />
        </button>
      </div>
      
      <!-- Rating Badge -->
      <div class="absolute bottom-2 left-2">
        <div class="badge badge-neutral gap-1">
          <Star class="w-3 h-3 fill-yellow-400 text-yellow-400" />
          <span>{{ movie.lemonPieRating.toFixed(1) }}</span>
        </div>
      </div>
    </figure>
    
    <!-- Movie Info -->
    <div v-if="showDetails" class="card-body p-4">
      <h3 :class="[
        'card-title font-bold line-clamp-2 group-hover:text-primary transition-colors',
        size === 'sm' ? 'text-sm' : size === 'lg' ? 'text-lg' : 'text-base'
      ]">
        {{ movie.title }}
      </h3>
      
      <div class="flex items-center justify-between text-xs text-gray-600 mt-2">
        <div class="flex items-center gap-1">
          <Calendar class="w-3 h-3" />
          <span>{{ movie.year }}</span>
        </div>
        <div class="flex items-center gap-1">
          <Eye class="w-3 h-3" />
          <span>{{ movie.reviewCount || 0 }} reviews</span>
        </div>
      </div>
      
      <!-- Genres -->
      <div class="flex flex-wrap gap-1 mt-2">
        <span 
          v-for="genre in movie.genre.slice(0, 2)" 
          :key="genre"
          class="badge badge-outline badge-xs"
        >
          {{ genre }}
        </span>
        <span 
          v-if="movie.genre.length > 2"
          class="badge badge-outline badge-xs"
        >
          +{{ movie.genre.length - 2 }}
        </span>
      </div>
      
      <!-- Production State & Location -->
      <div class="flex items-center justify-between mt-2 text-xs text-gray-500">
        <span v-if="movie.productionState">{{ movie.productionState }}</span>
        <div v-if="movie.director" class="flex items-center gap-1">
          <MapPin class="w-3 h-3" />
          <span>{{ movie.director }}</span>
        </div>
      </div>
      
      <!-- Synopsis (for larger cards) -->
      <p 
        v-if="size === 'lg' && movie.plotSummary" 
        class="text-sm text-gray-600 mt-2 line-clamp-3"
      >
        {{ movie.plotSummary }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>