<script setup lang="ts">
import { computed } from 'vue';
import type { Movie } from '@/data/mockMovies';
import LemonPieRating from './LemonPieRating.vue';

interface Props {
  movie: Movie;
  variant?: 'default' | 'featured' | 'compact';
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default'
});

const cardClasses = computed(() => {
  switch (props.variant) {
    case 'featured':
      return 'card lg:card-side bg-base-100 shadow-xl hover:shadow-2xl transition-all duration-300';
    case 'compact':
      return 'card bg-base-100 shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer';
    default:
      return 'card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer';
  }
});

const imageClasses = computed(() => {
  switch (props.variant) {
    case 'featured':
      return 'lg:w-96 h-64 lg:h-auto';
    case 'compact':
      return 'h-48';
    default:
      return 'h-56';
  }
});

const formatRuntime = (minutes: number) => {
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
};

const formatGenres = (genres: string[]) => {
  return genres.slice(0, 2).join(', ');
};
</script>

<template>
  <div :class="cardClasses">
    <!-- Movie Poster -->
    <figure :class="imageClasses">
      <img 
        :src="movie.posterUrl" 
        :alt="movie.title"
        class="w-full h-full object-cover"
        loading="lazy"
      />
    </figure>
    
    <!-- Movie Details -->
    <div class="card-body">
      <!-- Title and Local Title -->
      <div class="mb-2">
        <h2 :class="[
          'card-title',
          variant === 'featured' ? 'text-2xl' : 'text-lg',
          variant === 'compact' ? 'text-base' : ''
        ]">
          {{ movie.title }}
        </h2>
        <p v-if="movie.localTitle" class="text-sm text-gray-500 italic">
          {{ movie.localTitle }}
        </p>
      </div>
      
      <!-- Rating -->
      <div class="mb-3">
        <LemonPieRating 
          :rating="movie.lemonPieRating" 
          :size="variant === 'featured' ? 'lg' : 'md'"
        />
      </div>
      
      <!-- Movie Info -->
      <div class="space-y-2 text-sm">
        <div class="flex items-center gap-4">
          <span class="badge badge-outline">{{ movie.releaseDate.split('-')[0] }}</span>
          <span class="text-gray-600">{{ formatRuntime(movie.runtime) }}</span>
        </div>
        
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="genre in movie.genre.slice(0, 3)" 
            :key="genre"
            class="badge badge-primary badge-sm"
          >
            {{ genre }}
          </span>
        </div>
        
        <div class="flex items-center gap-2">
          <span class="text-gray-600">Director:</span>
          <span class="font-medium">{{ movie.director }}</span>
        </div>
        
        <div class="flex items-center gap-2">
          <span class="text-gray-600">State:</span>
          <span class="font-medium">{{ movie.productionState }}</span>
        </div>
      </div>
      
      <!-- Plot Summary (only for featured variant) -->
      <p v-if="variant === 'featured'" class="text-gray-700 mt-3 line-clamp-3">
        {{ movie.plotSummary }}
      </p>
      
      <!-- Stats -->
      <div class="flex items-center justify-between mt-4 text-sm text-gray-600">
        <div class="flex items-center gap-4">
          <span>{{ movie.reviewCount }} reviews</span>
          <span v-if="movie.boxOfficeNG">{{ movie.boxOfficeNG }}</span>
        </div>
        
        <!-- Streaming Platforms -->
        <div class="flex gap-1">
          <span 
            v-for="platform in movie.streamingPlatforms.slice(0, 2)" 
            :key="platform"
            class="badge badge-ghost badge-xs"
          >
            {{ platform }}
          </span>
        </div>
      </div>
      
      <!-- Awards (if any) -->
      <div v-if="movie.awards.length > 0" class="mt-2">
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="award in movie.awards.slice(0, 2)" 
            :key="award"
            class="badge badge-secondary badge-sm"
          >
            🏆 {{ award }}
          </span>
        </div>
      </div>
      
      <!-- Action Buttons -->
      <div class="card-actions justify-end mt-4">
        <button class="btn btn-primary btn-sm">
          View Details
        </button>
        <button v-if="variant !== 'compact'" class="btn btn-outline btn-sm">
          Add to Watchlist
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>