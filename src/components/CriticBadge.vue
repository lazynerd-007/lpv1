<template>
  <div 
    class="critic-badge" 
    :class="{ 
      'small': size === 'small', 
      'large': size === 'large',
      'verified': isVerified,
      'unverified': !isVerified
    }"
    :title="badgeTitle"
  >
    <div class="badge-container">
      <!-- Verification checkmark for verified critics -->
      <svg 
        v-if="isVerified"
        class="verification-icon" 
        viewBox="0 0 24 24" 
        fill="none" 
        xmlns="http://www.w3.org/2000/svg"
      >
        <path 
          d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" 
          stroke="currentColor" 
          stroke-width="2" 
          stroke-linecap="round" 
          stroke-linejoin="round"
        />
      </svg>
      
      <!-- Star icon for all critics -->
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
      
      <span class="badge-text" v-if="showText">
        {{ isVerified ? 'Verified Critic' : 'Critic' }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'small' | 'medium' | 'large'
  showText?: boolean
  isVerified?: boolean
  verificationLevel?: 'basic' | 'professional' | 'expert'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'medium',
  showText: true,
  isVerified: false,
  verificationLevel: 'basic'
})

const badgeTitle = computed(() => {
  if (!props.isVerified) {
    return 'Critic - Unverified'
  }
  
  const levelTitles = {
    basic: 'Verified Critic - Basic Level',
    professional: 'Verified Critic - Professional Level', 
    expert: 'Verified Critic - Expert Level'
  }
  
  return levelTitles[props.verificationLevel]
})
</script>

<style scoped>
.critic-badge {
  display: inline-flex;
  align-items: center;
  border-radius: 12px;
  padding: 4px 8px;
  font-weight: 600;
  font-size: 0.75rem;
  transition: all 0.2s ease;
  position: relative;
}

/* Verified critic styling */
.critic-badge.verified {
  background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3);
  border: 1px solid #059669;
}

.critic-badge.verified:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.4);
}

/* Unverified critic styling */
.critic-badge.unverified {
  background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
  color: #1a1a1a;
  box-shadow: 0 2px 4px rgba(255, 215, 0, 0.3);
  border: 1px solid #e6c200;
}

.critic-badge.unverified:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(255, 215, 0, 0.4);
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

.verification-icon {
  width: 12px;
  height: 12px;
  flex-shrink: 0;
  margin-right: 2px;
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

.critic-badge.small .verification-icon {
  width: 8px;
  height: 8px;
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

.critic-badge.large .verification-icon {
  width: 16px;
  height: 16px;
}

.critic-badge.large .badge-icon {
  width: 18px;
  height: 18px;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .critic-badge.verified {
    background: linear-gradient(135deg, #059669 0%, #10b981 100%);
    color: white;
    border-color: #047857;
  }
  
  .critic-badge.unverified {
    background: linear-gradient(135deg, #d97706 0%, #f59e0b 100%);
    color: white;
    border-color: #b45309;
  }
}
</style>