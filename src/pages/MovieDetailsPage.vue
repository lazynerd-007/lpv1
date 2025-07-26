<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Star, Clock, Calendar, MapPin, Award, Play, Heart, Share2, MessageCircle } from 'lucide-vue-next';
import LemonPieRating from '@/components/LemonPieRating.vue';
import ReviewCard from '@/components/ReviewCard.vue';
import { mockMovies, mockReviews, getMovieById, getReviewsForMovie } from '@/data/mockMovies';

interface Props {
  id: string;
}

const props = defineProps<Props>();
const route = useRoute();

const movie = ref(getMovieById(props.id || route.params.id as string));
const reviews = ref(getReviewsForMovie(props.id || route.params.id as string));
const isWatchlisted = ref(false);
const showTrailer = ref(false);
const activeTab = ref('reviews');

const averageRating = computed(() => {
  if (!reviews.value.length) return 0;
  return reviews.value.reduce((sum, review) => sum + review.rating, 0) / reviews.value.length;
});

const ratingDistribution = computed(() => {
  const dist = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0 };
  reviews.value.forEach(review => {
    dist[review.rating as keyof typeof dist]++;
  });
  return dist;
});

const toggleWatchlist = () => {
  isWatchlisted.value = !isWatchlisted.value;
};

const shareMovie = () => {
  if (navigator.share) {
    navigator.share({
      title: movie.value?.title,
      text: `Check out ${movie.value?.title} on LemonNPie`,
      url: window.location.href
    });
  }
};

onMounted(() => {
  if (!movie.value) {
    // Handle movie not found
    console.error('Movie not found');
  }
});
</script>

