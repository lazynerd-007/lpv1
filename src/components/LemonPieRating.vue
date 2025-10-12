<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, Teleport } from 'vue';

interface Props {
  rating: number;
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
  interactive?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  showText: true,
  interactive: false
});

const emit = defineEmits<{
  ratingChange: [rating: number];
}>();

// State for hover functionality
const isHovering = ref(false);
const tooltipPosition = ref({ x: 0, y: 0 });
const tooltipRef = ref<HTMLElement | null>(null);

const isLemon = computed(() => props.rating >= 1 && props.rating <= 4);
const isPie = computed(() => props.rating >= 7 && props.rating <= 10);
const isNeutral = computed(() => props.rating >= 5 && props.rating <= 6);

const ratingText = computed(() => {
  if (isLemon.value) return 'Lemon';
  if (isPie.value) return 'Pie';
  return 'Neutral';
});

const ratingColor = computed(() => {
  if (isLemon.value) return 'text-lemon-yellow';
  if (isPie.value) return 'text-pie-brown';
  return 'text-gray-500';
});

const ratingBgColor = computed(() => {
  if (isLemon.value) return 'bg-lemon-yellow/20';
  if (isPie.value) return 'bg-pie-brown/20';
  return 'bg-gray-200';
});

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'w-8 h-8 text-sm';
    case 'lg':
      return 'w-16 h-16 text-2xl';
    default:
      return 'w-12 h-12 text-lg';
  }
});

// Generate pie and lemon icons for visualization
const pieIcons = computed(() => {
  const rating = Math.min(Math.max(Math.round(props.rating), 0), 10);
  return Array(rating).fill('🥧');
});

const lemonIcons = computed(() => {
  const rating = Math.min(Math.max(Math.round(props.rating), 0), 10);
  const lemonCount = 10 - rating;
  return Array(lemonCount).fill('🍋');
});

// Generate pie slices for SVG visualization
const pieSlices = computed(() => {
  const rating = Math.min(Math.max(Math.round(props.rating), 0), 10);
  const slices = [];
  
  // Create pie slices (each representing 1 point)
  for (let i = 0; i < rating; i++) {
    const startAngle = (i / 10) * 360;
    const endAngle = ((i + 1) / 10) * 360;
    slices.push({
      path: createSlicePath(50, 50, 45, startAngle, endAngle),
      color: '#8B4513' // Pie brown color
    });
  }
  
  return slices;
});

// Generate lemon slices for SVG visualization
const lemonSlices = computed(() => {
  const rating = Math.min(Math.max(Math.round(props.rating), 0), 10);
  const lemonCount = 10 - rating;
  const slices = [];
  
  // Create lemon slices (each representing 1 point)
  for (let i = 0; i < lemonCount; i++) {
    const startAngle = ((rating + i) / 10) * 360;
    const endAngle = ((rating + i + 1) / 10) * 360;
    slices.push({
      path: createSlicePath(50, 50, 45, startAngle, endAngle),
      color: '#FFD700' // Lemon yellow color
    });
  }
  
  return slices;
});

// Helper function to create SVG path for a pie slice
const createSlicePath = (cx: number, cy: number, radius: number, startAngle: number, endAngle: number) => {
  const startAngleRad = (startAngle * Math.PI) / 180;
  const endAngleRad = (endAngle * Math.PI) / 180;
  
  const x1 = cx + radius * Math.cos(startAngleRad);
  const y1 = cy + radius * Math.sin(startAngleRad);
  
  const x2 = cx + radius * Math.cos(endAngleRad);
  const y2 = cy + radius * Math.sin(endAngleRad);
  
  const largeArcFlag = endAngle - startAngle > 180 ? 1 : 0;
  
  return `M ${cx} ${cy} L ${x1} ${y1} A ${radius} ${radius} 0 ${largeArcFlag} 1 ${x2} ${y2} Z`;
};

const handleRatingClick = (newRating: number) => {
  if (props.interactive) {
    emit('ratingChange', newRating);
  }
};

// Hover functionality
const handleMouseEnter = (event: MouseEvent) => {
  isHovering.value = true;
  updateTooltipPosition(event);
};

const handleMouseMove = (event: MouseEvent) => {
  if (isHovering.value) {
    updateTooltipPosition(event);
  }
};

const handleMouseLeave = () => {
  isHovering.value = false;
};

