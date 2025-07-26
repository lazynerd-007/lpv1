<script setup lang="ts">
import { computed, onMounted } from 'vue';
import { 
  getFeaturedMovie, 
  getPieMovies, 
  getLemonMovies, 
  getTrendingMovies,
  getTrendingReviews,
  getTrendingTVShows,
  mockMovies
} from '@/data/mockMovies';
import MovieCard from '@/components/MovieCard.vue';
import ReviewCard from '@/components/ReviewCard.vue';
import LemonPieRating from '@/components/LemonPieRating.vue';
import { Play, TrendingUp, Calendar, MapPin } from 'lucide-vue-next';

// Data
const featuredMovie = computed(() => getFeaturedMovie());
const pieMovies = computed(() => getPieMovies().slice(0, 3));
const lemonMovies = computed(() => getLemonMovies().slice(0, 3));
const trendingMovies = computed(() => getTrendingMovies());
const trendingTVShows = computed(() => getTrendingTVShows());
const trendingReviews = computed(() => getTrendingReviews());

// Mock Nollywood news
const nollywoodNews = [
  {
    id: 1,
    title: 'Funke Akindele Announces New Comedy Series',
    summary: 'The acclaimed actress and director reveals her latest project set to premiere on Netflix.',
    date: '2024-01-20',
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20actress%20Funke%20Akindele%20comedy%20series%20announcement%20colorful%20backdrop&image_size=landscape_4_3'
  },
  {
    id: 2,
    title: 'AMVCA 2024 Nominations Announced',
    summary: 'The Africa Magic Viewers Choice Awards reveals this year\'s nominees across 28 categories.',
    date: '2024-01-18',
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=AMVCA%20awards%20ceremony%20golden%20trophy%20elegant%20stage%20Nigerian%20entertainment&image_size=landscape_4_3'
  },
  {
    id: 3,
    title: 'Nollywood Box Office Hits Record High',
    summary: 'Nigerian cinema revenues reach unprecedented levels with local productions leading the charge.',
    date: '2024-01-15',
    image: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20cinema%20box%20office%20success%20movie%20theater%20audience%20celebration&image_size=landscape_4_3'
  }
];

onMounted(() => {
  console.log('LemonNPie Homepage loaded with', mockMovies.length, 'movies');
});
</script>

