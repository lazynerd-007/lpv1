<script setup lang="ts">
import { ref, computed } from 'vue'
import { MapPin, Play, Star, Calendar, Users } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useRouter } from 'vue-router'

const movieStore = useMovieStore()
const router = useRouter()

const selectedRegion = ref('Lagos')

// Regional data with cultural context
const regions = [
  {
    name: 'Lagos',
    description: 'Commercial hub of Nollywood',
    color: 'from-blue-500 to-cyan-500',
    bgColor: 'bg-blue-50',
    textColor: 'text-blue-700',
    borderColor: 'border-blue-200',
    icon: '🏙️',
    characteristics: ['Urban stories', 'Modern themes', 'High production values'],
    totalMovies: 45
  },
  {
    name: 'Enugu',
    description: 'Heartland of Nollywood',
    color: 'from-green-500 to-emerald-500',
    bgColor: 'bg-green-50',
    textColor: 'text-green-700',
    borderColor: 'border-green-200',
    icon: '🎬',
    characteristics: ['Traditional stories', 'Cultural themes', 'Igbo language films'],
    totalMovies: 38
  },
  {
    name: 'Kano',
    description: 'Home of Kannywood',
    color: 'from-orange-500 to-red-500',
    bgColor: 'bg-orange-50',
    textColor: 'text-orange-700',
    borderColor: 'border-orange-200',
    icon: '🕌',
    characteristics: ['Hausa cinema', 'Northern culture', 'Islamic themes'],
    totalMovies: 22
  },
  {
    name: 'Abuja',
    description: 'Modern Nigerian cinema',
    color: 'from-purple-500 to-pink-500',
    bgColor: 'bg-purple-50',
    textColor: 'text-purple-700',
    borderColor: 'border-purple-200',
    icon: '🏛️',
    characteristics: ['Political dramas', 'Contemporary stories', 'Elite narratives'],
    totalMovies: 18
  }
]

// Get movies by region
const getMoviesByRegion = (regionName: string) => {
  return movieStore.movies.filter(movie => 
    movie.productionState === regionName
  ).slice(0, 4)
}

const currentRegionMovies = computed(() => {
  return getMoviesByRegion(selectedRegion.value)
})

const currentRegionData = computed(() => {
  return regions.find(region => region.name === selectedRegion.value)
})

const navigateToMovie = (movieId: string) => {
  router.push(`/movie/${movieId}`)
}

const exploreRegion = (regionName: string) => {
  router.push({
    path: '/search',
    query: { state: regionName }
  })
}
</script>

