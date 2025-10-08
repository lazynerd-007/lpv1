<template>
  <div class="activity-feed">
    <!-- Activity Filter Tabs -->
    <div class="bg-theme-surface rounded-lg p-2 mb-6 flex flex-wrap gap-2">
      <button 
        @click="activeFilter = 'all'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
          activeFilter === 'all' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
        ]"
      >
        <Activity class="w-4 h-4" />
        All Activity
      </button>
      <button 
        @click="activeFilter = 'reviews'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
          activeFilter === 'reviews' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
        ]"
      >
        <MessageSquare class="w-4 h-4" />
        Reviews
      </button>
      <button 
        @click="activeFilter = 'ratings'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
          activeFilter === 'ratings' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
        ]"
      >
        <Star class="w-4 h-4" />
        Ratings
      </button>
      <button 
        @click="activeFilter = 'follows'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
          activeFilter === 'follows' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
        ]"
      >
        <UserPlus class="w-4 h-4" />
        Follows
      </button>
      <button 
        @click="activeFilter = 'watchlist'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
          activeFilter === 'watchlist' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
        ]"
      >
        <Bookmark class="w-4 h-4" />
        Watchlist
      </button>
      <button 
        @click="activeFilter = 'favorites'"
        :class="[
          'px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2',
          activeFilter === 'favorites' ? 'bg-theme-primary text-theme-primary-text' : 'text-theme-text hover:bg-theme-surface-hover'
        ]"
      >
        <Heart class="w-4 h-4" />
        Favorites
      </button>
    </div>

    <!-- Activity Feed -->
    <div class="space-y-4">
      <div v-if="filteredActivities.length > 0">
        <div 
          v-for="activity in filteredActivities" 
          :key="activity.id" 
          class="bg-theme-card rounded-lg p-6 hover:shadow-lg transition-shadow"
        >
          <div class="flex items-start gap-4">
            <!-- Activity Icon -->
            <div class="flex-shrink-0">
              <div 
                :class="[
                  'w-10 h-10 rounded-full flex items-center justify-center',
                  getActivityIconClass(activity.type)
                ]"
              >
                <component :is="getActivityIcon(activity.type)" class="w-5 h-5" />
              </div>
            </div>

            <!-- Activity Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-center justify-between mb-2">
                <h3 class="font-semibold text-lg truncate">{{ getActivityTitle(activity) }}</h3>
                <span class="text-sm text-theme-secondary flex-shrink-0">{{ formatTimeAgo(new Date(activity.timestamp).getTime()) }}</span>
              </div>
              
              <p class="text-theme-secondary mb-3">{{ getActivityDescription(activity) }}</p>
              
              <!-- Activity Details -->
              <div v-if="getMovieTitle(activity)" class="flex items-center gap-2 text-sm">
                <Film class="w-4 h-4 text-theme-secondary" />
                <span class="font-medium">{{ getMovieTitle(activity) }}</span>
                <span v-if="activity.rating" class="flex items-center gap-1 ml-2">
                  <Star class="w-4 h-4 text-yellow-400 fill-current" />
                  <span>{{ activity.rating }}/5</span>
                </span>
              </div>
              
              <div v-if="getTargetUserName(activity)" class="flex items-center gap-2 text-sm">
                <User class="w-4 h-4 text-theme-secondary" />
                <span class="font-medium">{{ getTargetUserName(activity) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <Activity class="w-16 h-16 text-theme-secondary mx-auto mb-4" />
        <h3 class="text-xl font-semibold mb-2">No Activity Yet</h3>
        <p class="text-theme-secondary">
          {{ activeFilter === 'all' 
            ? 'Start reviewing movies, adding to watchlist, or following users to see activity here.' 
            : `No ${activeFilter} activity found.` 
          }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useMovieStore } from '@/stores/movieStore'
import { 
  Activity, MessageSquare, Star, UserPlus, Bookmark, Heart, 
  Film, User, Clock
} from 'lucide-vue-next'

interface Props {
  userId?: string
  limit?: number
}

const props = withDefaults(defineProps<Props>(), {
  limit: 20
})

const userStore = useUserStore()
const movieStore = useMovieStore()
const activeFilter = ref<'all' | 'reviews' | 'ratings' | 'follows' | 'watchlist' | 'favorites'>('all')

// Get activities based on props
const activities = computed(() => {
  if (props.userId) {
    return userStore.getActivitiesForUser(props.userId).slice(0, props.limit)
  }
  return userStore.recentActivities.slice(0, props.limit)
})

// Filter activities based on active filter
const filteredActivities = computed(() => {
  if (activeFilter.value === 'all') {
    return userStore.userActivities.slice(0, props.limit)
  }
  
  // Map filter values to actual activity types
  const filterMap: Record<string, string> = {
    'reviews': 'review',
    'ratings': 'rating', 
    'follows': 'follow',
    'watchlist': 'watchlist_add',
    'favorites': 'favorite_add'
  }
  
  const activityType = filterMap[activeFilter.value] || activeFilter.value
  return userStore.getActivitiesByType(activityType as any).slice(0, props.limit)
})

// Activity icon mapping
const getActivityIcon = (type: string) => {
  const iconMap: Record<string, any> = {
    review: MessageSquare,
    rating: Star,
    follow: UserPlus,
    watchlist: Bookmark,
    favorites: Heart
  }
  return iconMap[type] || Activity
}

// Activity icon class mapping
const getActivityIconClass = (type: string) => {
  const classMap: Record<string, string> = {
    review: 'bg-blue-500 text-white',
    rating: 'bg-yellow-500 text-white',
    follow: 'bg-green-500 text-white',
    watchlist: 'bg-purple-500 text-white',
    favorites: 'bg-red-500 text-white'
  }
  return classMap[type] || 'bg-gray-500 text-white'
}

// Activity title generation
const getActivityTitle = (activity: any) => {
  const titleMap: Record<string, string> = {
    review: 'Wrote a Review',
    rating: 'Rated a Movie',
    follow: 'Followed User',
    watchlist: 'Added to Watchlist',
    favorites: 'Added to Favorites'
  }
  return titleMap[activity.type] || 'Activity'
}

// Activity description generation
const getActivityDescription = (activity: any) => {
  const user = userStore.currentUser
  const userName = user?.name || 'User'
  
  switch (activity.type) {
    case 'review':
      return `${userName} shared their thoughts on this movie`
    case 'rating':
      return `${userName} gave this movie ${activity.rating} stars`
    case 'follow':
      return `${userName} started following ${activity.targetUserName}`
    case 'watchlist':
      return `${userName} wants to watch this movie`
    case 'favorites':
      return `${userName} loved this movie`
    default:
      return 'Recent activity'
  }
}

// Helper functions to get movie title and user name
const getMovieTitle = (activity: any) => {
  if (activity.targetType === 'movie') {
    const movie = movieStore.getMovieById(activity.targetId)
    return movie?.title
  }
  return null
}

const getTargetUserName = (activity: any) => {
  if (activity.targetType === 'user') {
    // For now, return a placeholder since we don't have a user lookup method
    // This should be implemented when user management is added
    return 'User'
  }
  return null
}

// Time formatting
const formatTimeAgo = (timestamp: number) => {
  const now = Date.now()
  const diff = now - timestamp
  const minutes = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)
  
  if (minutes < 1) return 'Just now'
  if (minutes < 60) return `${minutes}m ago`
  if (hours < 24) return `${hours}h ago`
  if (days < 7) return `${days}d ago`
  return new Date(timestamp).toLocaleDateString()
}

onMounted(() => {
  // Load activities if needed
})
</script>

<style scoped>
.activity-feed {
  @apply w-full;
}
</style>