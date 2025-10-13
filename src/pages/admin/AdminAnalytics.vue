<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-slate-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <div class="flex items-center">
            <router-link to="/admin" class="text-slate-500 hover:text-slate-700 mr-4">
              <ArrowLeft class="w-5 h-5" />
            </router-link>
            <h1 class="text-2xl font-bold text-slate-900">Analytics Dashboard</h1>
          </div>
          <div class="flex items-center space-x-4">
            <select
              v-model="selectedTimeRange"
              @change="updateTimeRange"
              class="px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
              <option value="1y">Last year</option>
            </select>
            <button
              @click="exportReport"
              class="inline-flex items-center px-3 py-2 border border-slate-300 shadow-sm text-sm leading-4 font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50"
            >
              <Download class="w-4 h-4 mr-2" />
              Export
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Key Metrics -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Users class="h-6 w-6 text-blue-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Total Users</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-semibold text-slate-900">{{ metrics.totalUsers }}</div>
                    <div class="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                      <TrendingUp class="h-4 w-4 mr-1" />
                      {{ metrics.userGrowth }}%
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <MessageSquare class="h-6 w-6 text-green-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Total Reviews</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-semibold text-slate-900">{{ metrics.totalReviews }}</div>
                    <div class="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                      <TrendingUp class="h-4 w-4 mr-1" />
                      {{ metrics.reviewGrowth }}%
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Eye class="h-6 w-6 text-purple-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Page Views</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-semibold text-slate-900">{{ formatNumber(metrics.pageViews) }}</div>
                    <div class="ml-2 flex items-baseline text-sm font-semibold text-blue-600">
                      <TrendingUp class="h-4 w-4 mr-1" />
                      {{ metrics.pageViewGrowth }}%
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Activity class="h-6 w-6 text-orange-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Engagement Rate</dt>
                  <dd class="flex items-baseline">
                    <div class="text-2xl font-semibold text-slate-900">{{ metrics.engagementRate }}%</div>
                    <div class="ml-2 flex items-baseline text-sm font-semibold text-green-600">
                      <TrendingUp class="h-4 w-4 mr-1" />
                      {{ metrics.engagementGrowth }}%
                    </div>
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row 1 -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2 mb-8">
        <!-- User Growth Chart -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">User Growth</h3>
            <div class="h-64 flex items-center justify-center bg-slate-50 rounded-lg">
              <div class="text-center">
                <BarChart class="mx-auto h-12 w-12 text-slate-400 mb-2" />
                <p class="text-sm text-slate-500">User growth chart would be rendered here</p>
                <p class="text-xs text-slate-400 mt-1">Integration with chart library needed</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Review Activity Chart -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">Review Activity</h3>
            <div class="h-64 flex items-center justify-center bg-slate-50 rounded-lg">
              <div class="text-center">
                <LineChart class="mx-auto h-12 w-12 text-slate-400 mb-2" />
                <p class="text-sm text-slate-500">Review activity chart would be rendered here</p>
                <p class="text-xs text-slate-400 mt-1">Integration with chart library needed</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row 2 -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2 mb-8">
        <!-- Content Performance -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">Top Performing Content</h3>
            <div class="space-y-4">
              <div v-for="item in topContent" :key="item.id" class="flex items-center justify-between">
                <div class="flex items-center">
                  <img
                    :src="item.poster"
                    :alt="item.title"
                    class="h-12 w-8 object-cover rounded mr-3"
                  />
                  <div>
                    <p class="text-sm font-medium text-slate-900">{{ item.title }}</p>
                    <p class="text-xs text-slate-500">{{ item.type }} • {{ item.year }}</p>
                  </div>
                </div>
                <div class="text-right">
                  <p class="text-sm font-medium text-slate-900">{{ item.views }} views</p>
                  <p class="text-xs text-slate-500">{{ item.reviews }} reviews</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- User Demographics -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">User Demographics</h3>
            <div class="space-y-4">
              <div>
                <div class="flex justify-between text-sm">
                  <span class="text-slate-600">Age 18-24</span>
                  <span class="font-medium">32%</span>
                </div>
                <div class="mt-1 w-full bg-slate-200 rounded-full h-2">
                  <div class="bg-blue-600 h-2 rounded-full" style="width: 32%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm">
                  <span class="text-slate-600">Age 25-34</span>
                  <span class="font-medium">28%</span>
                </div>
                <div class="mt-1 w-full bg-slate-200 rounded-full h-2">
                  <div class="bg-green-600 h-2 rounded-full" style="width: 28%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm">
                  <span class="text-slate-600">Age 35-44</span>
                  <span class="font-medium">22%</span>
                </div>
                <div class="mt-1 w-full bg-slate-200 rounded-full h-2">
                  <div class="bg-purple-600 h-2 rounded-full" style="width: 22%"></div>
                </div>
              </div>
              <div>
                <div class="flex justify-between text-sm">
                  <span class="text-slate-600">Age 45+</span>
                  <span class="font-medium">18%</span>
                </div>
                <div class="mt-1 w-full bg-slate-200 rounded-full h-2">
                  <div class="bg-orange-600 h-2 rounded-full" style="width: 18%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Detailed Tables -->
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-2">
        <!-- Recent Activity -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">Recent Activity</h3>
            <div class="flow-root">
              <ul class="-mb-8">
                <li v-for="(activity, index) in recentActivity" :key="activity.id">
                  <div class="relative pb-8" :class="{ 'pb-0': index === recentActivity.length - 1 }">
                    <span
                      v-if="index !== recentActivity.length - 1"
                      class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-slate-200"
                    ></span>
                    <div class="relative flex space-x-3">
                      <div>
                        <span
                          class="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white"
                          :class="getActivityIconClass(activity.type)"
                        >
                          <component :is="getActivityIcon(activity.type)" class="h-4 w-4" />
                        </span>
                      </div>
                      <div class="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                        <div>
                          <p class="text-sm text-slate-500">
                            {{ activity.description }}
                          </p>
                        </div>
                        <div class="text-right text-sm whitespace-nowrap text-slate-500">
                          {{ formatTimeAgo(activity.timestamp) }}
                        </div>
                      </div>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <!-- System Health -->
        <div class="bg-white shadow rounded-lg">
          <div class="px-4 py-5 sm:p-6">
            <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">System Health</h3>
            <div class="space-y-4">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="h-3 w-3 bg-green-400 rounded-full mr-3"></div>
                  <span class="text-sm text-slate-600">API Response Time</span>
                </div>
                <span class="text-sm font-medium text-slate-900">125ms</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="h-3 w-3 bg-green-400 rounded-full mr-3"></div>
                  <span class="text-sm text-slate-600">Database Performance</span>
                </div>
                <span class="text-sm font-medium text-slate-900">98.5%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="h-3 w-3 bg-yellow-400 rounded-full mr-3"></div>
                  <span class="text-sm text-slate-600">Memory Usage</span>
                </div>
                <span class="text-sm font-medium text-slate-900">72%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <div class="h-3 w-3 bg-green-400 rounded-full mr-3"></div>
                  <span class="text-sm text-slate-600">Uptime</span>
                </div>
                <span class="text-sm font-medium text-slate-900">99.9%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import {
  ArrowLeft,
  Download,
  Users,
  MessageSquare,
  Eye,
  Activity,
  TrendingUp,
  BarChart,
  LineChart,
  UserPlus,
  Star,
  AlertTriangle
} from 'lucide-vue-next'

