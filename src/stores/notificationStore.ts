import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface Notification {
  id: string
  title: string
  message: string
  type: 'info' | 'success' | 'warning' | 'error'
  timestamp: Date
  isRead: boolean
  actionUrl?: string
  actionText?: string
}

export const useNotificationStore = defineStore('notification', () => {
  // State
  const notifications = ref<Notification[]>([
    {
      id: '1',
      title: 'Welcome to LemonPie!',
      message: 'Thanks for joining our movie review community. Start exploring and sharing your thoughts!',
      type: 'success',
      timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
      isRead: false,
      actionUrl: '/browse-movies',
      actionText: 'Browse Movies'
    },
    {
      id: '2',
      title: 'New Review on "Inception"',
      message: 'Someone commented on your review of Inception. Check it out!',
      type: 'info',
      timestamp: new Date(Date.now() - 4 * 60 * 60 * 1000), // 4 hours ago
      isRead: false,
      actionUrl: '/movie/inception',
      actionText: 'View Review'
    },
    {
      id: '3',
      title: 'Movie Added to Watchlist',
      message: '"The Dark Knight" has been successfully added to your watchlist.',
      type: 'success',
      timestamp: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000), // 1 day ago
      isRead: true,
      actionUrl: '/profile',
      actionText: 'View Watchlist'
    },
    {
      id: '4',
      title: 'Weekly Digest Available',
      message: 'Your weekly movie recommendations are ready. Discover new films based on your preferences!',
      type: 'info',
      timestamp: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000), // 2 days ago
      isRead: true,
      actionUrl: '/recommendations',
      actionText: 'View Recommendations'
    },
    {
      id: '5',
      title: 'Profile Update Required',
      message: 'Please update your profile information to get better movie recommendations.',
      type: 'warning',
      timestamp: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
      isRead: false,
      actionUrl: '/profile',
      actionText: 'Update Profile'
    },
    {
      id: '6',
      title: 'System Maintenance',
      message: 'Scheduled maintenance will occur tonight from 2-4 AM EST. Some features may be temporarily unavailable.',
      type: 'warning',
      timestamp: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000), // 5 days ago
      isRead: true
    }
  ])

  const isDropdownOpen = ref(false)

  // Getters
  const unreadCount = computed(() => 
    notifications.value.filter(n => !n.isRead).length
  )

  const sortedNotifications = computed(() => 
    [...notifications.value].sort((a, b) => 
      new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
    )
  )

  const unreadNotifications = computed(() => 
    notifications.value.filter(n => !n.isRead)
  )

  // Actions
  const markAsRead = (notificationId: string) => {
    const notification = notifications.value.find(n => n.id === notificationId)
    if (notification) {
      notification.isRead = true
    }
  }

  const markAllAsRead = () => {
    notifications.value.forEach(notification => {
      notification.isRead = true
    })
  }

  const clearAllNotifications = () => {
    notifications.value = []
  }

  const clearReadNotifications = () => {
    notifications.value = notifications.value.filter(n => !n.isRead)
  }

  const addNotification = (notification: Omit<Notification, 'id' | 'timestamp'>) => {
    const newNotification: Notification = {
      ...notification,
      id: Date.now().toString(),
      timestamp: new Date()
    }
    notifications.value.unshift(newNotification)
  }

  const removeNotification = (notificationId: string) => {
    const index = notifications.value.findIndex(n => n.id === notificationId)
    if (index > -1) {
      notifications.value.splice(index, 1)
    }
  }

  const toggleDropdown = () => {
    isDropdownOpen.value = !isDropdownOpen.value
  }

  const closeDropdown = () => {
    isDropdownOpen.value = false
  }

  const openDropdown = () => {
    isDropdownOpen.value = true
  }

  // Utility function to format timestamp
  const formatTimestamp = (timestamp: Date): string => {
    const now = new Date()
    const diff = now.getTime() - timestamp.getTime()
    const minutes = Math.floor(diff / (1000 * 60))
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const days = Math.floor(diff / (1000 * 60 * 60 * 24))

    if (minutes < 1) return 'Just now'
    if (minutes < 60) return `${minutes}m ago`
    if (hours < 24) return `${hours}h ago`
    if (days < 7) return `${days}d ago`
    
    return timestamp.toLocaleDateString()
  }

  return {
    // State
    notifications,
    isDropdownOpen,
    
    // Getters
    unreadCount,
    sortedNotifications,
    unreadNotifications,
    
    // Actions
    markAsRead,
    markAllAsRead,
    clearAllNotifications,
    clearReadNotifications,
    addNotification,
    removeNotification,
    toggleDropdown,
    closeDropdown,
    openDropdown,
    formatTimestamp
  }
})