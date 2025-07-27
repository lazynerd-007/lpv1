<template>
  <div class="min-h-screen bg-gray-900">
    <div v-if="loading" class="flex justify-center items-center min-h-screen">
      <div class="loading loading-spinner loading-lg text-primary"></div>
    </div>
    
    <div v-else-if="!actor" class="flex justify-center items-center min-h-screen">
      <div class="text-center">
        <h2 class="text-2xl font-bold text-white mb-4">Person Not Found</h2>
        <router-link to="/people" class="btn btn-primary">Back to People</router-link>
      </div>
    </div>
    
    <div v-else class="container mx-auto px-4 py-8">
      <!-- Main Content -->
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Left Column - Photo and Basic Info -->
        <div class="lg:col-span-1">
          <!-- Actor Photo -->
          <div class="mb-6">
            <img 
              :src="actor.image" 
              :alt="actor.name"
              class="w-full rounded-lg shadow-lg"
            />
          </div>
          
          <!-- Personal Details -->
          <div class="bg-gray-800 rounded-lg p-6">
            <h3 class="text-lg font-bold text-white mb-4">Personal Info</h3>
            
            <div class="space-y-3">
              <div>
                <span class="text-gray-400 text-sm">Known for</span>
                <p class="text-white font-medium">Acting</p>
              </div>
              
              <div>
                <span class="text-gray-400 text-sm">Gender</span>
                <p class="text-white font-medium">{{ getGender(actor.name) }}</p>
              </div>
              
              <div>
                <span class="text-gray-400 text-sm">Known credits</span>
                <p class="text-white font-medium">{{ actor.movieCount }}</p>
              </div>
              
              <div>
                <span class="text-gray-400 text-sm">Born</span>
                <p class="text-white font-medium">{{ getBirthDate(actor.age) }} ({{ actor.age }} years old)</p>
              </div>
              
              <div v-if="actor.birthPlace">
                <span class="text-gray-400 text-sm">Birthplace</span>
                <p class="text-white font-medium">{{ actor.birthPlace }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column - Biography and Known For -->
        <div class="lg:col-span-3">
          <!-- Header with Name and Share Button -->
          <div class="flex justify-between items-start mb-6">
            <h1 class="text-4xl font-bold text-white">{{ actor.name }}</h1>
            <button class="btn btn-ghost text-orange-500 hover:bg-orange-500 hover:text-white">
              <Share2 class="w-5 h-5 mr-2" />
              Share
            </button>
          </div>
          
          <!-- Biography -->
          <div class="mb-8">
            <h2 class="text-xl font-bold text-white mb-4">Biography</h2>
            <div class="text-gray-300 leading-relaxed">
              <p class="mb-4">{{ getFullBiography(actor) }}</p>
              <button 
                v-if="!showFullBio && getFullBiography(actor).length > 300"
                @click="showFullBio = true"
                class="text-orange-500 hover:text-orange-400 font-medium"
              >
                Show more
              </button>
            </div>
          </div>
          
          <!-- Known For Section -->
          <div>
            <h2 class="text-xl font-bold text-white mb-6">Known for</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div 
                v-for="movie in knownForMovies" 
                :key="movie.id"
                class="bg-gray-800 rounded-lg overflow-hidden hover:bg-gray-700 transition-colors cursor-pointer"
                @click="navigateToMovie(movie.id)"
              >
                <img 
                  :src="movie.poster" 
                  :alt="movie.title"
                  class="w-full h-48 object-cover"
                />
                <div class="p-3">
                  <h3 class="text-white font-medium text-sm mb-1 line-clamp-2">{{ movie.title }}</h3>
                  <div class="flex items-center gap-2 text-xs text-gray-400">
                    <Star class="w-3 h-3 text-yellow-500" />
                    <span>{{ movie.lemonPieRating.toFixed(1) }}/10</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Share2, Star } from 'lucide-vue-next'
import { useActorsStore } from '@/stores/actorsStore'
import { useMovieStore } from '@/stores/movieStore'
import type { Movie } from '@/data/mockMovies'

const route = useRoute()
const router = useRouter()
const actorsStore = useActorsStore()
const movieStore = useMovieStore()

const loading = ref(true)
const showFullBio = ref(false)
const actorId = computed(() => route.params.id as string)
const actor = computed(() => actorsStore.getActorById(actorId.value))

// Mock movies for "Known for" section based on actor's knownFor array
const knownForMovies = computed(() => {
  if (!actor.value?.knownFor) return []
  
  // Create mock movies based on the actor's known works
  return actor.value.knownFor.slice(0, 4).map((title, index) => ({
    id: `${actor.value!.id}-movie-${index}`,
    title,
    releaseDate: `${2020 + index}-01-01`,
    year: 2020 + index,
    runtime: 120,
    genre: ['Drama', 'Action'],
    language: ['English'],
    director: 'Various',
    producer: 'Various',
    cast: [actor.value!.name],
    plotSummary: `A compelling story featuring ${actor.value!.name}.`,
    posterUrl: `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(`${title} movie poster cinematic`)}%20movie%20poster&image_size=portrait_4_3`,
    poster: `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(`${title} movie poster cinematic`)}%20movie%20poster&image_size=portrait_4_3`,
    productionCompany: 'Various Productions',
    filmingLocations: ['Lagos'],
    productionState: 'Lagos',
    streamingPlatforms: ['Netflix'],
    awards: [],
    lemonPieRating: parseFloat((Math.random() * 3 + 7).toFixed(1)),
    userRating: parseFloat((Math.random() * 3 + 7).toFixed(1)),
    criticRating: parseFloat((Math.random() * 3 + 7).toFixed(1)),
    reviewCount: Math.floor(Math.random() * 1000) + 100
  } as Movie))
})

const getGender = (name: string): string => {
  // Simple gender detection based on common names
  const femaleNames = ['katherina', 'jenna', 'sae', 'kim', 'kandi', 'lupita', 'zendaya']
  const firstName = name.toLowerCase().split(' ')[0]
  return femaleNames.some(female => firstName.includes(female)) ? 'Female' : 'Male'
}

const getBirthDate = (age: number): string => {
  const currentYear = new Date().getFullYear()
  const birthYear = currentYear - age
  // Generate a random month and day
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 
                 'July', 'August', 'September', 'October', 'November', 'December']
  const month = months[Math.floor(Math.random() * 12)]
  const day = Math.floor(Math.random() * 28) + 1
  return `${month} ${day}, ${birthYear}`
}

const getFullBiography = (actor: any): string => {
  if (!actor.biography) return 'Biography information not available.'
  
  // Expand the biography with more details
  const baseBio = actor.biography
  const expandedBio = `${baseBio}. Known for their versatile acting style and compelling screen presence, ${actor.name} has become one of the most recognizable faces in cinema. With ${actor.movieCount} film credits to their name, they have worked with renowned directors and fellow actors across various genres. Their performances have garnered critical acclaim and a dedicated fan following worldwide.`
  
  return showFullBio.value ? expandedBio : baseBio
}

const navigateToMovie = (movieId: string) => {
  // For now, just log the navigation since these are mock movies
  console.log('Navigate to movie:', movieId)
}

onMounted(async () => {
  // Ensure actors are loaded
  if (actorsStore.actors.length === 0) {
    actorsStore.loadInitialActors()
  }
  
  loading.value = false
  
  // If actor not found, try loading more actors
  if (!actor.value) {
    await actorsStore.loadMoreActors()
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>