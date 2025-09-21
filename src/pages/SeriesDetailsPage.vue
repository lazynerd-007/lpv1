<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Star, Clock, Calendar, MapPin, Award, Play, Heart, Share2, MessageCircle, User, Plus, ChevronDown, Check } from 'lucide-vue-next'
import { useSeriesStore } from '@/stores/seriesStore'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import { useActorsStore, type Actor } from '@/stores/actorsStore'
import ReviewCard from '@/components/ui/ReviewCard.vue'

interface Props {
  id?: string
}

const props = defineProps<Props>()
const route = useRoute()
const router = useRouter()
const seriesStore = useSeriesStore()
const userStore = useUserStore()
const uiStore = useUIStore()

const seriesId = computed(() => props.id || route.params.id as string)
const series = computed(() => seriesStore.series.find(s => s.id === seriesId.value))
const reviews = computed(() => seriesStore.currentSeriesReviews)
const activeTab = ref('reviews')
const showAllReviews = ref(false)
const showAllCritics = ref(false)
const reviewsToShow = computed(() => showAllReviews.value ? reviews.value : reviews.value.slice(0, 5))
const hasMoreReviews = computed(() => reviews.value.length > 5)
const criticsToShow = computed(() => {
  const criticsArray = critics.value
  if (!criticsArray || !Array.isArray(criticsArray)) return []
  return showAllCritics.value ? criticsArray : criticsArray.slice(0, 5)
})
const hasMoreCritics = computed(() => {
  const criticsArray = critics.value
  return criticsArray && Array.isArray(criticsArray) && criticsArray.length > 5
})

// Get similar series based on genre matching
const similarSeries = computed(() => {
  if (!series.value) return []
  
  return seriesStore.series
    .filter(s => 
      s.id !== seriesId.value && // Not the current series
      s.genre.some(g => series.value?.genre.includes(g)) // Has at least one matching genre
    )
    .sort((a, b) => {
      // Count matching genres for better sorting
      const aMatches = a.genre.filter(g => series.value?.genre.includes(g)).length
      const bMatches = b.genre.filter(g => series.value?.genre.includes(g)).length
      return bMatches - aMatches
    })
    .slice(0, 10) // Limit to 10 similar series
})

// Reference to the similar series scroll container
const similarSeriesContainer = ref<HTMLElement | null>(null)

// Function to navigate to a series details page
const navigateToSeries = (seriesId: string) => {
  router.push({ name: 'series-details', params: { id: seriesId } })
}

