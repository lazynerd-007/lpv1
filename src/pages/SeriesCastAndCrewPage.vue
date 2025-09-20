<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Search } from 'lucide-vue-next'
import { useSeriesStore } from '@/stores/seriesStore'
import { useActorsStore } from '@/stores/actorsStore'
import { useUIStore } from '@/stores/uiStore'

const route = useRoute()
const router = useRouter()
const seriesStore = useSeriesStore()
const actorsStore = useActorsStore()
const uiStore = useUIStore()

const seriesId = computed(() => route.params.id as string)
const series = computed(() => seriesStore.series.find(s => s.id === seriesId.value))
const loading = ref(false)

// Cast data with images
const castWithImages = computed(() => {
  if (!series.value?.cast) return []
  
  // Map cast names to objects with images and roles
  return series.value.cast.map((castMember, index) => {
    // Split the cast member name if it contains a role
    const parts = castMember.split(' as ')
    const name = parts[0]
    const role = parts.length > 1 ? parts[1] : series.value?.title ? `Character in ${series.value.title}` : 'Character'
    
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
  if (!series.value) return []
  
  // Mock crew data - in a real app, this would come from the API
  const mockCrew = [
    { name: series.value.creator || 'John Creator', role: 'Creator', department: 'Writing' },
    { name: series.value.producer || 'Jane Producer', role: 'Executive Producer', department: 'Production' },
    { name: 'Bob Director', role: 'Director', department: 'Directing' },
    { name: 'Alice Writer', role: 'Writer', department: 'Writing' },
    { name: 'Charlie Cinematographer', role: 'Director of Photography', department: 'Camera' },
    { name: 'Diana Editor', role: 'Editor', department: 'Editing' },
    { name: 'Edward Composer', role: 'Music Composer', department: 'Sound' },
    { name: 'Fiona Designer', role: 'Production Designer', department: 'Art' },
    { name: 'George Costumer', role: 'Costume Designer', department: 'Costume & Make-Up' },
    { name: 'Hannah Sound', role: 'Sound Designer', department: 'Sound' },
    { name: 'Ian VFX', role: 'Visual Effects Supervisor', department: 'Visual Effects' },
    { name: 'Julia Casting', role: 'Casting Director', department: 'Production' }
  ]
  
  return mockCrew.map(crewMember => {
    // Generate image URL based on crew member name
    const imageUrl = `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(crewMember.name + ' TV series crew portrait')}&image_size=square_1_1`
    
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
  router.push({ name: 'series-details', params: { id: seriesId.value } })
}

onMounted(() => {
  if (series.value) {
    uiStore.setPageTitle(`${series.value.title} - Cast & Crew | LemonNPie`)
  } else {
    uiStore.setPageTitle('Series Cast & Crew | LemonNPie')
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <div v-if="loading" class="flex justify-center items-center min-h-screen">
      <div class="loading loading-spinner loading-lg text-primary"></div>
    </div>
    
    <div v-else-if="!series" class="flex justify-center items-center min-h-screen">
      <div class="text-center">
        <h2 class="text-2xl font-bold text-white mb-4">Series Not Found</h2>
        <router-link to="/series" class="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-lg transition-colors">Back to Series</router-link>
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
        <div>
          <h1 class="text-3xl font-bold">{{ series.title }} - Cast & Crew</h1>
          <p class="text-gray-400 mt-1">{{ series.seasons }} Season{{ series.seasons !== 1 ? 's' : '' }} • {{ series.episodes }} Episodes</p>
        </div>
      </div>
      
      <!-- Cast Section -->
      <div class="mb-12">
        <h2 class="text-2xl font-semibold mb-6 flex items-center border-b border-gray-800 pb-2">
          <span class="mr-2">Cast</span>
          <span class="text-sm text-gray-400 font-normal">{{ series?.cast?.length || 0 }} actors</span>
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