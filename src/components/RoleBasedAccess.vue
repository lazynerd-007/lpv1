<template>
  <div v-if="hasAccess" class="role-based-access">
    <slot></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/userStore'

const props = defineProps({
  requiredRole: {
    type: [String, Array],
    required: true
  },
  requireAll: {
    type: Boolean,
    default: false
  }
})

const userStore = useUserStore()

const hasAccess = computed(() => {
  if (!userStore.isAuthenticated || !userStore.currentUser) {
    return false
  }

  const userRole = userStore.currentUser.role
  const requiredRoles = Array.isArray(props.requiredRole) ? props.requiredRole : [props.requiredRole]

  if (props.requireAll) {
    // User must have all required roles (not typical, but available)
    return requiredRoles.every(role => userRole === role)
  } else {
    // User must have at least one of the required roles
    return requiredRoles.includes(userRole)
  }
})
</script>

<style scoped>
.role-based-access {
  /* Component wrapper - no specific styling needed */
}
</style>