<template>
  <section class="py-16 bg-gradient-to-br from-theme-background via-theme-surface to-theme-background">
    <div class="container mx-auto px-4">
      <!-- Section Header -->
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-theme-primary mb-4">
          🇳🇬 Regional Showcase
        </h2>
        <p class="text-lg text-theme-secondary max-w-3xl mx-auto">
          Discover the diverse cinematic landscapes of Nigeria. From Lagos' urban narratives to Enugu's cultural stories, 
          explore how different regions shape Nollywood's rich storytelling tradition.
        </p>
      </div>

      <!-- Regional Navigation -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-12">
        <button
          v-for="region in regions"
          :key="region.name"
          @click="selectedRegion = region.name"
          :class="[
            'p-6 rounded-xl border-2 transition-all duration-300 hover:scale-105 hover:shadow-lg',
            selectedRegion === region.name
              ? `${region.bgColor} ${region.borderColor} ${region.textColor} shadow-lg scale-105`
              : 'bg-theme-surface border-theme-border text-theme-secondary hover:bg-theme-accent'
          ]"
        >
          <div class="text-center">
            <div class="text-3xl mb-2">{{ region.icon }}</div>
            <h3 class="font-bold text-lg mb-1">{{ region.name }}</h3>
            <p class="text-sm opacity-80 mb-2">{{ region.description }}</p>
            <div class="text-xs font-medium">
              {{ region.totalMovies }} movies
            </div>
          </div>
        </button>
      </div>

      <!-- Selected Region Details -->
      <div v-if="currentRegionData" class="mb-8">
        <div :class="[
          'rounded-2xl p-8 border-2',
          currentRegionData.bgColor,
          currentRegionData.borderColor
        ]">
          <div class="flex flex-col md:flex-row items-start gap-6">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-4">
                <div class="text-4xl">{{ currentRegionData.icon }}</div>
                <div>
                  <h3 :class="['text-2xl font-bold', currentRegionData.textColor]">
                    {{ currentRegionData.name }} Cinema
                  </h3>
                  <p :class="['text-lg', currentRegionData.textColor, 'opacity-80']">
                    {{ currentRegionData.description }}
                  </p>
                </div>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div 
                  v-for="characteristic in currentRegionData.characteristics"
                  :key="characteristic"
                  :class="[
                    'p-3 rounded-lg border',
                    'bg-white/50',
                    currentRegionData.borderColor,
                    currentRegionData.textColor
                  ]"
                >
                  <div class="text-sm font-medium">{{ characteristic }}</div>
                </div>
              </div>
              
              <button
                @click="exploreRegion(currentRegionData.name)"
                :class="[
                  'btn btn-lg',
                  currentRegionData.textColor.replace('text-', 'btn-')
                ]"
              >
                <MapPin class="w-5 h-5 mr-2" />
                Explore All {{ currentRegionData.name }} Movies
              </button>
            </div>
            
            <!-- Regional Stats -->
            <div class="bg-white/70 rounded-xl p-6 min-w-[200px]">
              <h4 :class="['font-bold text-lg mb-4', currentRegionData.textColor]">
                Regional Stats
              </h4>
              <div class="space-y-3">
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Total Movies</span>
                  <span :class="['font-bold', currentRegionData.textColor]">
                    {{ currentRegionData.totalMovies }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Featured</span>
                  <span :class="['font-bold', currentRegionData.textColor]">
                    {{ currentRegionMovies.length }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-sm text-gray-600">Avg Rating</span>
                  <span :class="['font-bold', currentRegionData.textColor]">
                    {{ (currentRegionMovies.reduce((sum, movie) => sum + movie.lemonPieRating, 0) / currentRegionMovies.length || 0).toFixed(1) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Featured Movies from Selected Region -->
      <div v-if="currentRegionMovies.length > 0">
        <h3 class="text-2xl font-bold text-theme-primary mb-6 text-center">
          Featured Movies from {{ selectedRegion }}
        </h3>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div
            v-for="movie in currentRegionMovies"
            :key="movie.id"
            class="group cursor-pointer"
            @click="navigateToMovie(movie.id)"
          >
            <div class="bg-theme-surface rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 group-hover:scale-105">
              <!-- Movie Poster -->
              <div class="relative aspect-[2/3] overflow-hidden">
                <img
                  :src="movie.poster"
                  :alt="movie.title"
                  class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                />
                <div class="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-colors duration-300 flex items-center justify-center">
                  <Play class="w-12 h-12 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                </div>
                
                <!-- Rating Badge -->
                <div class="absolute top-3 right-3 bg-black/70 text-white px-2 py-1 rounded-lg flex items-center gap-1">
                  <Star class="w-3 h-3 fill-yellow-400 text-yellow-400" />
                  <span class="text-xs font-bold">{{ movie.lemonPieRating }}</span>
                </div>
              </div>
              
              <!-- Movie Info -->
              <div class="p-4">
                <h4 class="font-bold text-theme-primary mb-2 line-clamp-2">
                  {{ movie.title }}
                </h4>
                
                <div class="flex items-center gap-4 text-sm text-theme-tertiary mb-3">
                  <div class="flex items-center gap-1">
                    <Calendar class="w-3 h-3" />
                    <span>{{ movie.year }}</span>
                  </div>
                  <div class="flex items-center gap-1">
                    <Users class="w-3 h-3" />
                    <span>{{ movie.genre }}</span>
                  </div>
                </div>
                
                <p class="text-sm text-theme-secondary line-clamp-3">
                  {{ movie.plotSummary }}
                </p>
                
                <!-- Regional Badge -->
                <div class="mt-3 pt-3 border-t border-theme-border">
                  <div :class="[
                    'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
                    currentRegionData?.bgColor,
                    currentRegionData?.textColor
                  ]">
                    <MapPin class="w-3 h-3" />
                    {{ movie.productionState }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <div class="text-6xl mb-4">🎬</div>
        <h3 class="text-xl font-bold text-theme-primary mb-2">
          No movies found for {{ selectedRegion }}
        </h3>
        <p class="text-theme-secondary">
          Check back soon for more movies from this region!
        </p>
      </div>
      
      <!-- Call to Action -->
      <div class="text-center mt-12">
        <div class="bg-gradient-to-r from-orange-500 to-red-500 rounded-2xl p-8 text-white">
          <h3 class="text-2xl font-bold mb-4">
            🌍 Explore Nigeria's Cinematic Diversity
          </h3>
          <p class="text-lg mb-6 opacity-90">
            From the bustling streets of Lagos to the cultural heart of Enugu, discover how each region 
            contributes its unique voice to the Nollywood story.
          </p>
          <button
            @click="router.push('/search')"
            class="btn btn-lg bg-white text-orange-600 hover:bg-gray-100 border-none"
          >
            <MapPin class="w-5 h-5 mr-2" />
            Discover All Regions
          </button>
        </div>
      </div>
    </div>
  </section>
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