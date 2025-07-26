<script setup lang="ts">
import { computed } from 'vue';

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

const handleRatingClick = (newRating: number) => {
  if (props.interactive) {
    emit('ratingChange', newRating);
  }
};
</script>

<template>
  <div class="flex items-center gap-2">
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
  </div>
</template>