// State
const selectedTimeRange = ref('30d')

// Mock data
const metrics = ref({
  totalUsers: 12543,
  userGrowth: 12.5,
  totalReviews: 8921,
  reviewGrowth: 8.3,
  pageViews: 156789,
  pageViewGrowth: 15.2,
  engagementRate: 68.4,
  engagementGrowth: 5.7
})

const topContent = ref([
  {
    id: '1',
    title: 'The Dark Knight',
    type: 'Movie',
    year: 2008,
    views: 15420,
    reviews: 342,
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=dark%20knight%20movie%20poster&image_size=portrait_4_3'
  },
  {
    id: '2',
    title: 'Breaking Bad',
    type: 'Series',
    year: 2008,
    views: 12890,
    reviews: 298,
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=breaking%20bad%20tv%20series%20poster&image_size=portrait_4_3'
  },
  {
    id: '3',
    title: 'Inception',
    type: 'Movie',
    year: 2010,
    views: 11234,
    reviews: 256,
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=inception%20movie%20poster%20dream%20layers&image_size=portrait_4_3'
  }
])

const recentActivity = ref([
  {
    id: '1',
    type: 'user_signup',
    description: 'New user registered: john.doe@example.com',
    timestamp: '2024-01-15T10:30:00Z'
  },
  {
    id: '2',
    type: 'review_posted',
    description: 'New review posted for "The Dark Knight"',
    timestamp: '2024-01-15T10:15:00Z'
  },
  {
    id: '3',
    type: 'content_flagged',
    description: 'Content flagged for review: inappropriate language',
    timestamp: '2024-01-15T09:45:00Z'
  },
  {
    id: '4',
    type: 'user_signup',
    description: 'New user registered: jane.smith@example.com',
    timestamp: '2024-01-15T09:30:00Z'
  }
])

// Methods
const updateTimeRange = () => {
  // TODO: Fetch new data based on time range
  console.log('Time range changed to:', selectedTimeRange.value)
}

const exportReport = () => {
  // TODO: Implement report export
  console.log('Exporting analytics report')
}

const formatNumber = (num: number) => {
  return new Intl.NumberFormat().format(num)
}

const formatTimeAgo = (timestamp: string) => {
  const now = new Date()
  const time = new Date(timestamp)
  const diffInMinutes = Math.floor((now.getTime() - time.getTime()) / (1000 * 60))
  
  if (diffInMinutes < 60) {
    return `${diffInMinutes}m ago`
  } else if (diffInMinutes < 1440) {
    return `${Math.floor(diffInMinutes / 60)}h ago`
  } else {
    return `${Math.floor(diffInMinutes / 1440)}d ago`
  }
}

const getActivityIcon = (type: string) => {
  const icons = {
    user_signup: UserPlus,
    review_posted: Star,
    content_flagged: AlertTriangle
  }
  return icons[type as keyof typeof icons] || Activity
}

const getActivityIconClass = (type: string) => {
  const classes = {
    user_signup: 'bg-green-500 text-white',
    review_posted: 'bg-blue-500 text-white',
    content_flagged: 'bg-red-500 text-white'
  }
  return classes[type as keyof typeof classes] || 'bg-slate-500 text-white'
}

// Lifecycle
onMounted(() => {
  // Load analytics data
  console.log('Loading analytics data')
})
</script>