const updateTooltipPosition = (event: MouseEvent) => {
  tooltipPosition.value = {
    x: event.clientX,
    y: event.clientY
  };
  
  // Adjust tooltip position to keep it within viewport
  if (tooltipRef.value) {
    const tooltip = tooltipRef.value;
    const tooltipRect = tooltip.getBoundingClientRect();
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    // Adjust horizontal position
    if (event.clientX + tooltipRect.width > viewportWidth) {
      tooltipPosition.value.x = event.clientX - tooltipRect.width;
    }
    
    // Adjust vertical position
    if (event.clientY + tooltipRect.height > viewportHeight) {
      tooltipPosition.value.y = event.clientY - tooltipRect.height;
    }
  }
};

// Add event listeners for mouse movement
onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove);
});

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove);
});
</script>

<template>
  <div class="flex items-center gap-2 relative">
    <!-- Rating Circle -->
    <div
      :class="[
        'rounded-full flex items-center justify-center font-bold transition-all duration-300',
        sizeClasses,
        ratingBgColor,
        ratingColor,
        interactive ? 'cursor-pointer hover:scale-110' : ''
      ]"
      @click="() => interactive && handleRatingClick(rating)"
      @mouseenter="handleMouseEnter"
      @mouseleave="handleMouseLeave"
    >
      <span v-if="isLemon">🍋</span>
      <span v-else-if="isPie">🥧</span>
      <span v-else>😐</span>
    </div>
    
    <!-- Rating Score -->
    <div class="flex flex-col">
      <div class="flex items-center gap-1">
        <span class="font-bold text-lg">{{ rating.toFixed(1) }}</span>
        <span class="text-sm text-gray-500">/10</span>
      </div>
      <span
        v-if="showText"
        :class="['text-xs font-medium', ratingColor]"
      >
        {{ ratingText }}
      </span>
    </div>
    
    <!-- Pie Chart Visualization Tooltip -->
    <Teleport to="body">
      <div
        v-if="isHovering"
        ref="tooltipRef"
        class="fixed z-[9999] bg-white dark:bg-gray-800 shadow-xl rounded-lg p-4 border border-gray-200 dark:border-gray-700 transition-all duration-300 transform origin-bottom-left"
        :style="{
          left: `${tooltipPosition.x + 15}px`,
          top: `${tooltipPosition.y + 15}px`
        }"
      >
      <div class="text-center mb-2">
        <h3 class="font-bold text-lg">Rating Breakdown</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">{{ rating.toFixed(1) }} out of 10</p>
      </div>
      
      <!-- Pie Chart Visualization -->
      <div class="flex justify-center">
        <div class="relative w-40 h-40">
          <!-- Pie Chart -->
          <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <!-- Background Circle -->
            <circle cx="50" cy="50" r="45" fill="#f3f4f6" />
            
            <!-- Pie Slices -->
            <g v-for="(slice, index) in pieSlices" :key="`pie-slice-${index}`">
              <path
                :d="slice.path"
                :fill="slice.color"
                stroke="white"
                stroke-width="1"
                class="animate-pulse-in"
                :style="{ animationDelay: `${index * 100}ms` }"
              />
            </g>
            
            <!-- Lemon Slices -->
            <g v-for="(slice, index) in lemonSlices" :key="`lemon-slice-${index}`">
              <path
                :d="slice.path"
                :fill="slice.color"
                stroke="white"
                stroke-width="1"
                class="animate-pulse-in"
                :style="{ animationDelay: `${(pieSlices.length + index) * 100}ms` }"
              />
            </g>
            
            <!-- Center Circle -->
            <circle cx="50" cy="50" r="15" fill="white" />
            
            <!-- Center Icon -->
            <text
              x="50"
              y="50"
              text-anchor="middle"
              dominant-baseline="middle"
              class="text-xl"
            >
              {{ isPie ? '🥧' : (isLemon ? '🍋' : '😐') }}
            </text>
          </svg>
        </div>
      </div>
      
      <!-- Legend -->
      <div class="flex justify-center gap-4 mt-3 text-sm">
        <div class="flex items-center gap-1">
          <div class="w-4 h-4 rounded-sm" style="background-color: #8B4513;"></div>
          <span class="text-gray-700 dark:text-gray-300">{{ pieSlices.length }} Pie</span>
        </div>
        <div class="flex items-center gap-1">
          <div class="w-4 h-4 rounded-sm" style="background-color: #FFD700;"></div>
          <span class="text-gray-700 dark:text-gray-300">{{ lemonSlices.length }} Lemon</span>
        </div>
      </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
/* Animation for pie chart icons */
@keyframes pulseIn {
  0% {
    opacity: 0;
    transform: scale(0.8);
  }
  70% {
    opacity: 1;
    transform: scale(1.05);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-pulse-in {
  animation: pulseIn 0.4s ease-out forwards;
  opacity: 0;
}
</style>