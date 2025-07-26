<template>
  <div class="form-control mb-6">
    <label class="label">
      <span class="label-text font-semibold text-lg text-gray-300">Your Lemon 🍋 or Pie 🥧 Rating</span>
    </label>
    <div class="flex flex-col gap-4">
      <!-- Rating Slider -->
      <div class="flex items-center gap-4">
        <span class="text-2xl">🍋</span>
        <input 
          :value="rating" 
          @input="updateRating"
          type="range" 
          min="1" 
          max="10" 
          class="range range-warning flex-1" 
          step="1"
        />
        <span class="text-2xl">🥧</span>
      </div>
      
      <!-- Rating Display -->
      <div class="text-center">
        <div class="text-4xl mb-2">
          {{ rating <= 5 ? '🍋' : '🥧' }}
        </div>
        <div class="text-xl font-bold text-white">
          {{ rating }}/10 - {{ getRatingLabel(rating) }}
        </div>
        <div class="text-sm text-gray-400">
          {{ rating <= 5 ? 'Fresh Lemon' : 'Delicious Pie' }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  rating: number
}

interface Emits {
  (e: 'update:rating', value: number): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const updateRating = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:rating', parseInt(target.value))
}

const getRatingLabel = (rating: number): string => {
  if (rating <= 2) return 'Terrible'
  if (rating <= 4) return 'Poor'
  if (rating <= 5) return 'Average'
  if (rating <= 6) return 'Good'
  if (rating <= 8) return 'Great'
  if (rating <= 9) return 'Excellent'
  return 'Masterpiece'
}
</script>

<style scoped>
/* Custom range styling */
.range::-webkit-slider-thumb {
  background: linear-gradient(45deg, #fbbf24, #f59e0b);
}

.range::-moz-range-thumb {
  background: linear-gradient(45deg, #fbbf24, #f59e0b);
  border: none;
}
</style>