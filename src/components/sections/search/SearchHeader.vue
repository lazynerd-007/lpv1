<script setup lang="ts">
import { ref, watch } from 'vue'
import { Search } from 'lucide-vue-next'
import { useSearchStore } from '@/stores/searchStore'

interface Props {
  title?: string
  subtitle?: string
  placeholder?: string
  initialQuery?: string
}

const props = withDefaults(defineProps<Props>(), {
  title: '🔍 Search Nollywood Movies',
  subtitle: 'Discover your next favorite Nigerian film',
  placeholder: 'Search movies, actors, directors...'
})

const searchStore = useSearchStore()
const localQuery = ref(props.initialQuery || '')

// Watch for changes in the search query
watch(localQuery, (newQuery) => {
  if (newQuery !== searchStore.searchState.query) {
    performSearch()
  }
})

const performSearch = () => {
  searchStore.performSearch(localQuery.value)
}

const handleKeyup = (event: KeyboardEvent) => {
  if (event.key === 'Enter') {
    performSearch()
  }
}

// Initialize with any existing query
if (searchStore.searchState.query) {
  localQuery.value = searchStore.searchState.query
}
</script>

<template>
  <section class="bg-gradient-to-r from-nollywood-gold to-vibrant-orange py-12">
    <div class="container mx-auto px-4">
      <div class="max-w-4xl mx-auto text-center">
        <h1 class="text-4xl font-bold text-white mb-4">
          {{ title }}
        </h1>
        <p class="text-xl text-cream-white/90 mb-8">
          {{ subtitle }}
        </p>
        
        <!-- Search Bar -->
        <div class="form-control w-full">
          <div class="input-group justify-center">
            <input 
              v-model="localQuery"
              type="text" 
              :placeholder="placeholder"
              class="input input-bordered input-lg w-full max-w-2xl"
              @keyup="handleKeyup"
            />
            <button 
              class="btn btn-primary btn-lg"
              @click="performSearch"
              :disabled="searchStore.searchState.isLoading"
            >
              <Search class="w-5 h-5" />
              <span v-if="searchStore.searchState.isLoading" class="loading loading-spinner loading-sm"></span>
              <span v-else>Search</span>
            </button>
          </div>
        </div>
        
        <!-- Quick Search Suggestions -->
        <div class="flex flex-wrap justify-center gap-2 mt-6">
          <button 
            @click="() => { localQuery = 'comedy'; performSearch(); }"
            class="btn btn-sm btn-outline btn-primary"
          >
            Comedy Movies
          </button>
          <button 
            @click="() => { localQuery = '2024'; performSearch(); }"
            class="btn btn-sm btn-outline btn-primary"
          >
            Latest 2024
          </button>
          <button 
            @click="() => { localQuery = 'Lagos'; performSearch(); }"
            class="btn btn-sm btn-outline btn-primary"
          >
            Lagos Productions
          </button>
          <button 
            @click="() => { localQuery = 'Funke Akindele'; performSearch(); }"
            class="btn btn-sm btn-outline btn-primary"
          >
            Funke Akindele
          </button>
        </div>
      </div>
    </div>
  </section>
</template>