<template>
  <div v-if="movie" class="min-h-screen bg-base-100">
    <!-- Hero Section -->
    <div class="relative h-96 bg-gradient-to-r from-primary/20 to-secondary/20">
      <div class="absolute inset-0 bg-black/50"></div>
      <div class="relative container mx-auto px-4 h-full flex items-end pb-8">
        <div class="flex flex-col md:flex-row gap-6 w-full">
          <!-- Movie Poster -->
          <div class="flex-shrink-0">
            <img 
              :src="movie.poster" 
              :alt="movie.title"
              class="w-48 h-72 object-cover rounded-lg shadow-2xl"
            />
          </div>
          
          <!-- Movie Info -->
          <div class="flex-1 text-white">
            <h1 class="text-4xl md:text-5xl font-bold mb-2">{{ movie.title }}</h1>
            <p class="text-xl text-gray-200 mb-4">{{ movie.tagline }}</p>
            
            <div class="flex flex-wrap items-center gap-4 mb-4">
              <LemonPieRating :rating="averageRating" size="lg" />
              <span class="text-lg">{{ averageRating.toFixed(1) }}/10</span>
              <span class="text-gray-300">{{ reviews.length }} reviews</span>
            </div>
            
            <div class="flex flex-wrap items-center gap-6 text-sm">
              <div class="flex items-center gap-1">
                <Clock class="w-4 h-4" />
                <span>{{ movie.runtime }} min</span>
              </div>
              <div class="flex items-center gap-1">
                <Calendar class="w-4 h-4" />
                <span>{{ movie.releaseDate }}</span>
              </div>
              <div class="flex items-center gap-1">
                <MapPin class="w-4 h-4" />
                <span>{{ movie.productionState }}</span>
              </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="flex flex-wrap gap-3 mt-6">
              <button 
                @click="showTrailer = true"
                class="btn btn-primary btn-lg"
              >
                <Play class="w-5 h-5 mr-2" />
                Watch Trailer
              </button>
              <button 
                @click="toggleWatchlist"
                :class="['btn btn-outline btn-lg', isWatchlisted ? 'btn-error' : 'btn-secondary']"
              >
                <Heart :class="['w-5 h-5 mr-2', isWatchlisted ? 'fill-current' : '']" />
                {{ isWatchlisted ? 'Remove from Watchlist' : 'Add to Watchlist' }}
              </button>
              <button 
                @click="shareMovie"
                class="btn btn-outline btn-lg"
              >
                <Share2 class="w-5 h-5 mr-2" />
                Share
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Content Tabs -->
    <div class="container mx-auto px-4 py-8">
      <div class="tabs tabs-boxed mb-8">
        <button 
          @click="activeTab = 'overview'"
          :class="['tab', activeTab === 'overview' ? 'tab-active' : '']"
        >
          Overview
        </button>
        <button 
          @click="activeTab = 'reviews'"
          :class="['tab', activeTab === 'reviews' ? 'tab-active' : '']"
        >
          Reviews ({{ reviews.length }})
        </button>
        <button 
          @click="activeTab = 'cast'"
          :class="['tab', activeTab === 'cast' ? 'tab-active' : '']"
        >
          Cast & Crew
        </button>
      </div>
      
      <!-- Overview Tab -->
      <div v-if="activeTab === 'overview'" class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div class="lg:col-span-2">
          <div class="card bg-base-200 shadow-lg">
            <div class="card-body">
              <h2 class="card-title text-2xl mb-4">Plot Summary</h2>
              <p class="text-lg leading-relaxed">{{ movie.plot }}</p>
            </div>
          </div>
          
          <!-- Additional Movie Details -->
          <div class="card bg-base-200 shadow-lg mt-6">
            <div class="card-body">
              <h3 class="card-title mb-4">Movie Details</h3>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <span class="font-semibold">Genre:</span>
                  <span class="ml-2">{{ movie.genre }}</span>
                </div>
                <div>
                  <span class="font-semibold">Language:</span>
                  <span class="ml-2">{{ movie.language }}</span>
                </div>
                <div>
                  <span class="font-semibold">Director:</span>
                  <span class="ml-2">{{ movie.director }}</span>
                </div>
                <div>
                  <span class="font-semibold">Producer:</span>
                  <span class="ml-2">{{ movie.producer }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Rating Distribution -->
          <div class="card bg-base-200 shadow-lg">
            <div class="card-body">
              <h3 class="card-title mb-4">Rating Distribution</h3>
              <div class="space-y-2">
                <div v-for="(count, rating) in ratingDistribution" :key="rating" class="flex items-center gap-2">
                  <span class="w-8 text-sm">{{ rating }}</span>
                  <div class="flex-1 bg-base-300 rounded-full h-2">
                    <div 
                      class="bg-primary h-2 rounded-full" 
                      :style="{ width: `${(count / reviews.length) * 100}%` }"
                    ></div>
                  </div>
                  <span class="text-sm w-8">{{ count }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Reviews Tab -->
      <div v-if="activeTab === 'reviews'" class="space-y-6">
        <div class="flex justify-between items-center">
          <h2 class="text-2xl font-bold">User Reviews</h2>
          <router-link :to="`/write-review?movie=${movie.id}`" class="btn btn-primary">
            <MessageCircle class="w-4 h-4 mr-2" />
            Write Review
          </router-link>
        </div>
        
        <div v-if="reviews.length === 0" class="text-center py-12">
          <MessageCircle class="w-16 h-16 mx-auto text-base-content/30 mb-4" />
          <h3 class="text-xl font-semibold mb-2">No Reviews Yet</h3>
          <p class="text-base-content/70 mb-4">Be the first to review this movie!</p>
          <router-link :to="`/write-review?movie=${movie.id}`" class="btn btn-primary">
            Write First Review
          </router-link>
        </div>
        
        <div v-else class="space-y-4">
          <ReviewCard 
            v-for="review in reviews" 
            :key="review.id" 
            :review="review"
          />
        </div>
      </div>
      
      <!-- Cast & Crew Tab -->
      <div v-if="activeTab === 'cast'" class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="card bg-base-200 shadow-lg">
          <div class="card-body">
            <h3 class="card-title mb-4">Main Cast</h3>
            <div class="space-y-3">
              <div v-for="actor in movie.cast" :key="actor" class="flex items-center gap-3">
                <div class="avatar placeholder">
                  <div class="bg-neutral text-neutral-content rounded-full w-12">
                    <span class="text-sm">{{ actor.charAt(0) }}</span>
                  </div>
                </div>
                <span class="font-medium">{{ actor }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card bg-base-200 shadow-lg">
          <div class="card-body">
            <h3 class="card-title mb-4">Crew</h3>
            <div class="space-y-2">
              <div>
                <span class="font-semibold">Director:</span>
                <span class="ml-2">{{ movie.director }}</span>
              </div>
              <div>
                <span class="font-semibold">Producer:</span>
                <span class="ml-2">{{ movie.producer }}</span>
              </div>
              <div>
                <span class="font-semibold">Screenplay:</span>
                <span class="ml-2">{{ movie.screenplay || 'N/A' }}</span>
              </div>
              <div>
                <span class="font-semibold">Cinematography:</span>
                <span class="ml-2">{{ movie.cinematography || 'N/A' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Movie Not Found -->
  <div v-else class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">Movie Not Found</h1>
      <p class="text-lg text-base-content/70 mb-6">The movie you're looking for doesn't exist.</p>
      <router-link to="/" class="btn btn-primary">Go Home</router-link>
    </div>
  </div>
</template>

<style scoped>
/* Additional custom styles if needed */
</style>