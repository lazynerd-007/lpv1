<template>
  <div class="critic-badge" :class="{ 'small': size === 'small', 'large': size === 'large' }">
    <div class="badge-container">
      <svg 
        class="badge-icon" 
        viewBox="0 0 24 24" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        <path 
          d="M12 2L15.09 8.26L22 9L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9L8.91 8.26L12 2Z" 
          fill="currentColor"
        />
      </svg>
      <span class="badge-text" v-if="showText">Critic</span>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: 'small' | 'medium' | 'large'
  showText?: boolean
}

withDefaults(defineProps<Props>(), {
  size: 'medium',
  showText: true
})
</script>

<style scoped>
.critic-badge {
  display: inline-flex;
  align-items: center;
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e  100%);
  color: #1a1a1a;
  border-radius: 12px;
  padding: 4px 8px;
  font-weight: 600;
  font-size: 0.75rem;
  box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
  border: 1px solid #e6c200;
  transition: all 0.2s ease;
}

.critic-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(255, 215, 0, 0.4);
}

.badge-container {
  display: flex;
  align-items: center;
  gap: 4px;
}

.badge-icon {
  width: 14px;
  height: 14px;
  flex-shrink: 0;
}

.badge-text {
  font-size: inherit;
  font-weight: inherit;
  white-space: nowrap;
}

/* Size variants */
.critic-badge.small {
  padding: 2px 6px;
  font-size: 0.625rem;
  border-radius: 8px;
}

.critic-badge.small .badge-icon {
  width: 10px;
  height: 10px;
}

.critic-badge.large {
  padding: 6px 12px;
  font-size: 0.875rem;
  border-radius: 16px;
}

.critic-badge.large .badge-icon {
  width: 18px;
  height: 18px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .critic-badge {
    background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
    color: #1a1a1a;
    border-color: #e6c200;
  }
}
</style>