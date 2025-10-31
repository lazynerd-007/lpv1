<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Star, Clock, Calendar, MapPin, Award, Play, Heart, Share2, MessageCircle, User, Plus, ChevronDown, Check, ChevronRight } from 'lucide-vue-next'
import { useMovieStore } from '@/stores/movieStore'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import { useAuthStore } from '@/stores/authStore'
import { useActorsStore, type Actor } from '@/stores/actorsStore'
import ReviewCard from '@/components/ui/ReviewCard.vue'
import ReviewForm from '@/components/ReviewForm.vue'

interface Props {
  id?: string
}

const props = defineProps<Props>()
const route = useRoute()
const router = useRouter()
const movieStore = useMovieStore()
const userStore = useUserStore()
const uiStore = useUIStore()
const authStore = useAuthStore()

const movieId = computed(() => props.id || route.params.id as string)
const movie = computed(() => movieStore.movies.find(m => m.id === movieId.value))
const reviews = computed(() => movieStore.reviews.filter(r => r.movieId === movieId.value))
const activeTab = ref('reviews')
const showAllCritics = ref(false)
const showAllReviews = ref(false)
const showReviewForm = ref(false)
const editingReview = ref<any>(null)
const reviewsToShow = computed(() => showAllReviews.value ? reviews.value : reviews.value.slice(0, 5))
const hasMoreReviews = computed(() => reviews.value.length > 5)
const criticsToShow = computed(() => {
  const criticsArray = critics.value || []
  return showAllCritics.value ? criticsArray : criticsArray.slice(0, 5)
})
const hasMoreCritics = computed(() => {
  const criticsArray = critics.value || []
  return criticsArray.length > 5
})

// Get similar movies based on genre matching
const similarMovies = computed(() => {
  if (!movie.value) return []
  
  return movieStore.movies
    .filter(m => 
      m.id !== movieId.value && // Not the current movie
      m.genre.some(g => movie.value?.genre.includes(g)) // Has at least one matching genre
    )
    .sort((a, b) => {
      // Count matching genres for better sorting
      const aMatches = a.genre.filter(g => movie.value?.genre.includes(g)).length
      const bMatches = b.genre.filter(g => movie.value?.genre.includes(g)).length
      return bMatches - aMatches
    })
    .slice(0, 10) // Limit to 10 similar movies
})

// Reference to the similar movies scroll container
const similarMoviesContainer = ref<HTMLElement | null>(null)

// Function to navigate to a movie details page
const navigateToMovie = (movieId: string) => {
  router.push({ name: 'movie-details', params: { id: movieId } })
}

