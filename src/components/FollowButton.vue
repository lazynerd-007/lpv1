<template>
  <button
    @click="toggleFollow"
    :disabled="loading"
    :class="[
      'btn transition-all duration-200',
      isFollowing 
        ? 'btn-outline btn-secondary hover:btn-error' 
        : 'btn-primary',
      loading ? 'loading' : ''
    ]"
  >
    <UserPlus v-if="!isFollowing && !loading" class="w-4 h-4 mr-2" />
    <UserCheck v-if="isFollowing && !loading" class="w-4 h-4 mr-2" />
    <span v-if="!loading">
      {{ isFollowing ? (isHovered ? 'Unfollow' : 'Following') : 'Follow' }}
    </span>
  </button>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { UserPlus, UserCheck } from 'lucide-vue-next'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'

interface Props {
  userId: string
  variant?: 'default' | 'small'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'default'
})

const userStore = useUserStore()
const uiStore = useUIStore()

const loading = ref(false)
const isHovered = ref(false)

const isFollowing = computed(() => {
  return userStore.followingUsers.some(user => user.id === props.userId)
})

const toggleFollow = async () => {
  if (!userStore.currentUser) {
    uiStore.showErrorToast('Please log in to follow users')
    return
  }

  if (props.userId === userStore.currentUser.id) {
    uiStore.showErrorToast('You cannot follow yourself')
    return
  }

  loading.value = true

  try {
    if (isFollowing.value) {
      await userStore.unfollowUser(props.userId)
      uiStore.showSuccessToast('User unfollowed successfully')
    } else {
      await userStore.followUser(props.userId)
      uiStore.showSuccessToast('User followed successfully')
    }
  } catch (error) {
    uiStore.showErrorToast('Failed to update follow status')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.btn:hover .hover-text {
  display: inline;
}

.btn .hover-text {
  display: none;
}
</style>