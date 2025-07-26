<script setup lang="ts">
import { computed } from 'vue';
import type { Review } from '@/data/mockMovies';
import LemonPieRating from './LemonPieRating.vue';
import { ThumbsUp, MessageCircle, AlertTriangle } from 'lucide-vue-next';

interface Props {
  review: Review;
  showMovieTitle?: boolean;
  variant?: 'default' | 'compact';
}

const props = withDefaults(defineProps<Props>(), {
  showMovieTitle: false,
  variant: 'default'
});

const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

const truncatedReview = computed(() => {
  if (props.variant === 'compact' && props.review.reviewText.length > 150) {
    return props.review.reviewText.substring(0, 150) + '...';
  }
  return props.review.reviewText;
});

const cardClasses = computed(() => {
  return props.variant === 'compact' 
    ? 'card bg-base-100 shadow-md hover:shadow-lg transition-all duration-300 cursor-pointer'
    : 'card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300';
});
</script>

<template>
  <div :class="cardClasses">
    <div class="card-body">
      <!-- User Info Header -->
      <div class="flex items-start justify-between mb-3">
        <div class="flex items-center gap-3">
          <!-- User Avatar -->
          <div class="avatar">
            <div class="w-10 h-10 rounded-full">
              <img 
                :src="review.userAvatar" 
                :alt="review.userName"
                class="w-full h-full object-cover"
              />
            </div>
          </div>
          
          <!-- User Details -->
          <div>
            <div class="flex items-center gap-2">
              <h3 class="font-semibold text-sm">{{ review.userName }}</h3>
              <span v-if="review.isVerifiedCritic" class="badge badge-secondary badge-xs">
                ✓ Critic
              </span>
            </div>
            <p class="text-xs text-gray-500">{{ formatDate(review.createdAt) }}</p>
          </div>
        </div>
        
        <!-- Rating -->
        <LemonPieRating 
          :rating="review.lemonPieRating" 
          size="sm"
          :show-text="false"
        />
      </div>
      
      <!-- Spoiler Warning -->
      <div v-if="review.spoilerWarning" class="alert alert-warning alert-sm mb-3">
        <AlertTriangle class="w-4 h-4" />
        <span class="text-xs">Contains Spoilers</span>
      </div>
      
      <!-- Review Content -->
      <div class="mb-3">
        <p class="text-sm text-gray-700 leading-relaxed">
          {{ truncatedReview }}
        </p>
      </div>
      
      <!-- Nollywood Tags -->
      <div v-if="review.nollywoodTags.length > 0" class="mb-3">
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="tag in review.nollywoodTags.slice(0, 3)" 
            :key="tag"
            class="badge badge-accent badge-xs"
          >
            {{ tag }}
          </span>
        </div>
      </div>
      
      <!-- Category Ratings (for non-compact variant) -->
      <div v-if="variant !== 'compact'" class="grid grid-cols-2 gap-2 mb-3 text-xs">
        <div class="flex justify-between">
          <span class="text-gray-600">Cultural Authenticity:</span>
          <span class="font-medium">{{ review.culturalAuthenticityRating }}/10</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-600">Production Quality:</span>
          <span class="font-medium">{{ review.productionQualityRating }}/10</span>
        </div>
      </div>
      
      <!-- Review Actions -->
      <div class="flex items-center justify-between pt-2 border-t border-gray-100">
        <div class="flex items-center gap-4">
          <!-- Helpful Button -->
          <button class="btn btn-ghost btn-xs gap-1 hover:btn-primary">
            <ThumbsUp class="w-3 h-3" />
            <span>{{ review.helpfulnessScore }}</span>
          </button>
          
          <!-- Comment Button -->
          <button class="btn btn-ghost btn-xs gap-1">
            <MessageCircle class="w-3 h-3" />
            <span>Reply</span>
          </button>
        </div>
        
        <!-- Language Badge -->
        <div class="flex items-center gap-2">
          <span class="badge badge-ghost badge-xs">
            {{ review.reviewLanguage.toUpperCase() }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>