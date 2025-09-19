<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Search } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useActorsStore } from '@/stores/actorsStore'
import { useUIStore } from '@/stores/uiStore'

const route = useRoute()
const router = useRouter()
const movieStore = useMovieStore()
const actorsStore = useActorsStore()
const uiStore = useUIStore()

const movieId = computed(() => route.params.id as string)
const movie = computed(() => movieStore.movies.find(m => m.id === movieId.value))
const loading = ref(false)

// Cast data with images
const castWithImages = computed(() => {
  if (!movie.value?.cast) return []
  
  // Map cast names to objects with images and roles
  return movie.value.cast.map((castMember, index) => {
    // Split the cast member name if it contains a role
    const parts = castMember.split(' as ')
    const name = parts[0]
    const role = parts.length > 1 ? parts[1] : movie.value?.title ? `Character in ${movie.value.title}` : 'Character'
    
    // Generate image URL based on actor name
    const imageUrl = `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(name + ' actor portrait')}&image_size=square_1_1`
    
    return {
      name,
      role,
      imageUrl
    }
  })
})

// Crew data with images (mock data for now)
const crewWithImages = computed(() => {
  if (!movie.value) return []
  
  // Mock crew data - in a real app, this would come from the API
  const mockCrew = [
    { name: 'John Director', role: 'Director', department: 'Directing' },
    { name: 'Jane Writer', role: 'Screenplay', department: 'Writing' },
    { name: 'Bob Producer', role: 'Producer', department: 'Production' },
    { name: 'Alice Cinematographer', role: 'Director of Photography', department: 'Camera' },
    { name: 'Charlie Editor', role: 'Film Editor', department: 'Editing' },
    { name: 'Diana Composer', role: 'Music Composer', department: 'Sound' },
    { name: 'Edward Designer', role: 'Production Designer', department: 'Art' },
    { name: 'Fiona Costumer', role: 'Costume Designer', department: 'Costume & Make-Up' },
    { name: 'George Sound', role: 'Sound Designer', department: 'Sound' },
    { name: 'Hannah VFX', role: 'Visual Effects Supervisor', department: 'Visual Effects' }
  ]
  
  return mockCrew.map(crewMember => {
    // Generate image URL based on crew member name
    const imageUrl = `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(crewMember.name + ' film crew portrait')}&image_size=square_1_1`
    
    return {
      ...crewMember,
      imageUrl
    }
  })
})

// Group crew by department
const crewByDepartment = computed(() => {
  const departments: Record<string, typeof crewWithImages.value> = {}
  
  crewWithImages.value.forEach(crewMember => {
    if (!departments[crewMember.department]) {
      departments[crewMember.department] = []
    }
    departments[crewMember.department].push(crewMember)
  })
  
  return departments
})

const navigateToActor = (actorName: string) => {
  // Find actor by name in the actors store
  const actor = actorsStore.actors.find(a => a.name === actorName)
  
  if (actor) {
    router.push({ name: 'person-details', params: { id: actor.id } })
  } else {
    // If actor not found, navigate to people page with search query
    router.push({ name: 'people', query: { search: actorName } })
  }
}

const navigateBack = () => {
  router.push({ name: 'movie-details', params: { id: movieId.value } })
}

onMounted(() => {
  if (movie.value) {
    uiStore.setPageTitle(`${movie.value.title} - Cast & Crew | LemonNPie`)
  } else {
    uiStore.setPageTitle('Cast & Crew | LemonNPie')
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <div v-if="loading" class="flex justify-center items-center min-h-screen">
      <div class="loading loading-spinner loading-lg text-primary"></div>
    </div>
    
    <div v-else-if="!movie" class="flex justify-center items-center min-h-screen">
      <div class="text-center">
        <h2 class="text-2xl font-bold text-white mb-4">Movie Not Found</h2>
        <router-link to="/movies" class="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-lg transition-colors">Back to Movies</router-link>
      </div>
    </div>
    
    <div v-else class="container mx-auto px-4 py-8">
      <!-- Header with back button -->
      <div class="flex items-center mb-8">
        <button 
          @click="navigateBack" 
          class="mr-4 p-2 rounded-full bg-gray-800 hover:bg-gray-700 transition-colors"
        >
          <ArrowLeft class="w-6 h-6" />
        </button>
        <h1 class="text-3xl font-bold">{{ movie.title }} - Cast & Crew</h1>
      </div>
      
      <!-- Cast Section -->
      <div class="mb-12">
        <h2 class="text-2xl font-semibold mb-6 flex items-center border-b border-gray-800 pb-2">
          <span class="mr-2">Cast</span>
          <span class="text-sm text-gray-400 font-normal">{{ movie?.cast?.length || 0 }} actors</span>
        </h2>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <div 
            v-for="(actor, index) in castWithImages" 
            :key="index" 
            class="bg-gray-800/50 rounded-lg p-4 hover:bg-gray-800 transition-colors border-l-4 border-orange-500/70 cursor-pointer"
            @click="navigateToActor(actor.name)"
          >
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 rounded-full overflow-hidden border-2 border-gray-700 flex-shrink-0 shadow-lg group">
                <img :src="actor.imageUrl" :alt="actor.name" class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110" />
              </div>
              <div class="flex-1">
                <h4 class="font-semibold text-lg">{{ actor.name }}</h4>
                <p class="text-gray-400 text-sm">{{ actor.role }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Crew Section -->
      <div>
        <h2 class="text-2xl font-semibold mb-6 flex items-center border-b border-gray-800 pb-2">
          <span class="mr-2">Crew</span>
          <span class="text-sm text-gray-400 font-normal">{{ crewWithImages.length }} crew members</span>
        </h2>
        
        <!-- Crew by Department -->
        <div v-for="(crew, department) in crewByDepartment" :key="department" class="mb-8">
          <h3 class="text-xl font-medium mb-4 text-orange-500">{{ department }}</h3>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <div 
              v-for="(member, index) in crew" 
              :key="index" 
              class="bg-gray-800/50 rounded-lg p-4 hover:bg-gray-800 transition-colors border-l-4 border-blue-500/70"
            >
              <div class="flex items-center gap-4">
                <div class="w-16 h-16 rounded-full overflow-hidden border-2 border-gray-700 flex-shrink-0 shadow-lg group">
                  <img :src="member.imageUrl" :alt="member.name" class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110" />
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-lg">{{ member.name }}</h4>
                  <p class="text-gray-400 text-sm">{{ member.role }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>