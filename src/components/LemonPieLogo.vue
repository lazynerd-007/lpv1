<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  textColor?: string;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  textColor: 'text-white'
});

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'text-xl';
    case 'lg':
      return 'text-3xl';
    case 'xl':
      return 'text-4xl';
    default: // md
      return 'text-2xl';
  }
});
</script>

<template>
  <div class="flex items-center justify-center gap-2" :class="sizeClasses">
    <div class="flex items-center">
      <span class="text-yellow-400">🍋</span>
      <span class="text-orange-400">🥧</span>
    </div>
    <span :class="textColor" class="font-bold">LemonNPie</span>
  </div>
</template>