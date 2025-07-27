<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="container mx-auto px-2 py-4">
      <div class="flex items-center justify-between mb-6">
        <div class="flex items-center gap-3">
          <div class="w-1 h-8 bg-orange-500 rounded"></div>
          <h1 class="text-2xl font-bold text-gray-900">Trending Actors</h1>
        </div>
        
        <div class="flex items-center gap-4">
          <!-- Sort Dropdown -->
          <div class="flex items-center gap-2">
            <Filter class="w-4 h-4 text-gray-600" />
            <select 
              v-model="sortBy" 
              class="bg-white border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-500"
            >
              <option value="popularity">Most popular first</option>
              <option value="name">Name A-Z</option>
              <option value="age">Age</option>
              <option value="movies">Most movies</option>
            </select>
          </div>
          
          <!-- View Toggle -->
          <div class="flex items-center gap-2">
            <button 
              @click="viewMode = 'grid'"
              :class="[
                'p-2 rounded-lg transition-colors',
                viewMode === 'grid' ? 'bg-orange-500 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'
              ]"
            >
              <Grid class="w-4 h-4" />
            </button>
            <button 
              @click="viewMode = 'list'"
              :class="[
                'p-2 rounded-lg transition-colors',
                viewMode === 'list' ? 'bg-orange-500 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'
              ]"
            >
              <List class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
      
      <!-- Actors Grid -->
      <ActorsGrid 
        :actors="sortedActors" 
        :view-mode="viewMode"
        :loading="loading"
      />
      
      <!-- Loading Indicator -->
      <div v-if="loading" class="flex justify-center py-8">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-orange-500"></div>
      </div>
      
      <!-- End of Results -->
      <div v-if="hasReachedEnd && !loading" class="text-center py-8 text-gray-500">
        <p>You've reached the end of the list</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Filter, Grid, List } from 'lucide-vue-next'
import ActorsGrid from '@/components/sections/people/ActorsGrid.vue'
import { useActorsStore } from '@/stores/actorsStore'

const actorsStore = useActorsStore()
const sortBy = ref('popularity')
const viewMode = ref<'grid' | 'list'>('grid')
const loading = ref(false)
const hasReachedEnd = ref(false)

const sortedActors = computed(() => {
  const actors = [...actorsStore.actors]
  
  switch (sortBy.value) {
    case 'name':
      return actors.sort((a, b) => a.name.localeCompare(b.name))
    case 'age':
      return actors.sort((a, b) => a.age - b.age)
    case 'movies':
      return actors.sort((a, b) => b.movieCount - a.movieCount)
    case 'popularity':
    default:
      return actors.sort((a, b) => b.popularity - a.popularity)
  }
})

const loadMoreActors = async () => {
  if (loading.value || hasReachedEnd.value) return
  
  loading.value = true
  
  try {
    const hasMore = await actorsStore.loadMoreActors()
    if (!hasMore) {
      hasReachedEnd.value = true
    }
  } catch (error) {
    console.error('Error loading more actors:', error)
  } finally {
    loading.value = false
  }
}

const handleScroll = () => {
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop
  const windowHeight = window.innerHeight
  const documentHeight = document.documentElement.scrollHeight
  
  if (scrollTop + windowHeight >= documentHeight - 1000) {
    loadMoreActors()
  }
}

onMounted(() => {
  actorsStore.loadInitialActors()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>