<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Admin Header -->
    <header class="bg-white shadow-sm border-b border-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <h1 class="text-2xl font-bold text-slate-900">Admin Dashboard</h1>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="refreshData"
              :disabled="adminStore.isLoading"
              class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              <RefreshCw :class="{ 'animate-spin': adminStore.isLoading }" class="w-4 h-4 mr-2" />
              Refresh
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Admin Navigation -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex space-x-8">
          <router-link
            v-for="navItem in navigation"
            :key="navItem.name"
            :to="navItem.to"
            class="border-b-2 border-transparent py-4 px-1 text-sm font-medium text-slate-500 hover:text-slate-700 hover:border-slate-300"
            :class="{
              'border-blue-500 text-blue-600': $route.name === navItem.name
            }"
          >
            <component :is="navItem.icon" class="w-4 h-4 inline mr-2" />
            {{ navItem.label }}
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- System Health Alert -->
      <div v-if="adminStore.systemMetrics.systemHealth !== 'healthy'" class="mb-6">
        <div class="rounded-md bg-yellow-50 p-4">
          <div class="flex">
            <AlertTriangle class="h-5 w-5 text-yellow-400" />
            <div class="ml-3">
              <h3 class="text-sm font-medium text-yellow-800">
                System Health Warning
              </h3>
              <div class="mt-2 text-sm text-yellow-700">
                <p>System health status: {{ adminStore.systemMetrics.systemHealth }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Key Metrics -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div
          v-for="metric in keyMetrics"
          :key="metric.name"
          class="bg-white overflow-hidden shadow rounded-lg"
        >
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <component :is="metric.icon" class="h-6 w-6 text-slate-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">
                    {{ metric.name }}
                  </dt>
                  <dd>
                    <div class="text-lg font-medium text-slate-900">
                      {{ metric.value }}
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
          <div class="bg-slate-50 px-5 py-3">
            <div class="text-sm">
              <span
                :class="{
                  'text-green-600': metric.change > 0,
                  'text-red-600': metric.change < 0,
                  'text-slate-600': metric.change === 0
                }"
              >
                {{ metric.change > 0 ? '+' : '' }}{{ metric.change }}%
              </span>
              <span class="text-slate-500 ml-2">from last month</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="bg-white shadow rounded-lg mb-8">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">
            Quick Actions
          </h3>
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <button
              v-for="action in quickActions"
              :key="action.name"
              @click="action.action"
              class="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-blue-500 rounded-lg border border-slate-200 hover:border-slate-300 hover:shadow-md transition-all duration-200"
            >
              <div>
                <span class="rounded-lg inline-flex p-3 ring-4 ring-white" :class="action.iconBg">
                  <component :is="action.icon" class="h-6 w-6" :class="action.iconColor" />
                </span>
              </div>
              <div class="mt-4">
                <h3 class="text-lg font-medium text-slate-900">
                  {{ action.name }}
                </h3>
                <p class="mt-2 text-sm text-slate-500">
                  {{ action.description }}
                </p>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Recent Activity & System Status -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Recent Activity -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">
              Recent Activity
            </h3>
            <div class="flow-root">
              <ul class="-mb-8">
                <li v-for="(activity, index) in adminStore.recentActions" :key="activity.id">
                  <div class="relative pb-8" :class="{ 'pb-0': index === adminStore.recentActions.length - 1 }">
                    <span
                      v-if="index !== adminStore.recentActions.length - 1"
                      class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-slate-200"
                    ></span>
                    <div class="relative flex space-x-3">
                      <div>
                        <span class="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center ring-8 ring-white">
                          <Shield class="h-4 w-4 text-white" />
                        </span>
                      </div>
                      <div class="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                        <div>
                          <p class="text-sm text-slate-500">
                            <span class="font-medium text-slate-900">{{ activity.action }}</span>
                            on review {{ activity.review_id }}
                          </p>
                          <p v-if="activity.reason" class="text-xs text-slate-400 mt-1">
                            Reason: {{ activity.reason }}
                          </p>
                        </div>
                        <div class="text-right text-sm whitespace-nowrap text-slate-500">
                          {{ formatDate(activity.created_at) }}
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
            <div class="mt-6">
              <router-link
                to="/admin/logs"
                class="w-full flex justify-center items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50"
              >
                View all logs
              </router-link>
            </div>
          </div>
        </div>

        <!-- System Status -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">
              System Status
            </h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <Server class="h-5 w-5 text-slate-400 mr-3" />
                  <span class="text-sm font-medium text-slate-900">Server Status</span>
                </div>
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-800': adminStore.systemMetrics.serverStatus === 'online',
                    'bg-red-100 text-red-800': adminStore.systemMetrics.serverStatus === 'offline',
                    'bg-yellow-100 text-yellow-800': adminStore.systemMetrics.serverStatus === 'maintenance'
                  }"
                >
                  {{ adminStore.systemMetrics.serverStatus }}
                </span>
              </div>
              
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <Database class="h-5 w-5 text-slate-400 mr-3" />
                  <span class="text-sm font-medium text-slate-900">Database Health</span>
                </div>
                <span
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="{
                    'bg-green-100 text-green-800': adminStore.systemMetrics.systemHealth === 'healthy',
                    'bg-yellow-100 text-yellow-800': adminStore.systemMetrics.systemHealth === 'warning',
                    'bg-red-100 text-red-800': adminStore.systemMetrics.systemHealth === 'critical'
                  }"
                >
                  {{ adminStore.systemMetrics.systemHealth }}
                </span>
              </div>

              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <Flag class="h-5 w-5 text-slate-400 mr-3" />
                  <span class="text-sm font-medium text-slate-900">Flagged Content</span>
                </div>
                <span class="text-sm text-slate-900">
                  {{ adminStore.systemMetrics.flaggedContent }}
                </span>
              </div>

              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <AlertCircle class="h-5 w-5 text-slate-400 mr-3" />
                  <span class="text-sm font-medium text-slate-900">Pending Reports</span>
                </div>
                <span class="text-sm text-slate-900">
                  {{ adminStore.systemMetrics.pendingReports }}
                </span>
              </div>
            </div>

            <div class="mt-6">
              <router-link
                to="/admin/reports"
                class="w-full flex justify-center items-center px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50"
              >
                View all reports
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAdminStore } from '@/stores/adminStore'
import {
  Users,
  FileText,
  Film,
  Activity,
  RefreshCw,
  AlertTriangle,
  Shield,
  Server,
  Database,
  Flag,
  AlertCircle,
  Settings,
  BarChart3,
  UserCheck,
  MessageSquare
} from 'lucide-vue-next'

