<script setup lang="ts">
import { computed } from 'vue';
import type { Review } from '@/data/mockMovies';
import LemonPieRating from './LemonPieRating.vue';
import { ThumbsUp, ThumbsDown, MessageCircle, AlertTriangle, Eye, EyeOff, Edit3, MoreHorizontal } from 'lucide-vue-next';
import { useMovieStore } from '@/stores/movieStore';
import { useAuthStore } from '@/stores/authStore';
import { ref } from 'vue';

interface Props {
  review: Review;
  showMovieTitle?: boolean;
  variant?: 'default' | 'compact';
}

const props = withDefaults(defineProps<Props>(), {
  showMovieTitle: false,
  variant: 'default'
});

const emit = defineEmits<{
  edit: [review: Review]
}>();

const movieStore = useMovieStore();
const authStore = useAuthStore();
const showSpoilers = ref(false);

// Mock current user ID (in real app, this would come from auth)
const currentUserId = computed(() => authStore.user?.id || 'current-user');

const userVote = computed(() => {
  return movieStore.getUserVoteOnReview(props.review.id, currentUserId.value);
});

const canVote = computed(() => {
  return props.review.userId !== currentUserId.value;
});

const canEdit = computed(() => {
  return props.review.userId === currentUserId.value;
});

const handleEdit = () => {
  if (canEdit.value) {
    emit('edit', props.review);
  }
};

const handleVote = (voteType: 'helpful' | 'unhelpful') => {
  if (!canVote.value) return;
  movieStore.voteOnReview(props.review.id, currentUserId.value, voteType);
};

const toggleSpoilers = () => {
  showSpoilers.value = !showSpoilers.value;
};

const helpfulPercentage = computed(() => {
  const total = props.review.helpfulVotes + props.review.unhelpfulVotes;
  if (total === 0) return 0;
  return Math.round((props.review.helpfulVotes / total) * 100);
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
            <p class="text-xs text-theme-secondary">{{ formatDate(review.createdAt) }}</p>
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
        <button 
          @click="toggleSpoilers" 
          class="btn btn-ghost btn-xs ml-auto"
          :class="{ 'btn-active': showSpoilers }"
        >
          <Eye v-if="!showSpoilers" class="w-3 h-3" />
          <EyeOff v-else class="w-3 h-3" />
          <span class="ml-1">{{ showSpoilers ? 'Hide' : 'Show' }}</span>
        </button>
      </div>
      
      <!-- Review Content -->
      <div class="mb-3">
        <div v-if="review.spoilerWarning && !showSpoilers" class="relative">
          <p class="text-sm text-theme-primary leading-relaxed blur-sm select-none">
            {{ truncatedReview }}
          </p>
          <div class="absolute inset-0 flex items-center justify-center bg-base-100/50">
            <span class="text-xs font-medium text-warning">Spoiler content hidden</span>
          </div>
        </div>
        <p v-else class="text-sm text-theme-primary leading-relaxed">
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
          <span class="text-theme-secondary">Story:</span>
          <span class="font-medium">{{ review.storyRating }}/10</span>
        </div>
        <div class="flex justify-between">
          <span class="text-theme-secondary">Acting:</span>
          <span class="font-medium">{{ review.actingRating }}/10</span>
        </div>
        <div class="flex justify-between">
          <span class="text-theme-secondary">Cinematography:</span>
          <span class="font-medium">{{ review.cinematographyRating }}/10</span>
        </div>
        <div class="flex justify-between">
          <span class="text-theme-secondary">Production Quality:</span>
          <span class="font-medium">{{ review.productionQualityRating }}/10</span>
        </div>
        <div class="flex justify-between col-span-2">
          <span class="text-theme-secondary">Cultural Authenticity:</span>
          <span class="font-medium text-accent">{{ review.culturalAuthenticityRating }}/10</span>
        </div>
      </div>
      
      <!-- Review Actions -->
      <div class="flex items-center justify-between pt-2 border-t border-theme-border">
        <div class="flex items-center gap-2">
          <!-- Helpful Button -->
          <button 
            @click="handleVote('helpful')"
            :disabled="!canVote"
            class="btn btn-ghost btn-xs gap-1 transition-all"
            :class="{
              'btn-success': userVote === 'helpful',
              'hover:btn-success': canVote && userVote !== 'helpful',
              'opacity-50 cursor-not-allowed': !canVote
            }"
            :title="!canVote ? 'Cannot vote on your own review' : 'Mark as helpful'"
          >
            <ThumbsUp class="w-3 h-3" />
            <span>{{ review.helpfulVotes }}</span>
          </button>
          
          <!-- Unhelpful Button -->
          <button 
            @click="handleVote('unhelpful')"
            :disabled="!canVote"
            class="btn btn-ghost btn-xs gap-1 transition-all"
            :class="{
              'btn-error': userVote === 'unhelpful',
              'hover:btn-error': canVote && userVote !== 'unhelpful',
              'opacity-50 cursor-not-allowed': !canVote
            }"
            :title="!canVote ? 'Cannot vote on your own review' : 'Mark as unhelpful'"
          >
            <ThumbsDown class="w-3 h-3" />
            <span>{{ review.unhelpfulVotes }}</span>
          </button>
          
          <!-- Helpfulness Percentage -->
          <div v-if="review.helpfulVotes + review.unhelpfulVotes > 0" class="text-xs text-theme-secondary">
            {{ helpfulPercentage }}% helpful
          </div>
          
          <!-- Comment Button -->
          <button class="btn btn-ghost btn-xs gap-1 ml-2">
            <MessageCircle class="w-3 h-3" />
            <span>Reply</span>
          </button>
        </div>
        
        <!-- Review Options -->
        <div class="flex items-center gap-2">
          <!-- Edit Button (only for review owner) -->
          <button 
            v-if="canEdit"
            @click="handleEdit"
            class="btn btn-ghost btn-xs gap-1 text-theme-secondary hover:text-primary"
            title="Edit your review"
          >
            <Edit3 class="w-3 h-3" />
            <span class="hidden sm:inline">Edit</span>
          </button>
          
          <!-- Language Badge -->
          <span class="badge badge-ghost badge-xs">
            {{ review.reviewLanguage || 'EN' }}
          </span>
        </div>
      </div>
    </div>
  </div>
</template>