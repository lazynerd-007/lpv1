<template>
  <button
    @click="handleToggleFollow"
    @mouseenter="handleMouseEnter"
    @mouseleave="handleMouseLeave"
    :disabled="isLoading || isCurrentUser"
    :class="[
      'px-4 py-2 rounded-lg font-medium transition-all duration-200 flex items-center gap-2',
      'focus:outline-none focus:ring-2 focus:ring-offset-2',
      isCurrentUser
        ? 'bg-gray-100 text-gray-400 cursor-not-allowed dark:bg-gray-800 dark:text-gray-600'
        : isFollowing
        ? 'bg-red-500 hover:bg-red-600 text-white focus:ring-red-500'
        : 'bg-blue-500 hover:bg-blue-600 text-white focus:ring-blue-500',
      isLoading && 'opacity-75 cursor-not-allowed',
      size === 'sm' ? 'px-3 py-1.5 text-sm' : 'px-4 py-2 text-base'
    ]"
  >
    <!-- Loading spinner -->
    <div
      v-if="isLoading"
      class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"
    ></div>
    
    <!-- Follow/Unfollow icons -->
    <UserPlus v-else-if="!isFollowing && !isCurrentUser" class="w-4 h-4" />
    <UserMinus v-else-if="isFollowing && !isCurrentUser" class="w-4 h-4" />
    <User v-else class="w-4 h-4" />
    
    <!-- Button text -->
    <span v-if="!isLoading">
      <template v-if="isCurrentUser">You</template>
      <template v-else-if="isFollowing">{{ showUnfollowText ? 'Unfollow' : 'Following' }}</template>
      <template v-else>Follow</template>
    </span>
    <span v-else>{{ isFollowing ? 'Unfollowing...' : 'Following...' }}</span>
  </button>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { UserPlus, UserMinus, User } from 'lucide-vue-next'
import { useUserStore } from '@/stores/userStore'
import { toast } from 'vue-sonner'

interface Props {
  userId: string
  size?: 'sm' | 'md'
  showUnfollowText?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  showUnfollowText: false
})

const userStore = useUserStore()
const isLoading = ref(false)
const showUnfollowText = ref(props.showUnfollowText)

// Computed properties
const isFollowing = computed(() => userStore.isFollowing(props.userId))
const isCurrentUser = computed(() => userStore.currentUser?.id === props.userId)

// Mouse events for hover effect on following button
let hoverTimeout: ReturnType<typeof setTimeout> | null = null

const handleMouseEnter = () => {
  if (isFollowing.value && !props.showUnfollowText) {
    hoverTimeout = setTimeout(() => {
      showUnfollowText.value = true
    }, 300)
  }
}

const handleMouseLeave = () => {
  if (hoverTimeout) {
    clearTimeout(hoverTimeout)
    hoverTimeout = null
  }
  if (!props.showUnfollowText) {
    showUnfollowText.value = false
  }
}

// Follow/unfollow handler
const handleToggleFollow = async () => {
  if (isCurrentUser.value || isLoading.value) return

  isLoading.value = true
  
  try {
    const result = await userStore.toggleFollow(props.userId)
    
    if (result.success) {
      const action = isFollowing.value ? 'Unfollowed' : 'Followed'
      toast.success(`${action} user successfully`)
    } else {
      toast.error(result.error || 'Failed to update follow status')
    }
  } catch (error) {
    console.error('Follow toggle error:', error)
    toast.error('An unexpected error occurred')
  } finally {
    isLoading.value = false
  }
}


</script>

<style scoped>
/* Additional hover effects */
.group:hover .group-hover\:block {
  display: block;
}

.group:hover .group-hover\:hidden {
  display: none;
}

/* Smooth transitions */
button {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

button:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* Dark mode enhancements */
@media (prefers-color-scheme: dark) {
  button:hover:not(:disabled) {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }
}
</style>