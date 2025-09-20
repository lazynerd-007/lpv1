<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import { Shield, Users, BarChart3, Settings, FileText, AlertTriangle } from 'lucide-vue-next'

const userStore = useUserStore()
const router = useRouter()

const currentUser = computed(() => userStore.currentUser)
const isAdmin = computed(() => currentUser.value?.role === 'admin')

// Redirect non-admin users
if (!isAdmin.value) {
  router.push('/')
}

const adminStats = {
  totalUsers: 1247,
  totalMovies: 856,
  totalReviews: 3421,
  pendingReports: 12
}

const adminActions = [
  {
    title: 'User Management',
    description: 'Manage user accounts, roles, and permissions',
    icon: Users,
    path: '/admin/users',
    color: 'bg-blue-500'
  },
  {
    title: 'Content Management',
    description: 'Add, edit, and manage movies and series',
    icon: FileText,
    path: '/admin/content',
    color: 'bg-green-500'
  },
  {
    title: 'Analytics',
    description: 'View platform statistics and user engagement',
    icon: BarChart3,
    path: '/admin/analytics',
    color: 'bg-purple-500'
  },
  {
    title: 'Reports & Moderation',
    description: 'Handle user reports and content moderation',
    icon: AlertTriangle,
    path: '/admin/reports',
    color: 'bg-red-500',
    badge: adminStats.pendingReports
  },
  {
    title: 'System Settings',
    description: 'Configure platform settings and preferences',
    icon: Settings,
    path: '/admin/settings',
    color: 'bg-gray-500'
  }
]

const navigateTo = (path: string) => {
  // For now, just show an alert since these are placeholder routes
  alert(`Navigation to ${path} - This would be implemented in a real admin panel`)
}
</script>

<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container mx-auto px-4">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center gap-3 mb-4">
          <Shield class="w-8 h-8 text-orange-500" />
          <h1 class="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
        </div>
        <p class="text-gray-600">
          Welcome back, {{ currentUser?.name }}. Manage your LemonPie platform from here.
        </p>
      </div>

      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Users</p>
              <p class="text-2xl font-bold text-gray-900">{{ adminStats.totalUsers.toLocaleString() }}</p>
            </div>
            <Users class="w-8 h-8 text-blue-500" />
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Movies</p>
              <p class="text-2xl font-bold text-gray-900">{{ adminStats.totalMovies.toLocaleString() }}</p>
            </div>
            <FileText class="w-8 h-8 text-green-500" />
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Total Reviews</p>
              <p class="text-2xl font-bold text-gray-900">{{ adminStats.totalReviews.toLocaleString() }}</p>
            </div>
            <BarChart3 class="w-8 h-8 text-purple-500" />
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm font-medium text-gray-600">Pending Reports</p>
              <p class="text-2xl font-bold text-gray-900">{{ adminStats.pendingReports }}</p>
            </div>
            <AlertTriangle class="w-8 h-8 text-red-500" />
          </div>
        </div>
      </div>

      <!-- Admin Actions -->
      <div class="mb-8">
        <h2 class="text-xl font-semibold text-gray-900 mb-6">Administrative Functions</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="action in adminActions" 
            :key="action.title"
            @click="navigateTo(action.path)"
            class="bg-white rounded-lg shadow-md p-6 cursor-pointer hover:shadow-lg transition-shadow duration-200 border border-gray-200 hover:border-orange-300"
          >
            <div class="flex items-start gap-4">
              <div :class="[action.color, 'p-3 rounded-lg']">
                <component :is="action.icon" class="w-6 h-6 text-white" />
              </div>
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-2">
                  <h3 class="font-semibold text-gray-900">{{ action.title }}</h3>
                  <span 
                    v-if="action.badge" 
                    class="bg-red-100 text-red-800 text-xs font-medium px-2 py-1 rounded-full"
                  >
                    {{ action.badge }}
                  </span>
                </div>
                <p class="text-sm text-gray-600">{{ action.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <div class="space-y-4">
          <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
            <div class="w-2 h-2 bg-green-500 rounded-full"></div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">New user registration</p>
              <p class="text-xs text-gray-600">funmi.adebayo@example.com joined 2 hours ago</p>
            </div>
          </div>
          
          <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
            <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Movie review submitted</p>
              <p class="text-xs text-gray-600">Review for "The Wedding Party" by Kemi Okafor</p>
            </div>
          </div>
          
          <div class="flex items-center gap-4 p-4 bg-gray-50 rounded-lg">
            <div class="w-2 h-2 bg-yellow-500 rounded-full"></div>
            <div class="flex-1">
              <p class="text-sm font-medium text-gray-900">Content report received</p>
              <p class="text-xs text-gray-600">User reported inappropriate comment on "King of Boys"</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Additional styles if needed */
</style>