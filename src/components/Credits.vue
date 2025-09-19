<template>
  <div class="mb-8">
    <h2 class="text-xl font-bold text-white mb-6">Credits</h2>
    
    <!-- Acting Credits Section -->
    <div class="mb-4">
      <div 
        @click="toggleSection('acting')"
        class="bg-gray-800 rounded-t-lg p-4 flex justify-between items-center cursor-pointer hover:bg-gray-750 transition-colors border-l-4 border-orange-500"
      >
        <div class="flex items-center">
          <div class="w-8 h-8 flex items-center justify-center rounded-full bg-gray-700 mr-3 shadow-inner">
            <Film class="w-4 h-4 text-orange-500" />
          </div>
          <h3 class="text-white font-semibold">Acting</h3>
          <div class="ml-2 px-2 py-0.5 bg-gray-700 rounded-full text-xs text-gray-300 font-medium">
            {{ actingCredits.length }}
          </div>
        </div>
        <ChevronDown 
          :class="[isActingOpen ? 'transform rotate-180' : '', 'w-5 h-5 text-gray-400 transition-transform']" 
        />
      </div>
      
      <div 
        v-if="isActingOpen"
        class="bg-gray-800 rounded-b-lg overflow-hidden shadow-lg mb-4 divide-y divide-gray-700"
      >
        <div 
          v-for="(credit, index) in actingCredits" 
          :key="`acting-${index}`"
          class="p-4 hover:bg-gray-700 transition-colors cursor-pointer flex justify-between items-center"
        >
          <div class="flex items-center">
            <div class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-700 mr-4">
              <Film class="w-5 h-5 text-orange-500" />
            </div>
            <div>
              <h3 class="text-white font-medium">{{ credit.title }}</h3>
              <p class="text-gray-400 text-sm">{{ credit.role }}</p>
            </div>
          </div>
          <div class="text-gray-400 text-sm font-medium">
            {{ credit.year }}
          </div>
        </div>
      </div>
    </div>
    
    <!-- Production Credits Section -->
    <div>
      <div 
        @click="toggleSection('production')"
        class="bg-gray-800 rounded-t-lg p-4 flex justify-between items-center cursor-pointer hover:bg-gray-750 transition-colors border-l-4 border-blue-500"
      >
        <div class="flex items-center">
          <div class="w-8 h-8 flex items-center justify-center rounded-full bg-gray-700 mr-3 shadow-inner">
            <Video class="w-4 h-4 text-blue-500" />
          </div>
          <h3 class="text-white font-semibold">Production</h3>
          <div class="ml-2 px-2 py-0.5 bg-gray-700 rounded-full text-xs text-gray-300 font-medium">
            {{ productionCredits.length }}
          </div>
        </div>
        <ChevronDown 
          :class="[isProductionOpen ? 'transform rotate-180' : '', 'w-5 h-5 text-gray-400 transition-transform']" 
        />
      </div>
      
      <div 
        v-if="isProductionOpen"
        class="bg-gray-800 rounded-b-lg overflow-hidden shadow-lg divide-y divide-gray-700"
      >
        <div 
          v-for="(credit, index) in productionCredits" 
          :key="`production-${index}`"
          class="p-4 hover:bg-gray-700 transition-colors cursor-pointer flex justify-between items-center"
        >
          <div class="flex items-center">
            <div class="w-10 h-10 flex items-center justify-center rounded-full bg-gray-700 mr-4">
              <Video class="w-5 h-5 text-blue-500" />
            </div>
            <div>
              <h3 class="text-white font-medium">{{ credit.title }}</h3>
              <p class="text-gray-400 text-sm">{{ credit.role }}</p>
            </div>
          </div>
          <div class="text-gray-400 text-sm font-medium">
            {{ credit.year }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Film, Video, ChevronDown } from 'lucide-vue-next';
import { ref, computed } from 'vue';

interface Credit {
  title: string;
  role: string;
  year: number;
  type?: 'acting' | 'production';
}

const props = defineProps<{
  credits: Credit[];
}>();

// State for dropdown sections
const isActingOpen = ref(true);
const isProductionOpen = ref(true);

// Toggle section visibility
const toggleSection = (section: 'acting' | 'production') => {
  if (section === 'acting') {
    isActingOpen.value = !isActingOpen.value;
  } else {
    isProductionOpen.value = !isProductionOpen.value;
  }
};

// Filter credits by type
const actingCredits = computed(() => {
  return props.credits.filter(credit => 
    !credit.type || credit.type === 'acting' || 
    ['Actor', 'Lead Actor', 'Supporting Role', 'Supporting Actor', 'Guest Star', 'Voice Actor', 'Cameo'].includes(credit.role)
  );
});

const productionCredits = computed(() => {
  return props.credits.filter(credit => 
    credit.type === 'production' || 
    ['Director', 'Producer', 'Executive Producer', 'Writer', 'Creator', 'Showrunner'].includes(credit.role)
  );
});
</script>

<style scoped>
.hover\:bg-gray-750:hover {
  background-color: rgba(55, 65, 81, 0.9);
}

/* Smooth transitions for dropdowns */
.bg-gray-800 {
  transition: all 0.2s ease-in-out;
}

/* Animation for chevron rotation */
.transform {
  transition: transform 0.3s ease;
}

/* Dropdown animation */
[v-if] {
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>