// Functions to scroll the similar movies container left and right
const scrollLeft = () => {
  if (similarMoviesContainer.value) {
    similarMoviesContainer.value.scrollBy({ left: -300, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (similarMoviesContainer.value) {
    similarMoviesContainer.value.scrollBy({ left: 300, behavior: 'smooth' })
  }
}

// Sample critics data
const critics = computed(() => {
  // The Movie interface doesn't have a critics property, so we'll always use our sample data
  return [
    {
      source: 'The Guardian',
      date: '2 days ago',
      rating: 8,
      title: 'A Masterpiece of Nigerian Cinema',
      content: 'This film represents a significant leap forward for Nollywood, combining compelling storytelling with exceptional production values. The performances are nuanced and the direction is confident throughout.'
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
      content: 'The director demonstrates remarkable control over the material, balancing cultural specificity with universal themes. The result is a film that feels both authentic and accessible to international audiences.'
    },
    {
      source: 'The New York Times',
      date: '5 days ago',
      rating: 7,
      title: 'Promising But Uneven',
      content: 'There are moments of brilliance throughout, though the pacing issues in the second act prevent it from achieving greatness. Nevertheless, it represents an important voice in contemporary African cinema.'
    },
    {
      source: 'IndieWire',
      date: '1 week ago',
      rating: 9,
      title: 'A Revelation in Storytelling',
      content: 'Few films this year have managed to balance entertainment value with cultural significance so effectively. The director has crafted a work that feels both timely and timeless.'
    },
    {
      source: 'The Hollywood Reporter',
      date: '2 weeks ago',
      rating: 8,
      title: 'Visually Stunning Drama',
      content: 'The cinematography alone makes this worth watching, but the performances and screenplay elevate it to something truly special. A standout achievement for Nigerian cinema.'
    },
    {
      source: 'RogerEbert.com',
      date: '4 days ago',
      rating: 7.5,
      title: 'Thoughtful and Engaging',
      content: 'While not without flaws, this film offers a refreshing perspective and demonstrates the growing technical sophistication of Nollywood productions. The cultural specificity adds richness to the universal themes explored.'
    }
  ];
});

const averageRating = computed(() => {
  if (!reviews.value.length) return movie.value?.lemonPieRating || 0
  return reviews.value.reduce((sum, review) => sum + review.lemonPieRating, 0) / reviews.value.length
})

const ratingDistribution = computed(() => {
  const dist = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 }
  reviews.value.forEach(review => {
    const rating = Math.ceil(review.lemonPieRating)
    if (rating >= 1 && rating <= 5) {
      dist[rating as keyof typeof dist]++
    }
  })
  return dist
})

const isInWatchlist = computed(() => {
  return userStore.isInWatchlist(movieId.value)
})

// Cast data with images
const castWithImages = computed(() => {
  if (!movie.value?.cast) return []
  
  const actorStore = useActorsStore()
  
  // Map cast names to objects with images and roles
  return movie.value.cast.map((castMember, index) => {
    // Split the cast member name if it contains a role
    const parts = castMember.split(' as ')
    const actorName = parts[0].trim()
    const role = parts.length > 1 ? parts[1].trim() : movie.value?.title ? `Character in ${movie.value.title}` : 'Character'
    
    // Try to find the actor in the store first
    const actor = actorStore.actors.find(a => a.name === actorName)
    
    if (actor) {
      return {
        id: actor.id,
        name: actor.name,
        role,
        imageUrl: actor.image,
        popularity: actor.popularity,
        movieCount: actor.movieCount
      }
    } else {
      // Fallback to generated image if actor not found in store
      const imageUrl = `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(actorName + ' nigerian actor professional headshot')}&image_size=square`
      
      return {
        id: null,
        name: actorName,
        role,
        imageUrl,
        popularity: 0,
        movieCount: 0
      }
    }
  })
})

const isInFavorites = computed(() => {
  return userStore.isInFavorites(movieId.value)
})

const toggleWatchlist = async () => {
  if (!userStore.isAuthenticated) {
    uiStore.openModal({ id: 'auth', title: 'Authentication Required', content: 'Please log in to continue' })
    return
  }
  
  try {
    if (isInWatchlist.value) {
      await userStore.removeFromWatchlist(movieId.value)
    } else {
      await userStore.addToWatchlistWithActivity(movieId.value)
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
      await userStore.removeFromFavorites(movieId.value)
    } else {
      await userStore.addToFavoritesWithActivity(movieId.value)
    }
  } catch (error) {
    console.error('Error updating favorites:', error)
  }
}

const playTrailer = () => {
  if (movie.value) {
    uiStore.openTrailerModal(movie.value.id, movie.value.trailerUrl || '')
  }
}

const shareMovie = async () => {
  if (navigator.share && movie.value) {
    try {
      await navigator.share({
        title: movie.value.title,
        text: `Check out ${movie.value.title} on Nollywood Movies`,
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

// Review form handlers
const openReviewForm = () => {
  if (!authStore.isAuthenticated) {
    // Could redirect to login or show login modal
    console.log('User must be logged in to write a review')
    return
  }
  showReviewForm.value = true
  editingReview.value = null
}

const editReview = (review: any) => {
  if (!authStore.isAuthenticated || review.userId !== authStore.currentUserId) {
    return
  }
  editingReview.value = review
  showReviewForm.value = true
}

const handleReviewSubmit = async (reviewData: any) => {
  try {
    if (editingReview.value) {
      await userStore.updateUserReview(editingReview.value.id, reviewData)
    } else {
      await userStore.addUserReviewWithActivity(reviewData)
    }
    showReviewForm.value = false
    editingReview.value = null
  } catch (error) {
    console.error('Error submitting review:', error)
  }
}

const handleReviewCancel = () => {
  showReviewForm.value = false
  editingReview.value = null
}

const navigateToActor = (actorName: string) => {
  // Clean the actor name by removing any role information
  const cleanActorName = actorName.split(' as ')[0].trim()
  
  // Find actor by name in the actors store
  const actorStore = useActorsStore()
  const actor = actorStore.actors.find(a => a.name === cleanActorName)
  
  if (actor) {
    router.push({ name: 'person-details', params: { id: actor.id } })
  } else {
    // If actor not found, create a new actor entry with a unique ID
    const newActorId = `temp-${Date.now()}`
    const newActor: Actor = {
      id: newActorId,
      name: cleanActorName,
      age: 0, // Default values
      image: `https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(cleanActorName + ' nigerian actor professional headshot')}&image_size=square`,
      popularity: 0,
      movieCount: 1,
      biography: `Nigerian actor known for their work in Nollywood films.`,
      birthPlace: 'Nigeria',
      knownFor: [movie.value?.title || 'Various Films']
    }
    
    // Add the new actor to the store
    actorStore.addActor(newActor)
    
    // Navigate to the new actor's details page
    router.push({ name: 'person-details', params: { id: newActorId } })
  }
}

const viewAllCast = () => {
  if (movie.value) {
    // Navigate to the dedicated cast and crew page for this movie
    router.push({ name: 'movie-cast-crew', params: { id: movieId.value } })
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
        router.push(`/edit-review/${reviewId}`)
        break
      case 'delete':
        await movieStore.deleteReview(reviewId)
        break
    }
  } catch (error) {
    console.error('Error handling review action:', error)
  }
}

onMounted(async () => {
  // Load movies first if not already loaded
  if (!movieStore.hasLoadedMovies) {
    await movieStore.loadMovies()
  }
  
  // Try to fetch the specific movie
  await movieStore.fetchMovie(movieId.value)
  
  // Set current movie for detailed view
  if (movie.value) {
    // Set current movie in store for reviews
    movieStore.currentMovie = movie.value
    uiStore.setPageTitle(`${movie.value.title} - Nollywood Movies`)
  } else {
    uiStore.setPageTitle('Movie Not Found - Nollywood Movies')
  }
})
</script>

<template>
  <div v-if="movie" class="min-h-screen bg-theme-background text-theme-text">
    <!-- Hero Video Section -->
    <div class="relative w-full h-[500px] mb-8">
      <div class="relative group cursor-pointer bg-gray-800 w-full h-full overflow-hidden">
        <img 
          :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(movie.title + ' movie cinematic scene')}&image_size=landscape_16_9`" 
          :alt="`${movie.title} trailer`" 
          class="w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center group-hover:bg-opacity-60 transition-all duration-300">
          <div class="bg-orange-500 hover:bg-orange-600 rounded-full p-6 transform group-hover:scale-110 transition-transform duration-300">
            <Play class="w-12 h-12 text-white" />
          </div>
        </div>
        <div class="absolute bottom-6 left-6 bg-black bg-opacity-75 text-white px-4 py-3 rounded">
          <h4 class="text-xl font-semibold">{{ movie.title }} - Official Trailer</h4>
          <p class="text-sm text-gray-300">2:34</p>
        </div>
        <!-- Movie Info Overlay -->
        <div class="absolute top-6 right-6 bg-black bg-opacity-75 text-white px-4 py-3 rounded">
          <div class="flex items-center gap-2 mb-2">
            <Star class="w-5 h-5 text-yellow-400 fill-current" />
            <span class="text-lg font-bold">{{ averageRating.toFixed(1) }}</span>
            <span class="text-gray-300">/ 10</span>
          </div>
          <p class="text-sm text-gray-300">{{ movie.releaseDate }} • PG • 1hr 37min</p>
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Left Column - Movie Poster -->
        <div class="lg:col-span-1">
          <div class="sticky top-8">
            <!-- Movie Poster (Prominently Displayed) -->
          <div class="relative overflow-hidden rounded-lg shadow-2xl border-2 border-orange-500/20 hover:border-orange-500/40 transition-colors duration-300">
            <img
              :src="movie.poster"
              :alt="movie.title"
              class="w-full object-cover rounded-lg transform hover:scale-105 transition-transform duration-300"
            />
            <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black to-transparent h-24"></div>
            <div class="absolute top-0 right-0 m-3 bg-orange-500 text-white text-xs font-bold px-2 py-1 rounded shadow-lg">
              {{ movie.lemonPieRating.toFixed(1) }}/10
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
                @click="shareMovie"
                class="w-full bg-transparent text-white border border-gray-600 hover:bg-gray-800 px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 transition-colors"
              >
                <Share2 class="w-5 h-5" />
                Share
              </button>
            </div>
            
            <!-- Movie Info Sidebar -->
            <div class="mt-8 space-y-4 text-sm">
              <div>
                <span class="text-gray-400">Original language</span>
                <p class="text-white">{{ movie.language }}</p>
              </div>
              <div>
                <span class="text-gray-400">Budget</span>
                <p class="text-white">$200,000,000.00</p>
              </div>
              <div>
                <span class="text-gray-400">Revenue</span>
                <p class="text-white">$318,000,000.00</p>
              </div>
              <div>
                <span class="text-gray-400">Production countries</span>
                <p class="text-white">{{ movie.productionState }}</p>
              </div>
              <div>
                <span class="text-gray-400">Keywords</span>
                <div class="flex flex-wrap gap-1 mt-1">
                  <span v-for="genre in movie.genre" :key="genre" class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs">{{ genre }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column - Movie Details -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Movie Title and Basic Info -->
          <div>
            <h1 class="text-4xl md:text-5xl font-bold mb-4">{{ movie.title }}</h1>
            <div class="flex items-center gap-4 mb-4 text-sm">
              <span class="text-gray-400">{{ movie.releaseDate }}</span>
              <span class="text-gray-400">•</span>
              <span class="text-gray-400">PG • 1hr 37min</span>
              <div class="flex items-center gap-1">
                <span v-for="genre in movie.genre.slice(0, 3)" :key="genre" class="bg-gray-700 text-gray-300 px-2 py-1 rounded text-xs">{{ genre }}</span>
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
            <p class="text-gray-300 leading-relaxed mb-6">{{ movie.plotSummary }}</p>
            
            <!-- Director and Writers -->
            <div class="space-y-2 text-sm mb-8">
              <div class="flex">
                <span class="text-gray-400 w-20">Director</span>
                <span class="text-blue-400 hover:text-blue-300 cursor-pointer">{{ movie.director }}</span>
              </div>
              <div class="flex">
                <span class="text-gray-400 w-20">Writers</span>
                <span class="text-blue-400 hover:text-blue-300 cursor-pointer">{{ movie.director }}</span>
              </div>
              <div class="flex">
                <span class="text-gray-400 w-20">Stars</span>
                <div class="flex flex-wrap gap-1">
                  <span v-for="(actor, index) in movie.cast.slice(0, 3)" :key="actor" class="text-blue-400 hover:text-blue-300 cursor-pointer">
                    {{ actor }}<span v-if="index < movie.cast.slice(0, 3).length - 1">, </span>
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Hero Image Gallery -->
            <div class="mb-8">
              <h3 class="text-xl font-semibold mb-4">Movie Stills</h3>
              <div class="relative">
                <div class="flex overflow-x-auto pb-4 space-x-4 scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800">
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg flex-shrink-0">
                    <img 
                      :src="movie.poster" 
                      :alt="`${movie.title} still 1`" 
                      class="h-32 w-auto min-w-[180px] object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                  </div>
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg flex-shrink-0">
                    <img 
                      :src="movie.posterUrl" 
                      :alt="`${movie.title} still 2`" 
                      class="h-32 w-auto min-w-[180px] object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                  </div>
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg flex-shrink-0">
                    <img 
                      :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(movie.title + ' movie scene')}&image_size=landscape_16_9`" 
                      :alt="`${movie.title} still 3`" 
                      class="h-32 w-auto min-w-[180px] object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                    <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-opacity duration-300"></div>
                  </div>
                  <div class="relative group cursor-pointer overflow-hidden rounded-lg flex-shrink-0">
                    <img 
                      :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(movie.title + ' movie character')}&image_size=portrait_4_3`" 
                      :alt="`${movie.title} still 4`" 
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
                    :src="`https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=${encodeURIComponent(movie.title + (i % 2 === 0 ? ' movie scene ' : ' character ') + i)}&image_size=${i % 2 === 0 ? 'landscape_16_9' : 'portrait_4_3'}`" 
                    :alt="`${movie.title} Gallery Image ${i}`" 
                    class="h-40 w-auto min-w-[200px] object-cover rounded-lg cursor-pointer hover:opacity-80 transition-opacity flex-shrink-0" 
                  />
                </div>
              </div>
            </div>
          </div>
          
          <!-- Content Tabs -->
          <div>
            <div class="flex border-b border-theme-border mb-6">
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
              <div v-for="(critic, index) in criticsToShow" :key="index" class="bg-theme-surface rounded-lg p-6">
                <div class="flex items-start gap-4">
                  <div class="w-10 h-10 bg-theme-background rounded-full flex items-center justify-center">
                    <User class="w-6 h-6 text-theme-secondary" />
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="font-semibold">{{ critic.source }}</span>
                      <span class="text-theme-secondary text-sm">{{ critic.date }}</span>
                    </div>
                    <div class="flex items-center gap-1 mb-3">
                      <Star v-for="i in Math.round(critic.rating / 2)" :key="i" class="w-4 h-4 text-yellow-400 fill-current" />
                      <Star v-for="i in (5 - Math.round(critic.rating / 2))" :key="i + Math.round(critic.rating / 2)" class="w-4 h-4 text-theme-tertiary" />
                      <span class="text-sm text-theme-secondary ml-2">{{ critic.rating }} / 10</span>
                    </div>
                    <h4 class="font-semibold mb-2">{{ critic.title }}</h4>
                    <p class="text-theme-secondary leading-relaxed">{{ critic.content }}</p>
                  </div>
                </div>
              </div>
              
              <div v-if="hasMoreCritics" class="flex justify-center mt-6">
                <button 
                  @click="showAllCritics = !showAllCritics" 
                  class="flex items-center gap-2 px-6 py-2 bg-theme-surface hover:bg-theme-surface/80 rounded-full text-theme-secondary hover:text-theme-primary transition-colors"
                >
                  <span>{{ showAllCritics ? 'Show Less' : `Show More (${(critics?.length || 0) - 5})` }}</span>
                  <ChevronDown :class="{'transform rotate-180': showAllCritics}" class="w-4 h-4 transition-transform" />
                </button>
              </div>
            </div>
            
            <!-- Reviews Tab -->
            <div v-if="activeTab === 'reviews'" class="space-y-6">
              <div class="flex justify-between items-center">
                <div class="flex items-center gap-4">
                  <div class="flex items-center gap-2">
                    <Star class="w-5 h-5 text-yellow-400 fill-current" />
                    <span class="text-xl font-bold">{{ averageRating.toFixed(1) }}</span>
                    <span class="text-theme-secondary">/ 10</span>
                  </div>
                  <span class="text-theme-secondary">{{ reviews.length }} Reviews</span>
                </div>
                <button 
                  @click="openReviewForm"
                  class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2 transition-colors text-sm"
                >
                  <Plus class="w-4 h-4" />
                  Add Review
                </button>
              </div>
              
              <!-- Review Form -->
              <ReviewForm 
                v-if="showReviewForm"
                :movie-id="movieId"
                :movie-title="movie?.title"
                :edit-review="editingReview"
                @submit="handleReviewSubmit"
                @cancel="handleReviewCancel"
                class="mb-6"
              />
              
              <!-- Account Required Message -->
              <div class="bg-theme-surface border border-theme-border rounded-lg p-6 text-center">
                <h3 class="text-lg font-semibold mb-2">Account required</h3>
                <p class="text-theme-secondary mb-4">Please sign in or create account to add a review</p>
              </div>
              
              <!-- Sample Review -->
              <div class="bg-theme-surface rounded-lg p-6">
                <div class="flex items-start gap-4">
                  <div class="w-10 h-10 bg-theme-background rounded-full flex items-center justify-center">
                    <User class="w-6 h-6 text-theme-secondary" />
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center gap-2 mb-2">
                      <span class="font-semibold">Logan Roberts</span>
                      <span class="text-theme-secondary text-sm">4 days ago</span>
                    </div>
                    <div class="flex items-center gap-1 mb-3">
                      <Star v-for="i in 5" :key="i" class="w-4 h-4 text-yellow-400 fill-current" />
                      <span class="text-sm text-theme-secondary ml-2">9 / 10</span>
                    </div>
                    <h4 class="font-semibold mb-2">Action-Packed and Exciting</h4>
                    <p class="text-theme-secondary leading-relaxed">This movie is a thrilling adventure from start to finish. The action sequences are mind-blowing, and the excitement never lets up. The characters are well-developed and the story is engaging throughout.</p>
                    <div class="flex items-center gap-4 mt-4 text-sm">
                      <span class="text-theme-secondary">Was this review helpful?</span>
                      <button class="text-blue-400 hover:text-blue-300">YES</button>
                      <button class="text-blue-400 hover:text-blue-300">NO</button>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="reviews.length === 0" class="text-center py-8 text-theme-secondary">
                <MessageCircle class="w-12 h-12 mx-auto mb-4 text-theme-tertiary" />
                <p>No reviews yet. Be the first to review this movie!</p>
              </div>
              
              <div v-else class="space-y-4">
                <ReviewCard 
                  v-for="review in reviewsToShow" 
                  :key="review.id" 
                  :review="review"
                  :show-movie-title="false"
                  @action="handleReviewAction"
                  @edit="editReview"
                />
                
                <div v-if="hasMoreReviews" class="flex justify-center mt-6">
                  <button 
                    @click="showAllReviews = !showAllReviews" 
                    class="flex items-center gap-2 px-6 py-2 bg-theme-surface hover:bg-theme-surface/80 rounded-full text-theme-secondary hover:text-theme-primary transition-colors"
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
              <span class="text-sm text-theme-secondary font-normal">{{ movie?.cast?.length || 0 }} actors</span>
            </h3>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div 
                v-for="(actor, index) in castWithImages.slice(0, 10)" 
                :key="index" 
                class="group flex items-center gap-4 bg-theme-surface/50 hover:bg-theme-surface rounded-lg p-4 transition-all duration-300 border-l-4 border-orange-500/70 hover:border-orange-500 cursor-pointer hover:shadow-lg hover:scale-[1.02] transform"
                @click="navigateToActor(actor.name)"
              >
                <div class="relative w-16 h-16 rounded-full overflow-hidden border-2 border-theme-border group-hover:border-orange-400 flex-shrink-0 shadow-lg transition-all duration-300">
                  <img 
                    :src="actor.imageUrl" 
                    :alt="actor.name" 
                    class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110" 
                  />
                  <!-- Hover overlay -->
                  <div class="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                    <ChevronRight class="w-5 h-5 text-white" />
                  </div>
                </div>
                <div class="flex-1 min-w-0">
                  <h4 class="font-semibold text-lg group-hover:text-orange-400 transition-colors duration-300 truncate">{{ actor.name }}</h4>
                  <p class="text-theme-secondary text-sm group-hover:text-theme-text transition-colors duration-300 truncate">{{ actor.role }}</p>
                  <!-- Show popularity if available -->
                  <div v-if="actor.popularity > 0" class="flex items-center gap-1 mt-1">
                    <Star class="w-3 h-3 text-yellow-400 fill-current" />
                    <span class="text-xs text-theme-tertiary">{{ (actor.popularity / 1000000).toFixed(1) }}M followers</span>
                  </div>
                </div>
                <!-- Click indicator -->
                <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <div class="bg-orange-500 rounded-full p-1">
                    <ChevronRight class="w-4 h-4 text-white" />
                  </div>
                </div>
              </div>
            </div>
            <div class="mt-6 flex justify-center">
              <button 
                @click="viewAllCast" 
                class="px-6 py-3 bg-orange-600 hover:bg-orange-700 text-white font-medium rounded-lg transition-colors flex items-center gap-2 hover:shadow-lg transform hover:scale-105 duration-300"
              >
                <User class="w-5 h-5" />
                <span>View Complete Cast & Crew</span>
              </button>
            </div>
          </div>
          
          <!-- Movies Like This Section -->
          <div class="mt-12">
            <h3 class="text-xl font-semibold mb-6 flex items-center justify-between">
              <span class="mr-2">More like this</span>
              <div class="flex items-center gap-2">
                <button 
                  @click="scrollLeft"
                  class="bg-black/50 rounded-full p-1 hover:bg-black/70 transition-colors"
                  aria-label="Previous movies"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-left"><path d="m15 18-6-6 6-6"/></svg>
                </button>
                
                <button 
                  @click="scrollRight"
                  class="bg-black/50 rounded-full p-1 hover:bg-black/70 transition-colors"
                  aria-label="Next movies"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chevron-right"><path d="m9 18 6-6-6-6"/></svg>
                </button>
              </div>
            </h3>
            
            <div class="relative">
              <!-- Movie Cards Horizontal Scroll -->
              <div ref="similarMoviesContainer" class="flex overflow-x-auto pb-4 gap-4 hide-scrollbar">
                <div 
                  v-for="(movie, index) in similarMovies" 
                  :key="movie.id"
                  class="flex-shrink-0 w-56 relative group cursor-pointer"
                  @click="navigateToMovie(movie.id)"
                >
                  <div class="relative overflow-hidden rounded-lg">
                    <!-- Movie Poster -->
                    <img 
                      :src="movie.posterUrl" 
                      :alt="movie.title" 
                      class="w-full h-80 object-cover rounded-lg transition-transform duration-300 group-hover:scale-105"
                    />
                    
                    <!-- Play Button Overlay -->
                    <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <button class="bg-orange-600 hover:bg-orange-700 text-white rounded-full p-3 transition-colors">
                        <Play class="w-6 h-6" />
                      </button>
                    </div>
                  </div>
                  
                  <!-- Rating -->
                  <div class="flex items-center mt-2 text-orange-500">
                    <Star class="w-4 h-4 fill-current" />
                    <span class="ml-1 text-sm font-medium">{{ movie.lemonPieRating.toFixed(1) }} / 10</span>
                  </div>
                  
                  <!-- Title -->
                  <h4 class="font-medium text-white mt-1 line-clamp-2">{{ movie.title }}</h4>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- Movie Not Found -->
  <div v-else class="min-h-screen flex items-center justify-center bg-theme-background text-theme-text">
    <div class="text-center">
      <h1 class="text-4xl font-bold mb-4">Movie Not Found</h1>
      <p class="text-theme-secondary mb-8">The movie you're looking for doesn't exist or has been removed.</p>
      <router-link 
        to="/" 
        class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold transition-colors"
      >
        Go Home
      </router-link>
    </div>
  </div>
</template>

<style scoped>
/* Custom scrollbar styles */
.scrollbar-thin::-webkit-scrollbar {
  height: 6px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: #1f2937; /* gray-800 */
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #4b5563; /* gray-600 */
  border-radius: 3px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #6b7280; /* gray-500 */
}

/* Hide scrollbar for Firefox */
.scrollbar-thin {
  scrollbar-width: thin;
  scrollbar-color: #4b5563 #1f2937;
}
</style>