// Functions to scroll the similar series container left and right
const scrollLeft = () => {
  if (similarSeriesContainer.value) {
    similarSeriesContainer.value.scrollBy({ left: -300, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (similarSeriesContainer.value) {
    similarSeriesContainer.value.scrollBy({ left: 300, behavior: 'smooth' })
  }
}

// Sample critics data
const critics = computed(() => {
  // The TVShow interface doesn't have a critics property, so we'll always use our sample data
  return [
    {
      source: 'The Guardian',
      date: '2 days ago',
      rating: 8,
      title: 'A Masterpiece of Nigerian Television',
      content: 'This series represents a significant leap forward for Nollywood television, combining compelling storytelling with exceptional production values. The performances are nuanced and the direction is confident throughout.'
    },
    {
      source: 'Variety',
      date: '1 week ago',
      rating: 7.5,
      title: 'Impressive Technical Achievement',
      content: 'While the narrative occasionally stumbles, the technical prowess on display is undeniable. The cinematography and sound design elevate this above typical genre fare.'
    },
    {
      source: 'Film Comment',
      date: '3 days ago',
      rating: 8.5,
      title: 'Bold Vision and Execution',
      content: 'The creators demonstrate remarkable control over the material, balancing cultural specificity with universal themes. The result is a series that feels both authentic and accessible to international audiences.'
    },
    {
      source: 'The New York Times',
      date: '5 days ago',
      rating: 7,
      title: 'Promising But Uneven',
      content: 'There are moments of brilliance throughout, though the pacing issues in some episodes prevent it from achieving greatness. Nevertheless, it represents an important voice in contemporary African television.'
    },
    {
      source: 'IndieWire',
      date: '1 week ago',
      rating: 8.2,
      title: 'Culturally Rich and Engaging',
      content: 'A series that successfully bridges local storytelling traditions with modern television sensibilities. The cast delivers compelling performances that bring depth to every character.'
    }
  ];
});

// Computed property for average rating
const averageRating = computed(() => {
  if (!series.value) return 0
  return (series.value.userRating + series.value.lemonPieRating + series.value.criticRating) / 3
})

// Cast with images
const castWithImages = computed(() => {
  if (!series.value?.cast) return []
  
  return series.value.cast.map((actorString: string) => {
    // Split by common delimiters to separate name from role
    const parts = actorString.split(/\s+as\s+|\s+-\s+|\s+\(|\)|,/)
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

const isInWatchlist = computed(() => {
  return userStore.isInWatchlist(seriesId.value)
})

const isInFavorites = computed(() => {
  return userStore.isInFavorites(seriesId.value)
})

const toggleWatchlist = async () => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (isInWatchlist.value) {
      await userStore.removeFromWatchlist(seriesId.value)
    } else {
      await userStore.addToWatchlist(seriesId.value)
    }
  } catch (error) {
    console.error('Error updating watchlist:', error)
  }
}

const toggleFavorites = async () => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (isInFavorites.value) {
      await userStore.removeFromFavorites(seriesId.value)
    } else {
      await userStore.addToFavorites(seriesId.value)
    }
  } catch (error) {
    console.error('Error updating favorites:', error)
  }
}

const playTrailer = () => {
  if (series.value) {
    uiStore.openTrailerModal(series.value.id, series.value.trailerUrl || '')
  }
}

const shareSeries = async () => {
  if (navigator.share && series.value) {
    try {
      await navigator.share({
        title: series.value.title,
        text: `Check out ${series.value.title} on Nollywood Series`,
        url: window.location.href
      })
    } catch (error) {
      // Fallback to copying to clipboard
      navigator.clipboard.writeText(window.location.href)
    }
  } else {
    // Fallback to copying to clipboard
    navigator.clipboard.writeText(window.location.href)
  }
}

const navigateToActor = (actorName: string) => {
  // Find actor by name in the actors store
  const actorStore = useActorsStore()
  const actor = actorStore.actors.find(a => a.name === actorName)
  
  if (actor) {
    router.push({ name: 'person-details', params: { id: actor.id } })
  } else {
    // If actor not found, create a new actor entry with a unique ID
    const newActorId = `temp-${Date.now()}`
    const newActor: Actor = {
      id: newActorId,
      name: actorName,
      age: 0, // Default values
      image: `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20${encodeURIComponent(actorName)}&image_size=square`,
      popularity: 0,
      movieCount: 1
    }
    
    // Add the new actor to the store
    actorStore.addActor(newActor)
    
    // Navigate to the new actor's details page
    router.push({ name: 'person-details', params: { id: newActorId } })
  }
}

const viewAllCast = () => {
  if (series.value) {
    // Navigate to the dedicated cast and crew page for this series
    router.push({ name: 'series-cast-crew', params: { id: seriesId.value } })
  }
}

const handleReviewAction = async (action: string, reviewId: string) => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    switch (action) {
      case 'like':
        // Like functionality not implemented yet
        break
      case 'dislike':
        // Dislike functionality not implemented yet
        break
      case 'report':
        // Report functionality not implemented yet
        break
      case 'edit':
        router.push(`/write-review?series=${seriesId.value}&edit=${reviewId}`)
        break
      case 'delete':
        // Delete review functionality not implemented yet
        console.log('Delete review:', reviewId)
        break
    }
  } catch (error) {
    console.error('Error handling review action:', error)
  }
}

onMounted(async () => {
  // Set current series for detailed view
  if (series.value) {
    // Set current series in store for reviews
    seriesStore.currentSeries = series.value
    uiStore.setPageTitle(`${series.value.title} - Nollywood Series`)
  } else {
    uiStore.setPageTitle('Series Not Found - Nollywood Series')
  }
})
</script>

<template>
  <div v-if="series" class="min-h-screen bg-gray-900 text-white">
    <!-- Hero Video Section -->
    <div class="relative w-full h-[500px] mb-8">
      <div class="relative group cursor-pointer bg-gray-800 w-full h-full overflow-hidden">
        <img 
          :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(series.title + ' TV series cinematic scene')}&image_size=landscape_16_9`" 
          :alt="`${series.title} trailer`" 
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center group-hover:bg-opacity-60 transition-all duration-300">
          <div class="bg-orange-500 hover:bg-orange-600 rounded-full p-6 transform group-hover:scale-110 transition-transform duration-300">
            <Play class="w-12 h-12 text-white" />
          </div>
        </div>
        <div class="absolute bottom-6 left-6 bg-black bg-opacity-75 text-white px-4 py-3 rounded">
          <h4 class="text-xl font-semibold">{{ series.title }} - Official Trailer</h4>
          <p class="text-sm text-gray-300">2:34</p>
        </div>
        <!-- Series Info Overlay -->
        <div class="absolute top-6 right-6 bg-black bg-opacity-75 text-white px-4 py-3 rounded">
          <div class="flex items-center gap-2 mb-2">
            <Star class="w-5 h-5 text-yellow-400 fill-current" />
            <span class="text-lg font-bold">{{ averageRating.toFixed(1) }}</span>
            <span class="text-gray-300">/ 10</span>
          </div>
          <p class="text-sm text-gray-300">{{ series.releaseDate }} • {{ series.seasons }} Season{{ series.seasons !== 1 ? 's' : '' }} • {{ series.episodes }} Episodes</p>
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column - Series Poster -->
        <div class="lg:col-span-1">
          <div class="sticky top-8">
            <!-- Series Poster (Prominently Displayed) -->
          <div class="relative overflow-hidden rounded-lg shadow-2xl border-2 border-orange-500/20 hover:border-orange-500/40 transition-colors duration-300">
            <img
              :src="series.posterUrl"
              :alt="series.title"
              class="w-full object-cover rounded-lg transform hover:scale-105 transition-transform duration-300"
            />
            <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent h-24"></div>
            <div class="absolute top-0 right-0 m-3 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded shadow-lg">
              {{ series.lemonPieRating.toFixed(1) }}/10
            </div>
          </div>
            
            <!-- Action Buttons -->
            <div class="mt-6 space-y-3">
              <button
                @click="toggleWatchlist"
                class="w-full bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
              >
                <Plus v-if="!isInWatchlist" class="w-5 h-5" />
                <Check v-else class="w-5 h-5" />
                {{ isInWatchlist ? 'Remove from watchlist' : 'Add to watchlist' }}
              </button>
              <button
                @click="shareSeries"
                class="w-full bg-transparent text-white border border-gray-600 hover:bg-gray-800 px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
              >
                <Share2 class="w-5 h-5" />
                Share
              </button>
            </div>
            
            <!-- Series Info Sidebar -->
            <div class="mt-8 space-y-4 text-sm">
              <div>
                <span class="text-gray-400">Original language</span>
                <p class="text-white">{{ series.language.join(', ') }}</p>
              </div>
              <div>
                <span class="text-gray-400">Seasons</span>
                <p class="text-white">{{ series.seasons }}</p>
              </div>
              <div>
                <span class="text-gray-400">Episodes</span>
                <p class="text-white">{{ series.episodes }}</p>
              </div>
              <div>
                <span class="text-gray-400">Production countries</span>
                <p class="text-white">{{ series.productionState }}</p>
              </div>
              <div>
                <span class="text-gray-400">Keywords</span>
                <div class="flex flex-wrap gap-1 mt-1">
                  <span v-for="genre in series.genre" :key="genre" class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs">{{ genre }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column - Series Details -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Series Title and Basic Info -->
          <div>
            <h1 class="text-4xl md:text-5xl font-bold mb-4">{{ series.title }}</h1>
            <div class="flex items-center gap-4 mb-4 text-sm">
              <span class="text-gray-400">{{ series.releaseDate }}</span>
              <span class="text-gray-400">•</span>
              <span class="text-gray-400">{{ series.seasons }} Season{{ series.seasons !== 1 ? 's' : '' }} • {{ series.episodes }} Episodes</span>
              <div class="flex items-center gap-1">
                <span v-for="genre in series.genre.slice(0, 3)" :key="genre" class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs">{{ genre }}</span>
              </div>
            </div>
            
            <!-- Rating -->
            <div class="flex items-center gap-6 mb-6">
              <div class="flex items-center gap-2">
                <Star class="w-6 h-6 text-yellow-400 fill-current" />
                <span class="text-2xl font-bold">{{ averageRating.toFixed(1) }}</span>
                <span class="text-gray-400">/ 10</span>
              </div>
              <button class="text-blue-400 hover:text-blue-300 text-sm font-medium flex items-center gap-1">
                <Star class="w-4 h-4" />
                Rate this
              </button>
            </div>
            
            <!-- Plot Summary -->
            <p class="text-gray-300 leading-relaxed mb-6">{{ series.plotSummary }}</p>
            
            <!-- Creator and Producer -->
            <div class="space-y-2 text-sm mb-8">
              <div class="flex">
                <span class="text-gray-400 w-20">Creator</span>
                <span class="text-blue-400 hover:text-blue-300 cursor-pointer">{{ series.creator }}</span>
              </div>
              <div class="flex">
                <span class="text-gray-400 w-20">Producer</span>
                <span class="text-blue-400 hover:text-blue-300 cursor-pointer">{{ series.producer }}</span>
              </div>
              <div class="flex">
                <span class="text-gray-400 w-20">Stars</span>
                <div class="flex flex-wrap gap-1">
                  <span v-for="(actor, index) in series.cast.slice(0, 3)" :key="actor" class="text-blue-400 hover:text-blue-300 cursor-pointer">
                    {{ actor }}<span v-if="index < series.cast.slice(0, 3).length - 1">, </span>
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Seasons Section -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Seasons</h3>
              <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
                <div v-for="seasonNumber in series.seasons" :key="seasonNumber" class="bg-gray-800 rounded-lg p-4 flex flex-col items-center justify-center aspect-square">
                  <h4 class="text-lg font-semibold">Season {{ seasonNumber }}</h4>
                  <p class="text-sm text-gray-400 mt-1">Details coming soon</p>
                </div>
              </div>
            </div>
            
            <!-- Hero Image Gallery -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Series Stills</h3>
              <div class="relative">
                <div class="flex overflow-x-auto pb-4 space-x-4 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg flex-shrink-0">
                    <img 
                      :src="series.posterUrl" 
                      :alt="`${series.title} still 1`" 
                      class="h-32 w-auto min-w-[180px] object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                  </div>
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg flex-shrink-0">
                    <img 
                      :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(series.title + ' TV series scene')}&image_size=landscape_16_9`" 
                      :alt="`${series.title} still 2`" 
                      class="h-32 w-auto min-w-[180px] object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                  </div>
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg flex-shrink-0">
                    <img 
                      :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(series.title + ' TV series character')}&image_size=portrait_4_3`" 
                      :alt="`${series.title} still 3`" 
                      class="h-32 w-auto min-w-[180px] object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                  </div>
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg flex-shrink-0">
                    <img 
                      :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(series.title + ' TV series behind scenes')}&image_size=landscape_16_9`" 
                      :alt="`${series.title} still 4`" 
                      class="h-32 w-auto min-w-[180px] object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Additional Images Section -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Gallery</h3>
              <div class="relative">
                <div class="flex overflow-x-auto pb-4 space-x-4 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                  <img 
                    v-for="i in 8" 
                    :key="i" 
                    :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(series.title + (i % 2 === 0 ? ' TV series scene ' : ' character ') + i)}&image_size=${i % 2 === 0 ? 'landscape_16_9' : 'portrait_4_3'}`" 
                    :alt="`${series.title} Gallery Image ${i}`" 
                    class="h-40 w-auto min-w-[200px] object-cover rounded-lg cursor-pointer hover:opacity-80 transition-opacity flex-shrink-0" 
                  />
                </div>
              </div>
            </div>
          </div>
          
          <!-- Content Tabs -->
          <div>
            <div class="flex border-b border-gray-700 mb-6">
              <button 
                @click="activeTab = 'reviews'"
                :class="[
                  'px-4 py-2 font-medium transition-colors border-b-2 text-sm',
                  activeTab === 'reviews'
                    ? 'border-orange-500 text-orange-500'
                    : 'border-transparent text-gray-400 hover:text-white'
                ]"
              >
                Reviews ({{ reviews.length }})
              </button>
              <button 
                @click="activeTab = 'critics'"
                :class="[
                  'px-4 py-2 font-medium transition-colors border-b-2 text-sm',
                  activeTab === 'critics'
                    ? 'border-orange-500 text-orange-500'
                    : 'border-transparent text-gray-400 hover:text-white'
                ]"
              >
                Critics
              </button>
            </div>
            
            <!-- Critics Tab -->
            <div v-if="activeTab === 'critics'" class="space-y-6">
              <div v-for="(critic, index) in criticsToShow" :key="index" class="bg-gray-800 rounded-lg p-6">
                <div class="flex items-start gap-4">
                  <div class="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center">
                    <User class="w-6 h-6 text-gray-400" />
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="font-semibold">{{ critic.source }}</span>
                      <span class="text-gray-400 text-sm">{{ critic.date }}</span>
                    </div>
                    <div class="flex items-center gap-1 mb-3">
                      <Star v-for="i in Math.round(critic.rating / 2)" :key="i" class="w-4 h-4 text-yellow-400 fill-current" />
                      <Star v-for="i in (5 - Math.round(critic.rating / 2))" :key="i + Math.round(critic.rating / 2)" class="w-4 h-4 text-gray-400" />
                      <span class="text-sm text-gray-400 ml-2">{{ critic.rating }} / 10</span>
                    </div>
                    <h4 class="font-semibold mb-2">{{ critic.title }}</h4>
                    <p class="text-gray-300 leading-relaxed">{{ critic.content }}</p>
                  </div>
                </div>
              </div>
              
              <div v-if="hasMoreCritics" class="flex justify-center mt-6">
                <button 
                  @click="showAllCritics = !showAllCritics" 
                  class="flex items-center gap-2 px-6 py-2 bg-gray-800 hover:bg-gray-700 rounded-full text-gray-300 hover:text-white transition-colors"
                >
                  <span>{{ showAllCritics ? 'Show Less' : `Show More (${(critics?.length || 0) - 5})` }}</span>
                  <ChevronDown :class="{'transform rotate-180': showAllCritics}" class="w-4 h-4 transition-transform" />
                </button>
              </div>
            </div>
            
            <!-- Reviews Tab -->
            <div v-if="activeTab === 'reviews'" class="space-y-6">
              <!-- Sample User Review -->
              <div class="bg-gray-800 rounded-lg p-6">
                <div class="flex items-start gap-4">
                  <div class="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center">
                    <User class="w-6 h-6 text-gray-400" />
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="font-semibold">Logan Roberts</span>
                      <span class="text-gray-400 text-sm">4 days ago</span>
                    </div>
                    <div class="flex items-center gap-1 mb-3">
                      <Star v-for="i in 5" :key="i" class="w-4 h-4 text-yellow-400 fill-current" />
                      <span class="text-sm text-gray-400 ml-2">9 / 10</span>
                    </div>
                    <h4 class="font-semibold mb-2">Engaging and Well-Crafted</h4>
                    <p class="text-gray-300 leading-relaxed">This series is a captivating journey from start to finish. The character development is exceptional, and the storytelling keeps you engaged throughout every episode. The production quality is top-notch.</p>
                    <div class="flex items-center gap-4 mt-4 text-sm">
                      <span class="text-gray-400">Was this review helpful?</span>
                      <button class="text-blue-400 hover:text-blue-300">YES</button>
                      <button class="text-blue-400 hover:text-blue-300">NO</button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="reviews.length === 0" class="text-center py-8 text-gray-400">
                <MessageCircle class="w-12 h-12 mx-auto mb-4 text-gray-500" />
                <p>No reviews yet. Be the first to review this series!</p>
              </div>
              
              <div v-else class="space-y-4">
                <ReviewCard 
                  v-for="review in reviewsToShow" 
                  :key="review.id" 
                  :review="review"
                  :show-movie-title="false"
                  @action="handleReviewAction"
                />
                
                <div v-if="hasMoreReviews" class="flex justify-center mt-6">
                  <button 
                    @click="showAllReviews = !showAllReviews" 
                    class="flex items-center gap-2 px-6 py-2 bg-gray-800 hover:bg-gray-700 rounded-full text-gray-300 hover:text-white transition-colors"
                  >
                    <span>{{ showAllReviews ? 'Show Less' : `Show More (${reviews.length - 5})` }}</span>
                    <ChevronDown :class="{'transform rotate-180': showAllReviews}" class="w-4 h-4 transition-transform" />
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Cast Section -->
          <div class="mt-12">
            <h3 class="text-xl font-semibold mb-6 flex items-center">
              <span class="mr-2">Cast</span>
              <span class="text-sm text-gray-400 font-normal">Cast & Crew</span>
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div 
                v-for="(actor, index) in castWithImages.slice(0, 10)" 
                :key="index" 
                class="flex items-center gap-4 bg-gray-800/50 rounded-lg p-3 hover:bg-gray-800 transition-colors border-l-4 border-orange-500/70 cursor-pointer"
                @click="navigateToActor(actor.name)"
              >
                <div class="w-16 h-16 rounded-full overflow-hidden border-2 border-gray-700 flex-shrink-0 shadow-lg group">
                  <img :src="actor.imageUrl" :alt="actor.name" class="w-full h-full object-cover transition-transform duration-300" />
                </div>
                <div class="flex-1">
                  <h4 class="font-semibold text-lg">{{ actor.name }}</h4>
                  <p class="text-gray-400 text-sm">{{ actor.role }}</p>
                </div>
              </div>
            </div>
            <div class="mt-6 flex justify-center">
              <button 
                @click="viewAllCast" 
                class="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-lg transition-colors flex items-center gap-2"
              >
                <User class="w-5 h-5" />
                <span>View Complete Cast & Crew</span>
              </button>
            </div>
          </div>
          
          <!-- Series Like This Section -->
          <div class="mt-12">
            <h3 class="text-xl font-semibold mb-6 flex items-center justify-between">
              <span class="mr-2">More like this</span>
              <div class="flex items-center gap-2">
                <button 
                  @click="scrollLeft"
                  class="bg-black/50 rounded-full p-1 hover:bg-black/70 transition-colors"
                  aria-label="Previous series"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-left"><path d="m15 18-6-6 6-6"/></svg>
                </button>
                
                <button 
                  @click="scrollRight"
                  class="bg-black/50 rounded-full p-1 hover:bg-black/70 transition-colors"
                  aria-label="Next series"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-right"><path d="m9 18 6-6-6-6"/></svg>
                </button>
              </div>
            </h3>
            
            <div class="relative overflow-hidden">
              <div 
                ref="similarSeriesContainer"
                class="flex gap-4 overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800"
              >
                <div 
                  v-for="similarSeries in similarSeries" 
                  :key="similarSeries.id"
                  @click="navigateToSeries(similarSeries.id)"
                  class="flex-shrink-0 w-48 cursor-pointer group"
                >
                  <div class="relative rounded-lg overflow-hidden mb-2">
                    <img 
                      :src="similarSeries.posterUrl" 
                      :alt="similarSeries.title"
                      class="w-full h-64 object-cover group-hover:scale-105 transition-transform"
                    >
                    <div class="absolute inset-0 bg-black bg-opacity-20 group-hover:bg-opacity-10 transition-opacity"></div>
                    <button 
                      class="absolute top-2 right-2 p-2 bg-black bg-opacity-50 rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
                      @click.stop
                    >
                      <Play class="w-4 h-4 text-white" />
                    </button>
                    <div class="absolute bottom-2 left-2 bg-yellow-500 text-black text-xs font-bold rounded px-1.5 py-0.5 flex items-center">
                      <Star class="w-3 h-3 fill-current" />
                      <span class="ml-1">{{ similarSeries.userRating.toFixed(1) }}</span>
                    </div>
                  </div>
                  <h4 class="font-medium text-sm line-clamp-2 group-hover:text-orange-500 transition-colors">{{ similarSeries.title }}</h4>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Loading State -->
  <div v-else-if="seriesStore.isLoading" class="min-h-screen bg-gray-900 flex items-center justify-center">
    <div class="text-center">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto mb-4"></div>
      <p class="text-gray-400">Loading series details...</p>
    </div>
  </div>
  
  <!-- Error State -->
  <div v-else-if="seriesStore.error" class="min-h-screen bg-gray-900 flex items-center justify-center">
    <div class="text-center">
      <div class="text-red-500 text-xl mb-4">{{ seriesStore.error }}</div>
      <button @click="seriesStore.fetchSeries(seriesId)" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
        Try Again
      </button>
    </div>
  </div>
</template>

<style scoped>
/* Custom styles if needed */
.series-details-page {
  margin-top: -64px; /* Adjust based on header height */
}

/* Scrollbar styling for horizontal scrolling containers */
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: #d1d5db transparent;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background-color: #d1d5db;
  border-radius: 20px;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>