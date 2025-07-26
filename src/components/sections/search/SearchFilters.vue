<script setup lang="ts">
import { computed } from 'vue'
import { Filter, SlidersHorizontal, X, RotateCcw } from 'lucide-vue-next'
import { useSearchStore } from '@/stores/searchStore'
import { useUIStore } from '@/stores/uiStore'

const searchStore = useSearchStore()
const uiStore = useUIStore()

const isExpanded = computed({
  get: () => uiStore.showFilters,
  set: (value) => uiStore.showFilters = value
})

const toggleFilters = () => {
  uiStore.toggleFilters()
}

const updateFilter = (key: string, value: string) => {
  searchStore.updateFilter(key as any, value)
}

const clearAllFilters = () => {
  searchStore.clearFilters()
}
</script>

<template>
  <section class="py-6 bg-base-200">
    <div class="container mx-auto px-4">
      <!-- Filter Toggle Button -->
      <div class="flex justify-between items-center mb-4">
        <button 
          @click="toggleFilters"
          class="btn btn-outline btn-primary"
        >
          <SlidersHorizontal class="w-4 h-4 mr-2" />
          {{ isExpanded ? 'Hide Filters' : 'Show Filters' }}
          <span v-if="searchStore.hasActiveFilters" class="badge badge-secondary badge-sm ml-2">
            {{ Object.values(searchStore.filters).filter(v => v !== '').length }}
          </span>
        </button>
        
        <div class="flex items-center gap-2">
          <span class="text-sm text-gray-600">
            {{ searchStore.searchSummary.total }} results
            <span v-if="searchStore.searchSummary.hasQuery">
              for "{{ searchStore.searchState.query }}"
            </span>
          </span>
          
          <button 
            v-if="searchStore.hasActiveFilters"
            @click="clearAllFilters"
            class="btn btn-sm btn-outline btn-warning"
          >
            <X class="w-3 h-3 mr-1" />
            Clear
          </button>
        </div>
      </div>
      
      <!-- Filters Panel -->
      <div v-if="isExpanded" class="card bg-white shadow-lg">
        <div class="card-body">
          <div class="flex justify-between items-center mb-6">
            <h3 class="card-title text-lg">
              <Filter class="w-5 h-5 mr-2" />
              Filter Movies
            </h3>
            <button 
              @click="toggleFilters"
              class="btn btn-sm btn-ghost"
            >
              <X class="w-4 h-4" />
            </button>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
            <!-- Genre Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Genre</span>
              </label>
              <select 
                :value="searchStore.filters.genre"
                @change="updateFilter('genre', ($event.target as HTMLSelectElement).value)"
                class="select select-bordered select-sm"
              >
                <option value="">All Genres</option>
                <option 
                  v-for="genre in searchStore.filterOptions.genres" 
                  :key="genre" 
                  :value="genre"
                >
                  {{ genre }}
                </option>
              </select>
            </div>

            <!-- Year Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Release Year</span>
              </label>
              <select 
                :value="searchStore.filters.year"
                @change="updateFilter('year', ($event.target as HTMLSelectElement).value)"
                class="select select-bordered select-sm"
              >
                <option value="">All Years</option>
                <option 
                  v-for="year in searchStore.filterOptions.years" 
                  :key="year" 
                  :value="year"
                >
                  {{ year }}
                </option>
              </select>
            </div>

            <!-- Rating Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Rating</span>
              </label>
              <select 
                :value="searchStore.filters.rating"
                @change="updateFilter('rating', ($event.target as HTMLSelectElement).value)"
                class="select select-bordered select-sm"
              >
                <option 
                  v-for="rating in searchStore.filterOptions.ratings" 
                  :key="rating.value" 
                  :value="rating.value"
                >
                  {{ rating.label }}
                </option>
              </select>
            </div>

            <!-- Language Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Language</span>
              </label>
              <select 
                :value="searchStore.filters.language"
                @change="updateFilter('language', ($event.target as HTMLSelectElement).value)"
                class="select select-bordered select-sm"
              >
                <option value="">All Languages</option>
                <option 
                  v-for="language in searchStore.filterOptions.languages" 
                  :key="language" 
                  :value="language"
                >
                  {{ language }}
                </option>
              </select>
            </div>

            <!-- Production State Filter -->
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Production State</span>
              </label>
              <select 
                :value="searchStore.filters.productionState"
                @change="updateFilter('productionState', ($event.target as HTMLSelectElement).value)"
                class="select select-bordered select-sm"
              >
                <option value="">All States</option>
                <option 
                  v-for="state in searchStore.filterOptions.states" 
                  :key="state" 
                  :value="state"
                >
                  {{ state }}
                </option>
              </select>
            </div>
          </div>

          <!-- Sort Options -->
          <div class="divider"></div>
          
          <div class="flex flex-wrap gap-4">
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Sort By</span>
              </label>
              <select 
                :value="searchStore.sortBy"
                @change="searchStore.updateSort(($event.target as HTMLSelectElement).value)"
                class="select select-bordered select-sm"
              >
                <option value="title">Title (A-Z)</option>
                <option value="year">Release Year</option>
                <option value="rating">Rating</option>
                <option value="reviews">Most Reviewed</option>
              </select>
            </div>
            
            <div class="form-control">
              <label class="label">
                <span class="label-text font-semibold">Order</span>
              </label>
              <select 
                :value="searchStore.sortOrder"
                @change="searchStore.updateSort(searchStore.sortBy, ($event.target as HTMLSelectElement).value as 'asc' | 'desc')"
                class="select select-bordered select-sm"
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>

            <div class="form-control">
              <label class="label">
                <span class="label-text">&nbsp;</span>
              </label>
              <button 
                @click="clearAllFilters" 
                class="btn btn-outline btn-warning btn-sm"
                :disabled="!searchStore.hasActiveFilters"
              >
                <RotateCcw class="w-4 h-4 mr-2" />
                Clear Filters
              </button>
            </div>
          </div>
          
          <!-- Quick Filter Presets -->
          <div class="divider">Quick Filters</div>
          
          <div class="flex flex-wrap gap-2">
            <button 
              @click="searchStore.applyPreset('popularPies')"
              class="btn btn-sm btn-outline btn-success"
            >
              🥧 Popular Pies
            </button>
            <button 
              @click="searchStore.applyPreset('recentReleases')"
              class="btn btn-sm btn-outline btn-info"
            >
              🆕 Recent Releases
            </button>
            <button 
              @click="searchStore.applyPreset('comedies')"
              class="btn btn-sm btn-outline btn-warning"
            >
              😂 Comedies
            </button>
            <button 
              @click="searchStore.applyPreset('lagosMovies')"
              class="btn btn-sm btn-outline btn-primary"
            >
              🏙️ Lagos Movies
            </button>
          </div>
        </div>
      </div>
      
      <!-- Active Filters Display -->
      <div v-if="searchStore.hasActiveFilters && !isExpanded" class="flex flex-wrap gap-2 mt-4">
        <div class="text-sm font-medium text-gray-600 mr-2">Active filters:</div>
        
        <div 
          v-for="(value, key) in searchStore.filters" 
          :key="key"
          v-show="value"
          class="badge badge-primary gap-2"
        >
          {{ key }}: {{ value }}
          <button 
            @click="updateFilter(key, '')"
            class="btn btn-xs btn-ghost p-0 min-h-0 h-4 w-4"
          >
            <X class="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  </section>
</template>