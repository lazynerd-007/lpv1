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
          
          <!-- Visual Filter Cards -->
          <div class="space-y-6">
            <!-- Genre Filter -->
            <div>
              <h4 class="text-lg font-semibold mb-3 flex items-center gap-2">
                <img src="https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=colorful%20movie%20genre%20icons%20collection%20cinema%20film%20categories&image_size=square" alt="Genres" class="w-6 h-6 rounded" />
                Genres
              </h4>
              <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                <button 
                  v-for="genre in searchStore.filterOptions.genres" 
                  :key="genre"
                  @click="updateFilter('genre', searchStore.filters.genre === genre ? '' : genre)"
                  :class="[
                    'p-3 rounded-lg border-2 transition-all duration-200 text-center hover:scale-105',
                    searchStore.filters.genre === genre 
                      ? 'border-orange-500 bg-orange-50 text-orange-700' 
                      : 'border-gray-200 bg-white hover:border-orange-300'
                  ]"
                >
                  <div class="w-8 h-8 mx-auto mb-2 rounded-full bg-gradient-to-br from-orange-400 to-red-500 flex items-center justify-center text-white text-xs font-bold">
                    {{ genre.charAt(0) }}
                  </div>
                  <span class="text-xs font-medium">{{ genre }}</span>
                </button>
              </div>
            </div>

            <!-- Year Filter -->
            <div>
              <h4 class="text-lg font-semibold mb-3 flex items-center gap-2">
                <img src="https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=vintage%20calendar%20years%20timeline%20retro%20design&image_size=square" alt="Years" class="w-6 h-6 rounded" />
                Release Year
              </h4>
              <div class="grid grid-cols-3 md:grid-cols-6 lg:grid-cols-8 gap-2">
                <button 
                  v-for="year in searchStore.filterOptions.years" 
                  :key="year"
                  @click="updateFilter('year', searchStore.filters.year === year ? '' : year)"
                  :class="[
                    'p-2 rounded-lg border-2 transition-all duration-200 text-center hover:scale-105',
                    searchStore.filters.year === year 
                      ? 'border-orange-500 bg-orange-50 text-orange-700' 
                      : 'border-gray-200 bg-white hover:border-orange-300'
                  ]"
                >
                  <span class="text-sm font-bold">{{ year }}</span>
                </button>
              </div>
            </div>

            <!-- Rating Filter -->
            <div>
              <h4 class="text-lg font-semibold mb-3 flex items-center gap-2">
                <img src="https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=golden%20star%20rating%20system%20movie%20reviews&image_size=square" alt="Ratings" class="w-6 h-6 rounded" />
                Rating
              </h4>
              <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <button 
                  v-for="rating in searchStore.filterOptions.ratings" 
                  :key="rating.value"
                  @click="updateFilter('rating', searchStore.filters.rating === rating.value ? '' : rating.value)"
                  :class="[
                    'p-3 rounded-lg border-2 transition-all duration-200 text-center hover:scale-105',
                    searchStore.filters.rating === rating.value 
                      ? 'border-orange-500 bg-orange-50 text-orange-700' 
                      : 'border-gray-200 bg-white hover:border-orange-300'
                  ]"
                >
                  <div class="flex justify-center mb-2">
                    <div class="flex gap-1">
                      <span v-for="star in 5" :key="star" :class="[
                        'text-lg',
                        star <= parseFloat(rating.value) ? 'text-yellow-400' : 'text-gray-300'
                      ]">★</span>
                    </div>
                  </div>
                  <span class="text-xs font-medium">{{ rating.label }}</span>
                </button>
              </div>
            </div>

            <!-- Language Filter -->
            <div>
              <h4 class="text-lg font-semibold mb-3 flex items-center gap-2">
                <img src="https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=world%20languages%20flags%20international%20communication&image_size=square" alt="Languages" class="w-6 h-6 rounded" />
                Language
              </h4>
              <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                <button 
                  v-for="language in searchStore.filterOptions.languages" 
                  :key="language"
                  @click="updateFilter('language', searchStore.filters.language === language ? '' : language)"
                  :class="[
                    'p-3 rounded-lg border-2 transition-all duration-200 text-center hover:scale-105',
                    searchStore.filters.language === language 
                      ? 'border-orange-500 bg-orange-50 text-orange-700' 
                      : 'border-gray-200 bg-white hover:border-orange-300'
                  ]"
                >
                  <div class="w-8 h-8 mx-auto mb-2 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-white text-xs font-bold">
                    {{ language.substring(0, 2).toUpperCase() }}
                  </div>
                  <span class="text-xs font-medium">{{ language }}</span>
                </button>
              </div>
            </div>

            <!-- Production State Filter -->
            <div>
              <h4 class="text-lg font-semibold mb-3 flex items-center gap-2">
                <img src="https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nigeria%20map%20states%20regions%20nollywood%20film%20production&image_size=square" alt="States" class="w-6 h-6 rounded" />
                Production State
              </h4>
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                <button 
                  v-for="state in searchStore.filterOptions.states" 
                  :key="state"
                  @click="updateFilter('productionState', searchStore.filters.productionState === state ? '' : state)"
                  :class="[
                    'p-3 rounded-lg border-2 transition-all duration-200 text-center hover:scale-105',
                    searchStore.filters.productionState === state 
                      ? 'border-orange-500 bg-orange-50 text-orange-700' 
                      : 'border-gray-200 bg-white hover:border-orange-300'
                  ]"
                >
                  <div class="w-8 h-8 mx-auto mb-2 rounded-full bg-gradient-to-br from-green-400 to-teal-500 flex items-center justify-center text-white text-xs font-bold">
                    {{ state.substring(0, 2).toUpperCase() }}
                  </div>
                  <span class="text-xs font-medium">{{ state }}</span>
                </button>
              </div>
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