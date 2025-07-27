<template>
  <div>
    <!-- Grid View -->
    <div v-if="viewMode === 'grid'" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-8">
      <!-- Loading Skeletons -->
      <div v-if="loading" v-for="i in 12" :key="`skeleton-${i}`" class="flex flex-col items-center">
        <div class="w-40 h-40 bg-gray-200 rounded-full animate-pulse mb-4"></div>
        <div class="h-5 bg-gray-200 rounded animate-pulse w-24 mb-2"></div>
        <div class="h-4 bg-gray-200 rounded animate-pulse w-10"></div>
      </div>
      
      <!-- Actor Cards -->
      <div 
        v-for="actor in actors" 
        :key="actor.id"
        class="flex flex-col items-center group cursor-pointer transition-transform hover:scale-105"
        @click="navigateToActor(actor.id)"
      >
        <div class="relative mb-4">
          <img 
            :src="actor.image" 
            :alt="actor.name"
            class="w-40 h-40 rounded-full object-cover border-2 border-gray-200 group-hover:border-orange-500 transition-colors"
            loading="lazy"
          />
          <div class="absolute inset-0 rounded-full bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all"></div>
        </div>
        <h3 class="text-base font-medium text-gray-900 text-center mb-2 group-hover:text-orange-600 transition-colors">{{ actor.name }}</h3>
        <p class="text-sm text-gray-500">{{ actor.age }}</p>
      </div>
    </div>
    
    <!-- List View -->
    <div v-else class="space-y-4">
      <!-- Loading Skeletons -->
      <div v-if="loading" v-for="i in 8" :key="`list-skeleton-${i}`" class="bg-white rounded-lg p-4 shadow-sm">
        <div class="flex items-center gap-4">
          <div class="w-16 h-16 bg-gray-200 rounded-full animate-pulse"></div>
          <div class="flex-1">
            <div class="h-5 bg-gray-200 rounded animate-pulse w-32 mb-2"></div>
            <div class="h-4 bg-gray-200 rounded animate-pulse w-20 mb-1"></div>
            <div class="h-3 bg-gray-200 rounded animate-pulse w-24"></div>
          </div>
          <div class="h-4 bg-gray-200 rounded animate-pulse w-16"></div>
        </div>
      </div>
      
      <!-- Actor List Items -->
      <div 
        v-for="actor in actors" 
        :key="actor.id"
        class="bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow cursor-pointer group"
        @click="navigateToActor(actor.id)"
      >
        <div class="flex items-center gap-4">
          <div class="relative">
            <img 
              :src="actor.image" 
              :alt="actor.name"
              class="w-16 h-16 rounded-full object-cover border-2 border-gray-200 group-hover:border-orange-500 transition-colors"
              loading="lazy"
            />
          </div>
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900 group-hover:text-orange-600 transition-colors mb-1">{{ actor.name }}</h3>
            <p class="text-sm text-gray-600 mb-1">Age: {{ actor.age }}</p>
            <p class="text-xs text-gray-500">{{ actor.movieCount }} movies</p>
          </div>
          <div class="text-right">
            <div class="text-sm font-medium text-gray-900">{{ formatPopularity(actor.popularity) }}</div>
            <div class="text-xs text-gray-500">popularity</div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Empty State -->
    <div v-if="!loading && actors.length === 0" class="text-center py-16">
      <div class="text-gray-400 mb-4">
        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">No actors found</h3>
      <p class="text-gray-500">Try adjusting your search criteria</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'
import { useRouter } from 'vue-router'
import type { Actor } from '@/stores/actorsStore'

interface Props {
  actors: Actor[]
  viewMode: 'grid' | 'list'
  loading: boolean
}

defineProps<Props>()

const router = useRouter()

const navigateToActor = (actorId: string) => {
  router.push({ name: 'person-details', params: { id: actorId } })
}

const formatPopularity = (popularity: number) => {
  if (popularity >= 1000000) {
    return `${(popularity / 1000000).toFixed(1)}M`
  } else if (popularity >= 1000) {
    return `${(popularity / 1000).toFixed(1)}K`
  }
  return popularity.toString()
}
</script>