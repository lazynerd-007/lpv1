<template>
  <div class="relative" ref="dropdownRef">
    <!-- Notification Bell Icon -->
    <button
      @click="notificationStore.toggleDropdown"
      class="relative p-2 text-gray-600 hover:text-gray-900 dark:text-gray-300 dark:hover:text-white transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 rounded-lg"
      :aria-expanded="notificationStore.isDropdownOpen"
      aria-haspopup="true"
      aria-label="Notifications"
    >
      <!-- Bell Icon -->
      <svg
        class="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
        />
      </svg>
      
      <!-- Unread Count Badge -->
      <span
        v-if="notificationStore.unreadCount > 0"
        class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center min-w-[20px] animate-pulse"
        :aria-label="`${notificationStore.unreadCount} unread notifications`"
      >
        {{ notificationStore.unreadCount > 99 ? '99+' : notificationStore.unreadCount }}
      </span>
    </button>

    <!-- Dropdown Modal -->
    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="notificationStore.isDropdownOpen"
        class="absolute right-0 mt-2 w-80 sm:w-96 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 max-h-[80vh] flex flex-col"
        role="dialog"
        aria-labelledby="notifications-title"
        aria-modal="true"
      >
        <!-- Header -->
        <div class="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 id="notifications-title" class="text-lg font-semibold text-gray-900 dark:text-white">
            Notifications
          </h3>
          <div class="flex items-center space-x-2">
            <button
              v-if="notificationStore.unreadCount > 0"
              @click="notificationStore.markAllAsRead"
              class="text-sm text-yellow-600 hover:text-yellow-700 dark:text-yellow-400 dark:hover:text-yellow-300 font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 rounded px-2 py-1"
            >
              Mark all read
            </button>
            <button
              @click="notificationStore.clearReadNotifications"
              class="text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 rounded px-2 py-1"
              title="Clear read notifications"
            >
              Clear
            </button>
          </div>
        </div>

        <!-- Notifications List -->
        <div class="flex-1 overflow-y-auto max-h-96">
          <div v-if="notificationStore.sortedNotifications.length === 0" class="p-8 text-center">
            <div class="text-gray-400 dark:text-gray-500 mb-2">
              <svg class="w-12 h-12 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
            </div>
            <p class="text-gray-500 dark:text-gray-400 font-medium">No notifications</p>
            <p class="text-sm text-gray-400 dark:text-gray-500 mt-1">You're all caught up!</p>
          </div>

          <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
            <div
              v-for="notification in notificationStore.sortedNotifications"
              :key="notification.id"
              class="p-4 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-200 cursor-pointer group"
              :class="{
                'bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400': !notification.isRead
              }"
              @click="handleNotificationClick(notification)"
              role="button"
              :tabindex="0"
              @keydown.enter="handleNotificationClick(notification)"
              @keydown.space.prevent="handleNotificationClick(notification)"
              :aria-label="`${notification.title}. ${notification.isRead ? 'Read' : 'Unread'}. ${notificationStore.formatTimestamp(notification.timestamp)}`"
            >
              <div class="flex items-start space-x-3">
                <!-- Notification Type Icon -->
                <div class="flex-shrink-0 mt-1">
                  <div
                    class="w-8 h-8 rounded-full flex items-center justify-center"
                    :class="getNotificationIconClass(notification.type)"
                  >
                    <component :is="getNotificationIcon(notification.type)" class="w-4 h-4" />
                  </div>
                </div>

                <!-- Notification Content -->
                <div class="flex-1 min-w-0">
                  <div class="flex items-start justify-between">
                    <div class="flex-1">
                      <p class="text-sm font-medium text-gray-900 dark:text-white group-hover:text-yellow-600 dark:group-hover:text-yellow-400 transition-colors duration-200">
                        {{ notification.title }}
                      </p>
                      <p class="text-sm text-gray-600 dark:text-gray-300 mt-1 line-clamp-2">
                        {{ notification.message }}
                      </p>
                      <div class="flex items-center justify-between mt-2">
                        <p class="text-xs text-gray-500 dark:text-gray-400">
                          {{ notificationStore.formatTimestamp(notification.timestamp) }}
                        </p>
                        <button
                          v-if="notification.actionText && notification.actionUrl"
                          class="text-xs text-yellow-600 hover:text-yellow-700 dark:text-yellow-400 dark:hover:text-yellow-300 font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 rounded px-2 py-1"
                          @click.stop="handleActionClick(notification)"
                        >
                          {{ notification.actionText }}
                        </button>
                      </div>
                    </div>
                    
                    <!-- Unread Indicator -->
                    <div v-if="!notification.isRead" class="flex-shrink-0 ml-2">
                      <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
                    </div>
                  </div>
                </div>

                <!-- Remove Button -->
                <button
                  @click.stop="notificationStore.removeNotification(notification.id)"
                  class="flex-shrink-0 opacity-0 group-hover:opacity-100 text-gray-400 hover:text-red-500 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 rounded p-1"
                  :aria-label="`Remove ${notification.title} notification`"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Footer -->
        <div v-if="notificationStore.sortedNotifications.length > 0" class="p-3 border-t border-gray-200 dark:border-gray-700">
          <button
            @click="notificationStore.clearAllNotifications"
            class="w-full text-sm text-gray-500 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 rounded py-2"
          >
            Clear all notifications
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useNotificationStore, type Notification } from '../../stores/notificationStore'

const router = useRouter()
const notificationStore = useNotificationStore()
const dropdownRef = ref<HTMLElement>()

// Access store properties directly to maintain reactivity
// Note: We don't destructure to preserve Vue 3 reactivity

// Handle notification click
const handleNotificationClick = (notification: Notification) => {
  if (!notification.isRead) {
    notificationStore.markAsRead(notification.id)
  }
  
  if (notification.actionUrl) {
    notificationStore.closeDropdown()
    router.push(notification.actionUrl)
  }
}

// Handle action button click
const handleActionClick = (notification: Notification) => {
  if (notification.actionUrl) {
    router.push(notification.actionUrl)
    notificationStore.closeDropdown()
  }
}

// Get notification icon based on type
const getNotificationIcon = (type: Notification['type']) => {
  const icons = {
    info: 'InfoIcon',
    success: 'CheckIcon',
    warning: 'ExclamationIcon',
    error: 'XCircleIcon'
  }
  return icons[type] || 'InfoIcon'
}

// Get notification icon class based on type
const getNotificationIconClass = (type: Notification['type']) => {
  const classes = {
    info: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
    success: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
    warning: 'bg-yellow-100 text-yellow-600 dark:bg-yellow-900/30 dark:text-yellow-400',
    error: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400'
  }
  return classes[type] || classes.info
}

// Click outside handler
const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    notificationStore.closeDropdown()
  }
}

// Escape key handler
const handleEscapeKey = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && notificationStore.isDropdownOpen) {
    notificationStore.closeDropdown()
  }
}

// Setup event listeners
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleEscapeKey)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleEscapeKey)
})
</script>

<script lang="ts">
// Icon components
const InfoIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
}

const CheckIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
    </svg>
  `
}

const ExclamationIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
    </svg>
  `
}

const XCircleIcon = {
  template: `
    <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
  `
}

export default {
  components: {
    InfoIcon,
    CheckIcon,
    ExclamationIcon,
    XCircleIcon
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>