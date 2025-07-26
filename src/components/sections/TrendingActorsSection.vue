<script setup lang="ts">
import { ref } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'

interface Actor {
  id: number
  name: string
  age: number
  profileImage: string
}

const scrollContainer = ref<HTMLElement>()

const actors: Actor[] = [
  {
    id: 1,
    name: 'Katherine LaNasa',
    age: 58,
    profileImage: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20elegant%20blonde%20actress%20with%20short%20hair%20wearing%20jewelry&image_size=square'
  },
  {
    id: 2,
    name: 'Gary Oldman',
    age: 67,
    profileImage: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20distinguished%20older%20man%20with%20glasses%20and%20beard&image_size=square'
  },
  {
    id: 3,
    name: 'Jenna Ortega',
    age: 22,
    profileImage: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20young%20latina%20actress%20with%20dark%20hair&image_size=square'
  },
  {
    id: 4,
    name: 'Jackie Chan',
    age: 71,
    profileImage: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20asian%20action%20star%20with%20friendly%20smile&image_size=square'
  },
  {
    id: 5,
    name: 'Sae Bom',
    age: 40,
    profileImage: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20korean%20actress%20with%20long%20dark%20hair&image_size=square'
  },
  {
    id: 6,
    name: 'Frank Welker',
    age: 79,
    profileImage: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20elderly%20voice%20actor%20with%20warm%20smile&image_size=square'
  }
]

const scrollLeft = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: -300, behavior: 'smooth' })
  }
}

const scrollRight = () => {
  if (scrollContainer.value) {
    scrollContainer.value.scrollBy({ left: 300, behavior: 'smooth' })
  }
}
</script>

<template>
  <section class="py-12 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Section Header -->
      <div class="flex items-center justify-between mb-8">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-3">
            <span class="w-1 h-6 bg-orange-500 rounded"></span>
            <h2 class="text-2xl font-bold text-gray-900">Trending Actors</h2>
          </div>
          <ChevronRight class="w-5 h-5 text-orange-500" />
        </div>
        
        <!-- Navigation Arrows -->
        <div class="flex gap-2">
          <button 
            @click="scrollLeft"
            class="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors duration-200"
          >
            <ChevronLeft class="w-5 h-5 text-gray-600" />
          </button>
          <button 
            @click="scrollRight"
            class="p-2 rounded-full bg-gray-100 hover:bg-gray-200 transition-colors duration-200"
          >
            <ChevronRight class="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>

      <!-- Actors Carousel -->
      <div 
        ref="scrollContainer"
        class="flex gap-6 overflow-x-auto scrollbar-hide pb-4"
        style="scroll-snap-type: x mandatory;"
      >
        <div 
          v-for="actor in actors" 
          :key="actor.id"
          class="flex-shrink-0 text-center cursor-pointer group"
          style="scroll-snap-align: start;"
        >
          <!-- Actor Profile Image -->
          <div class="relative mb-3">
            <div class="w-32 h-32 rounded-full overflow-hidden bg-gray-200 mx-auto group-hover:scale-105 transition-transform duration-300">
              <img 
                :src="actor.profileImage" 
                :alt="actor.name"
                class="w-full h-full object-cover"
                loading="lazy"
              />
            </div>
          </div>
          
          <!-- Actor Info -->
          <div class="space-y-1">
            <h3 class="font-semibold text-gray-900 text-sm group-hover:text-orange-500 transition-colors duration-200">
              {{ actor.name }}
            </h3>
            <p class="text-gray-500 text-sm">
              {{ actor.age }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>