<template>
  <div class="min-h-screen bg-base-100">
    <!-- Hero Section -->
    <section v-if="featuredMovie" class="relative h-[80vh] overflow-hidden">
      <!-- Background Image with Gradient Overlay -->
      <div 
        class="absolute inset-0 bg-cover bg-center bg-no-repeat"
        :style="{ backgroundImage: `url(${featuredMovie.posterUrl})` }"
      >
        <div class="absolute inset-0 bg-gradient-to-r from-purple-900/90 via-pink-800/70 to-orange-600/60"></div>
      </div>
      
      <!-- Content -->
      <div class="relative z-10 h-full flex items-center">
        <div class="container mx-auto px-4">
          <div class="flex items-center gap-8 max-w-6xl">
            <!-- Movie Poster -->
            <div class="hidden md:block flex-shrink-0">
              <img 
                :src="featuredMovie.posterUrl" 
                :alt="featuredMovie.title"
                class="w-80 h-[450px] object-cover rounded-lg shadow-2xl"
              />
            </div>
            
            <!-- Movie Details -->
            <div class="flex-1 text-white">
              <!-- Rating -->
              <div class="flex items-center gap-2 mb-4">
                <div class="flex items-center gap-1">
                  <span class="text-yellow-400">⭐</span>
                  <span class="text-2xl font-bold">{{ featuredMovie.lemonPieRating }}</span>
                  <span class="text-gray-300">/ 10</span>
                </div>
              </div>
              
              <!-- Title -->
              <h1 class="text-5xl md:text-6xl font-bold mb-4 leading-tight">
                {{ featuredMovie.title }}
              </h1>
              
              <!-- Local Title -->
              <p v-if="featuredMovie.localTitle" class="text-xl text-gray-300 italic mb-6">
                {{ featuredMovie.localTitle }}
              </p>
              
              <!-- Description -->
              <p class="text-lg text-gray-200 mb-8 max-w-2xl leading-relaxed">
                {{ featuredMovie.plotSummary }}
              </p>
              
              <!-- Action Button -->
              <button class="flex items-center gap-3 bg-orange-500 hover:bg-orange-600 text-white px-8 py-4 rounded-lg font-semibold text-lg transition-colors">
                <Play class="w-6 h-6" fill="currentColor" />
                Play trailer
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Navigation Arrows -->
      <button class="absolute left-4 top-1/2 transform -translate-y-1/2 bg-black/30 hover:bg-black/50 text-white p-3 rounded-full transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
      </button>
      <button class="absolute right-4 top-1/2 transform -translate-y-1/2 bg-black/30 hover:bg-black/50 text-white p-3 rounded-full transition-colors">
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </button>
    </section>

    <!-- Now Playing Section -->
    <section class="bg-white py-12">
      <div class="container mx-auto px-4">
        <!-- Section Header -->
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center gap-3">
            <div class="w-1 h-8 bg-orange-500 rounded"></div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Now playing</h2>
              <p class="text-gray-600">Movies that are currently playing in theaters.</p>
            </div>
          </div>
          
          <!-- Navigation Arrows -->
          <div class="flex gap-2">
            <button class="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <button class="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Movies Carousel -->
        <div class="flex gap-6 overflow-x-auto pb-4 scrollbar-hide">
          <div 
            v-for="movie in trendingMovies.slice(0, 6)" 
            :key="movie.id"
            class="flex-shrink-0 w-48 group cursor-pointer"
          >
            <!-- Movie Poster with Play Button -->
            <div class="relative mb-3">
              <img 
                :src="movie.posterUrl" 
                :alt="movie.title"
                class="w-full h-72 object-cover rounded-lg shadow-md"
              />
              
              <!-- Play Button Overlay -->
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded-lg">
                <div class="bg-white/90 rounded-full p-3 transform scale-90 group-hover:scale-100 transition-transform">
                  <Play class="w-8 h-8 text-gray-800" fill="currentColor" />
                </div>
              </div>
              
              <!-- Rating Badge -->
              <div class="absolute top-3 left-3 bg-black/70 text-white px-2 py-1 rounded text-sm font-medium">
                <span class="text-yellow-400">⭐</span>
                {{ movie.lemonPieRating }} / 10
              </div>
            </div>
            
            <!-- Movie Title -->
            <h3 class="font-semibold text-gray-900 text-sm leading-tight group-hover:text-orange-500 transition-colors">
              {{ movie.title }}
            </h3>
          </div>
        </div>
      </div>
    </section>

    <!-- Trending TV Shows Section -->
    <section class="bg-white py-12">
      <div class="container mx-auto px-4">
        <!-- Section Header -->
        <div class="flex items-center justify-between mb-8">
          <div class="flex items-center gap-3">
            <div class="w-1 h-8 bg-orange-500 rounded"></div>
            <div>
              <h2 class="text-2xl font-bold text-gray-900">Trending TV shows</h2>
              <p class="text-gray-600">Currently trending TV shows.</p>
            </div>
          </div>
          
          <!-- Navigation Arrows -->
          <div class="flex gap-2">
            <button class="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
              </svg>
            </button>
            <button class="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <!-- TV Shows Carousel -->
        <div class="flex gap-6 overflow-x-auto pb-4 scrollbar-hide">
          <div 
            v-for="show in trendingTVShows" 
            :key="show.id"
            class="flex-shrink-0 w-48 group cursor-pointer"
          >
            <!-- TV Show Poster with Play Button -->
            <div class="relative mb-3">
              <img 
                :src="show.posterUrl" 
                :alt="show.title"
                class="w-full h-72 object-cover rounded-lg shadow-md"
              />
              
              <!-- Play Button Overlay -->
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded-lg">
                <div class="bg-white/90 rounded-full p-3 transform scale-90 group-hover:scale-100 transition-transform">
                  <Play class="w-8 h-8 text-gray-800" fill="currentColor" />
                </div>
              </div>
              
              <!-- Rating Badge -->
              <div class="absolute top-3 left-3 bg-black/70 text-white px-2 py-1 rounded text-sm font-medium">
                <span class="text-yellow-400">⭐</span>
                {{ show.lemonPieRating }} / 10
              </div>
            </div>
            
            <!-- TV Show Title -->
            <h3 class="font-semibold text-gray-900 text-sm leading-tight group-hover:text-orange-500 transition-colors">
              {{ show.title }}
            </h3>
          </div>
        </div>
      </div>
    </section>

    <!-- Up Next Section -->
    <section class="bg-gray-50 py-12">
      <div class="container mx-auto px-4">
        <div class="flex gap-8">
          <!-- Main Content Area -->
          <div class="flex-1">
            <!-- Placeholder for main content -->
          </div>
          
          <!-- Up Next Sidebar -->
          <div class="w-80 bg-white rounded-lg shadow-lg p-6">
            <h3 class="text-xl font-bold mb-6 text-gray-800">Up next</h3>
            <div class="space-y-4">
              <div 
                v-for="movie in trendingMovies.slice(0, 3)" 
                :key="movie.id"
                class="flex gap-3 group cursor-pointer"
              >
                <!-- Play Button -->
                <div class="relative flex-shrink-0">
                  <img 
                    :src="movie.posterUrl" 
                    :alt="movie.title"
                    class="w-16 h-24 object-cover rounded"
                  />
                  <div class="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity rounded">
                    <Play class="w-6 h-6 text-white" fill="currentColor" />
                  </div>
                </div>
                
                <!-- Movie Info -->
                <div class="flex-1 min-w-0">
                  <h4 class="font-semibold text-gray-800 truncate group-hover:text-orange-500 transition-colors">
                    {{ movie.title }}
                  </h4>
                  <div class="flex items-center gap-1 mt-1">
                    <span class="text-yellow-500">⭐</span>
                    <span class="text-sm font-medium">{{ movie.lemonPieRating }}</span>
                    <span class="text-sm text-gray-500">/ 10</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Latest Pies Section -->
    <section class="py-16 bg-base-100">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold mb-4 flex items-center justify-center gap-3">
            <span class="text-pie-brown">🥧</span>
            Latest Pies
            <span class="text-pie-brown">🥧</span>
          </h2>
          <p class="text-lg text-gray-600">
            Exceptional Nollywood films that deserve your attention
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <MovieCard 
            v-for="movie in pieMovies" 
            :key="movie.id" 
            :movie="movie"
          />
        </div>
        
        <div class="text-center mt-8">
          <button class="btn btn-primary btn-lg">
            View All Pies
          </button>
        </div>
      </div>
    </section>

    <!-- Fresh Lemons Section -->
    <section class="py-16 bg-lemon-yellow/5">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold mb-4 flex items-center justify-center gap-3">
            <span class="text-lemon-yellow">🍋</span>
            Fresh Lemons
            <span class="text-lemon-yellow">🍋</span>
          </h2>
          <p class="text-lg text-gray-600">
            Recent disappointments to help you avoid wasting your time
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <MovieCard 
            v-for="movie in lemonMovies" 
            :key="movie.id" 
            :movie="movie"
          />
        </div>
        
        <div class="text-center mt-8">
          <button class="btn btn-warning btn-lg">
            View All Lemons
          </button>
        </div>
      </div>
    </section>

    <!-- Trending Reviews Section -->
    <section class="py-16 bg-base-100">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold mb-4 flex items-center justify-center gap-3">
            <TrendingUp class="w-8 h-8 text-vibrant-orange" />
            Trending Reviews
          </h2>
          <p class="text-lg text-gray-600">
            What the Nollywood community is talking about
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <ReviewCard 
            v-for="review in trendingReviews" 
            :key="review.id" 
            :review="review"
            variant="compact"
          />
        </div>
        
        <div class="text-center mt-8">
          <button class="btn btn-accent btn-lg">
            Read More Reviews
          </button>
        </div>
      </div>
    </section>

    <!-- This Week in Nollywood Section -->
    <section class="py-16 bg-nigerian-green/5">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold mb-4 flex items-center justify-center gap-3">
            <Calendar class="w-8 h-8 text-nigerian-green" />
            This Week in Nollywood
          </h2>
          <p class="text-lg text-gray-600">
            Latest news and updates from the Nigerian film industry
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div 
            v-for="news in nollywoodNews" 
            :key="news.id"
            class="card bg-base-100 shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer"
          >
            <figure class="h-48">
              <img 
                :src="news.image" 
                :alt="news.title"
                class="w-full h-full object-cover"
              />
            </figure>
            <div class="card-body">
              <h3 class="card-title text-lg">{{ news.title }}</h3>
              <p class="text-gray-600 text-sm">{{ news.summary }}</p>
              <div class="flex items-center justify-between mt-4">
                <span class="text-xs text-gray-500">{{ news.date }}</span>
                <button class="btn btn-primary btn-sm">
                  Read More
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action Section -->
    <section class="py-16 bg-gradient-to-r from-nollywood-gold to-vibrant-orange">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold text-white mb-4">
          Join the LemonNPie Community
        </h2>
        <p class="text-xl text-white/90 mb-8">
          Share your thoughts on Nollywood films and help others discover great cinema
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <button class="btn btn-lg bg-white text-nollywood-gold hover:bg-gray-100">
            Sign Up Free
          </button>
          <button class="btn btn-lg btn-outline text-white border-white hover:bg-white hover:text-nollywood-gold">
            Write a Review
          </button>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -30px, 0);
  }
  70% {
    transform: translate3d(0, -15px, 0);
  }
  90% {
    transform: translate3d(0, -4px, 0);
  }
}

.animate-bounce {
  animation: bounce 2s infinite;
}
</style>