const router = useRouter()
const adminStore = useAdminStore()

// Navigation items
const navigation = [
  { name: 'admin', label: 'Dashboard', to: '/admin', icon: Activity },
  { name: 'admin-users', label: 'Users', to: '/admin/users', icon: Users },
  { name: 'admin-moderation', label: 'Moderation', to: '/admin/moderation', icon: Shield },
  { name: 'admin-content', label: 'Content', to: '/admin/content', icon: Film },
  { name: 'admin-analytics', label: 'Analytics', to: '/admin/analytics', icon: BarChart3 },
  { name: 'admin-critics', label: 'Critics', to: '/admin/critics', icon: UserCheck },
  { name: 'admin-reports', label: 'Reports', to: '/admin/reports', icon: MessageSquare },
  { name: 'admin-settings', label: 'Settings', to: '/admin/settings', icon: Settings }
]

// Key metrics computed from store
const keyMetrics = [
  {
    name: 'Total Users',
    value: adminStore.systemMetrics.totalUsers.toLocaleString(),
    change: 12.5,
    icon: Users
  },
  {
    name: 'Total Reviews',
    value: adminStore.systemMetrics.totalReviews.toLocaleString(),
    change: 8.2,
    icon: FileText
  },
  {
    name: 'Active Users',
    value: adminStore.systemMetrics.activeUsers.toLocaleString(),
    change: 15.3,
    icon: Activity
  },
  {
    name: 'Total Movies',
    value: adminStore.systemMetrics.totalMovies.toLocaleString(),
    change: 5.1,
    icon: Film
  }
]

// Quick actions
const quickActions = [
  {
    name: 'Broadcast Message',
    description: 'Send a message to all users',
    icon: MessageSquare,
    iconBg: 'bg-blue-50',
    iconColor: 'text-blue-600',
    action: () => {
      // TODO: Implement broadcast message modal
      console.log('Broadcast message')
    }
  },
  {
    name: 'Export Data',
    description: 'Export platform data',
    icon: FileText,
    iconBg: 'bg-green-50',
    iconColor: 'text-green-600',
    action: () => {
      // TODO: Implement data export
      console.log('Export data')
    }
  },
  {
    name: 'System Maintenance',
    description: 'Put system in maintenance mode',
    icon: Settings,
    iconBg: 'bg-yellow-50',
    iconColor: 'text-yellow-600',
    action: () => {
      // TODO: Implement maintenance mode
      console.log('System maintenance')
    }
  },
  {
    name: 'View Analytics',
    description: 'Go to analytics dashboard',
    icon: BarChart3,
    iconBg: 'bg-purple-50',
    iconColor: 'text-purple-600',
    action: () => {
      router.push('/admin/analytics')
    }
  }
]

// Methods
const refreshData = async () => {
  await adminStore.fetchSystemMetrics()
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / (1000 * 60))
  
  if (diffInMinutes < 1) return 'Just now'
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`
  if (diffInMinutes < 1440) return `${Math.floor(diffInMinutes / 60)}h ago`
  return `${Math.floor(diffInMinutes / 1440)}d ago`
}

// Lifecycle
onMounted(() => {
  adminStore.fetchSystemMetrics()
})
</script>