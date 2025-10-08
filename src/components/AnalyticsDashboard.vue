<template>
  <div class="analytics-dashboard">
    <div class="dashboard-header">
      <h2 class="dashboard-title">Analytics Dashboard</h2>
      <div class="date-range-selector">
        <select v-model="selectedPeriod" class="period-select">
          <option value="7d">Last 7 days</option>
          <option value="30d">Last 30 days</option>
          <option value="90d">Last 90 days</option>
          <option value="1y">Last year</option>
        </select>
      </div>
    </div>

    <!-- Key Metrics Overview -->
    <div class="metrics-overview">
      <div class="metric-card">
        <div class="metric-icon users">
          <Users class="icon" />
        </div>
        <div class="metric-content">
          <span class="metric-value">{{ formatNumber(analytics.totalUsers) }}</span>
          <span class="metric-label">Total Users</span>
          <span class="metric-change" :class="analytics.userGrowth >= 0 ? 'positive' : 'negative'">
            {{ analytics.userGrowth >= 0 ? '+' : '' }}{{ analytics.userGrowth }}%
          </span>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon reviews">
          <MessageSquare class="icon" />
        </div>
        <div class="metric-content">
          <span class="metric-value">{{ formatNumber(analytics.totalReviews) }}</span>
          <span class="metric-label">Total Reviews</span>
          <span class="metric-change" :class="analytics.reviewGrowth >= 0 ? 'positive' : 'negative'">
            {{ analytics.reviewGrowth >= 0 ? '+' : '' }}{{ analytics.reviewGrowth }}%
          </span>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon engagement">
          <Activity class="icon" />
        </div>
        <div class="metric-content">
          <span class="metric-value">{{ analytics.avgEngagement }}%</span>
          <span class="metric-label">Engagement Rate</span>
          <span class="metric-change" :class="analytics.engagementChange >= 0 ? 'positive' : 'negative'">
            {{ analytics.engagementChange >= 0 ? '+' : '' }}{{ analytics.engagementChange }}%
          </span>
        </div>
      </div>

      <div class="metric-card">
        <div class="metric-icon revenue">
          <TrendingUp class="icon" />
        </div>
        <div class="metric-content">
          <span class="metric-value">{{ formatNumber(analytics.avgRating, 1) }}</span>
          <span class="metric-label">Avg Rating</span>
          <span class="metric-change" :class="analytics.ratingChange >= 0 ? 'positive' : 'negative'">
            {{ analytics.ratingChange >= 0 ? '+' : '' }}{{ analytics.ratingChange.toFixed(1) }}
          </span>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div class="charts-section">
      <!-- User Growth Chart -->
      <div class="chart-container">
        <div class="chart-header">
          <h3 class="chart-title">User Growth</h3>
          <div class="chart-legend">
            <div class="legend-item">
              <span class="legend-color new-users"></span>
              <span>New Users</span>
            </div>
            <div class="legend-item">
              <span class="legend-color active-users"></span>
              <span>Active Users</span>
            </div>
          </div>
        </div>
        <div class="chart-content">
          <div class="chart-placeholder">
            <div class="chart-bars">
              <div 
                v-for="(data, index) in userGrowthData" 
                :key="index"
                class="bar-group"
              >
                <div class="bar new-users" :style="{ height: `${(data.newUsers / maxUsers) * 100}%` }"></div>
                <div class="bar active-users" :style="{ height: `${(data.activeUsers / maxUsers) * 100}%` }"></div>
                <span class="bar-label">{{ data.date }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Review Analytics Chart -->
      <div class="chart-container">
        <div class="chart-header">
          <h3 class="chart-title">Review Analytics</h3>
          <div class="chart-legend">
            <div class="legend-item">
              <span class="legend-color reviews"></span>
              <span>Reviews</span>
            </div>
            <div class="legend-item">
              <span class="legend-color avg-rating"></span>
              <span>Avg Rating</span>
            </div>
          </div>
        </div>
        <div class="chart-content">
          <div class="chart-placeholder">
            <div class="line-chart">
              <svg viewBox="0 0 400 200" class="chart-svg">
                <!-- Grid lines -->
                <defs>
                  <pattern id="grid" width="40" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 20" fill="none" stroke="var(--border-color)" stroke-width="0.5"/>
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />
                
                <!-- Review count line -->
                <polyline 
                  :points="reviewLinePoints" 
                  fill="none" 
                  stroke="var(--accent-color)" 
                  stroke-width="2"
                />
                
                <!-- Rating line -->
                <polyline 
                  :points="ratingLinePoints" 
                  fill="none" 
                  stroke="#10b981" 
                  stroke-width="2"
                />
                
                <!-- Data points -->
                <circle 
                  v-for="(point, index) in reviewDataPoints" 
                  :key="`review-${index}`"
                  :cx="point.x" 
                  :cy="point.y" 
                  r="3" 
                  fill="var(--accent-color)"
                />
                <circle 
                  v-for="(point, index) in ratingDataPoints" 
                  :key="`rating-${index}`"
                  :cx="point.x" 
                  :cy="point.y" 
                  r="3" 
                  fill="#10b981"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Analytics -->
    <div class="detailed-analytics">
      <!-- Top Movies -->
      <div class="analytics-card">
        <h3 class="card-title">Top Reviewed Movies</h3>
        <div class="top-movies-list">
          <div 
            v-for="movie in topMovies" 
            :key="movie.id"
            class="movie-item"
          >
            <img :src="movie.poster" :alt="movie.title" class="movie-poster" />
            <div class="movie-info">
              <span class="movie-title">{{ movie.title }}</span>
              <span class="movie-stats">{{ movie.reviewCount }} reviews • {{ movie.avgRating }}/10</span>
            </div>
            <div class="movie-metrics">
              <span class="metric-badge">{{ movie.reviewCount }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- User Demographics -->
      <div class="analytics-card">
        <h3 class="card-title">User Demographics</h3>
        <div class="demographics-chart">
          <div class="demo-section">
            <h4 class="demo-title">By Location</h4>
            <div class="demo-bars">
              <div 
                v-for="location in userDemographics.locations" 
                :key="location.name"
                class="demo-bar"
              >
                <span class="demo-label">{{ location.name }}</span>
                <div class="demo-progress">
                  <div 
                    class="demo-fill" 
                    :style="{ width: `${location.percentage}%` }"
                  ></div>
                </div>
                <span class="demo-value">{{ location.percentage }}%</span>
              </div>
            </div>
          </div>
          
          <div class="demo-section">
            <h4 class="demo-title">By Age Group</h4>
            <div class="demo-bars">
              <div 
                v-for="age in userDemographics.ageGroups" 
                :key="age.range"
                class="demo-bar"
              >
                <span class="demo-label">{{ age.range }}</span>
                <div class="demo-progress">
                  <div 
                    class="demo-fill" 
                    :style="{ width: `${age.percentage}%` }"
                  ></div>
                </div>
                <span class="demo-value">{{ age.percentage }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Platform Usage -->
      <div class="analytics-card">
        <h3 class="card-title">Platform Usage</h3>
        <div class="usage-stats">
          <div class="usage-metric">
            <span class="usage-label">Daily Active Users</span>
            <span class="usage-value">{{ formatNumber(platformUsage.dailyActiveUsers) }}</span>
            <span class="usage-change positive">+{{ platformUsage.dauChange }}%</span>
          </div>
          
          <div class="usage-metric">
            <span class="usage-label">Avg Session Duration</span>
            <span class="usage-value">{{ platformUsage.avgSessionDuration }}m</span>
            <span class="usage-change positive">+{{ platformUsage.sessionChange }}%</span>
          </div>
          
          <div class="usage-metric">
            <span class="usage-label">Page Views</span>
            <span class="usage-value">{{ formatNumber(platformUsage.pageViews) }}</span>
            <span class="usage-change positive">+{{ platformUsage.pageViewChange }}%</span>
          </div>
          
          <div class="usage-metric">
            <span class="usage-label">Bounce Rate</span>
            <span class="usage-value">{{ platformUsage.bounceRate }}%</span>
            <span class="usage-change negative">{{ platformUsage.bounceRateChange }}%</span>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="analytics-card">
        <h3 class="card-title">Recent Activity</h3>
        <div class="activity-feed">
          <div 
            v-for="activity in recentActivity" 
            :key="activity.id"
            class="activity-item"
          >
            <div class="activity-icon" :class="activity.type">
              <component :is="getActivityIcon(activity.type)" class="icon" />
            </div>
            <div class="activity-content">
              <span class="activity-text">{{ activity.description }}</span>
              <span class="activity-time">{{ formatTime(activity.timestamp) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Export Options -->
    <div class="export-section">
      <h3 class="export-title">Export Data</h3>
      <div class="export-options">
        <button class="export-btn" @click="exportData('csv')">
          <Download class="icon" />
          Export CSV
        </button>
        <button class="export-btn" @click="exportData('pdf')">
          <FileText class="icon" />
          Export PDF
        </button>
        <button class="export-btn" @click="exportData('json')">
          <Code class="icon" />
          Export JSON
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  Users, 
  MessageSquare, 
  Activity, 
  TrendingUp, 
  Download, 
  FileText, 
  Code,
  UserPlus,
  Star,
  Eye,
  Heart
} from 'lucide-vue-next'
import { useUIStore } from '@/stores/uiStore'

interface Analytics {
  totalUsers: number
  userGrowth: number
  totalReviews: number
  reviewGrowth: number
  avgEngagement: number
  engagementChange: number
  avgRating: number
  ratingChange: number
}

interface UserGrowthData {
  date: string
  newUsers: number
  activeUsers: number
}

interface ReviewData {
  date: string
  reviews: number
  avgRating: number
}

interface TopMovie {
  id: string
  title: string
  poster: string
  reviewCount: number
  avgRating: number
}

interface UserDemographics {
  locations: Array<{ name: string; percentage: number }>
  ageGroups: Array<{ range: string; percentage: number }>
}

interface PlatformUsage {
  dailyActiveUsers: number
  dauChange: number
  avgSessionDuration: number
  sessionChange: number
  pageViews: number
  pageViewChange: number
  bounceRate: number
  bounceRateChange: number
}

interface RecentActivity {
  id: string
  type: 'user' | 'review' | 'like' | 'view'
  description: string
  timestamp: string
}

const uiStore = useUIStore()

const selectedPeriod = ref('30d')

// Mock analytics data
const analytics = ref<Analytics>({
  totalUsers: 12547,
  userGrowth: 15.3,
  totalReviews: 8934,
  reviewGrowth: 23.7,
  avgEngagement: 68.4,
  engagementChange: 5.2,
  avgRating: 7.2,
  ratingChange: 0.3
})

const userGrowthData = ref<UserGrowthData[]>([
  { date: 'Jan 1', newUsers: 120, activeUsers: 890 },
  { date: 'Jan 8', newUsers: 145, activeUsers: 920 },
  { date: 'Jan 15', newUsers: 167, activeUsers: 1050 },
  { date: 'Jan 22', newUsers: 189, activeUsers: 1120 },
  { date: 'Jan 29', newUsers: 203, activeUsers: 1180 },
  { date: 'Feb 5', newUsers: 234, activeUsers: 1250 },
  { date: 'Feb 12', newUsers: 256, activeUsers: 1320 }
])

const reviewData = ref<ReviewData[]>([
  { date: 'Jan 1', reviews: 45, avgRating: 6.8 },
  { date: 'Jan 8', reviews: 52, avgRating: 7.1 },
  { date: 'Jan 15', reviews: 67, avgRating: 7.0 },
  { date: 'Jan 22', reviews: 78, avgRating: 7.3 },
  { date: 'Jan 29', reviews: 89, avgRating: 7.2 },
  { date: 'Feb 5', reviews: 95, avgRating: 7.4 },
  { date: 'Feb 12', reviews: 103, avgRating: 7.2 }
])

const topMovies = ref<TopMovie[]>([
  {
    id: '1',
    title: 'The Wedding Party',
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20wedding%20comedy%20movie%20poster&image_size=portrait_4_3',
    reviewCount: 234,
    avgRating: 8.2
  },
  {
    id: '2',
    title: 'King of Boys',
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20crime%20thriller%20movie%20poster&image_size=portrait_4_3',
    reviewCount: 189,
    avgRating: 8.7
  },
  {
    id: '3',
    title: 'Lionheart',
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20drama%20movie%20poster&image_size=portrait_4_3',
    reviewCount: 156,
    avgRating: 7.9
  },
  {
    id: '4',
    title: 'Chief Daddy',
    poster: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20family%20comedy%20movie%20poster&image_size=portrait_4_3',
    reviewCount: 143,
    avgRating: 7.6
  }
])

const userDemographics = ref<UserDemographics>({
  locations: [
    { name: 'Lagos', percentage: 35 },
    { name: 'Abuja', percentage: 18 },
    { name: 'Kano', percentage: 12 },
    { name: 'Port Harcourt', percentage: 10 },
    { name: 'Ibadan', percentage: 8 },
    { name: 'Others', percentage: 17 }
  ],
  ageGroups: [
    { range: '18-24', percentage: 28 },
    { range: '25-34', percentage: 42 },
    { range: '35-44', percentage: 20 },
    { range: '45-54', percentage: 8 },
    { range: '55+', percentage: 2 }
  ]
})

const platformUsage = ref<PlatformUsage>({
  dailyActiveUsers: 3247,
  dauChange: 12.5,
  avgSessionDuration: 18,
  sessionChange: 8.3,
  pageViews: 45678,
  pageViewChange: 15.7,
  bounceRate: 32,
  bounceRateChange: -4.2
})

const recentActivity = ref<RecentActivity[]>([
  {
    id: '1',
    type: 'user',
    description: 'New user registration from Lagos',
    timestamp: '2024-01-15T10:30:00Z'
  },
  {
    id: '2',
    type: 'review',
    description: 'New review posted for "King of Boys"',
    timestamp: '2024-01-15T10:25:00Z'
  },
  {
    id: '3',
    type: 'like',
    description: 'Review received 50+ likes',
    timestamp: '2024-01-15T10:20:00Z'
  },
  {
    id: '4',
    type: 'view',
    description: 'Movie page viewed 1000+ times today',
    timestamp: '2024-01-15T10:15:00Z'
  }
])

const maxUsers = computed(() => {
  const allUsers = userGrowthData.value.flatMap(d => [d.newUsers, d.activeUsers])
  return Math.max(...allUsers)
})

const reviewLinePoints = computed(() => {
  return reviewData.value.map((data, index) => {
    const x = (index / (reviewData.value.length - 1)) * 380 + 10
    const y = 180 - (data.reviews / 120) * 160
    return `${x},${y}`
  }).join(' ')
})

const ratingLinePoints = computed(() => {
  return reviewData.value.map((data, index) => {
    const x = (index / (reviewData.value.length - 1)) * 380 + 10
    const y = 180 - ((data.avgRating - 6) / 4) * 160
    return `${x},${y}`
  }).join(' ')
})

const reviewDataPoints = computed(() => {
  return reviewData.value.map((data, index) => ({
    x: (index / (reviewData.value.length - 1)) * 380 + 10,
    y: 180 - (data.reviews / 120) * 160
  }))
})

const ratingDataPoints = computed(() => {
  return reviewData.value.map((data, index) => ({
    x: (index / (reviewData.value.length - 1)) * 380 + 10,
    y: 180 - ((data.avgRating - 6) / 4) * 160
  }))
})

const formatNumber = (num: number, decimals = 0) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(decimals) + 'M'
  } else if (num >= 1000) {
    return (num / 1000).toFixed(decimals) + 'K'
  }
  return num.toFixed(decimals)
}

const formatTime = (timestamp: string) => {
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const minutes = Math.floor(diff / 60000)
  
  if (minutes < 60) {
    return `${minutes}m ago`
  } else if (minutes < 1440) {
    return `${Math.floor(minutes / 60)}h ago`
  } else {
    return `${Math.floor(minutes / 1440)}d ago`
  }
}

const getActivityIcon = (type: string) => {
  switch (type) {
    case 'user': return UserPlus
    case 'review': return MessageSquare
    case 'like': return Heart
    case 'view': return Eye
    default: return Activity
  }
}

const exportData = (format: 'csv' | 'pdf' | 'json') => {
  // Implementation for data export
  uiStore.showToast({ message: `Exporting data as ${format.toUpperCase()}...`, type: 'info' })
  
  // Simulate export process
  setTimeout(() => {
    uiStore.showToast({ message: `Data exported successfully as ${format.toUpperCase()}`, type: 'success' })
  }, 2000)
}

onMounted(() => {
  // Load analytics data
})
</script>

<style scoped>
.analytics-dashboard {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.dashboard-title {
  font-size: 2rem;
  font-weight: bold;
  color: var(--text-primary);
}

.period-select {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: var(--text-primary);
  cursor: pointer;
}

.metrics-overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.metric-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.metric-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.metric-icon.users {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
}

.metric-icon.reviews {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.metric-icon.engagement {
  background: linear-gradient(135deg, #10b981, #059669);
}

.metric-icon.revenue {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.metric-icon .icon {
  width: 24px;
  height: 24px;
  color: white;
}

.metric-content {
  display: flex;
  flex-direction: column;
}

.metric-value {
  font-size: 2rem;
  font-weight: bold;
  color: var(--text-primary);
  line-height: 1;
}

.metric-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0.25rem 0;
}

.metric-change {
  font-size: 0.875rem;
  font-weight: 600;
}

.metric-change.positive {
  color: #10b981;
}

.metric-change.negative {
  color: #ef4444;
}

.charts-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.chart-container {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.chart-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.chart-legend {
  display: flex;
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.legend-color.new-users {
  background: var(--accent-color);
}

.legend-color.active-users {
  background: #3b82f6;
}

.legend-color.reviews {
  background: var(--accent-color);
}

.legend-color.avg-rating {
  background: #10b981;
}

.chart-content {
  height: 200px;
}

.chart-placeholder {
  width: 100%;
  height: 100%;
  position: relative;
}

.chart-bars {
  display: flex;
  align-items: end;
  justify-content: space-between;
  height: 100%;
  padding: 1rem 0;
}

.bar-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
  flex: 1;
  max-width: 60px;
}

.bar {
  width: 20px;
  border-radius: 2px 2px 0 0;
  margin: 0 1px;
  min-height: 4px;
}

.bar.new-users {
  background: var(--accent-color);
}

.bar.active-users {
  background: #3b82f6;
}

.bar-label {
  font-size: 0.75rem;
  color: var(--text-secondary);
  margin-top: 0.5rem;
}

.line-chart {
  width: 100%;
  height: 100%;
}

.chart-svg {
  width: 100%;
  height: 100%;
}

.detailed-analytics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.analytics-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.top-movies-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.movie-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem;
  background: var(--bg-tertiary);
  border-radius: 8px;
}

.movie-poster {
  width: 50px;
  height: 75px;
  object-fit: cover;
  border-radius: 6px;
}

.movie-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.movie-title {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.movie-stats {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.movie-metrics {
  display: flex;
  align-items: center;
}

.metric-badge {
  background: var(--accent-color);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.875rem;
  font-weight: 600;
}

.demographics-chart {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.demo-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.demo-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.demo-bars {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.demo-bar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.demo-label {
  min-width: 80px;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.demo-progress {
  flex: 1;
  height: 8px;
  background: var(--bg-tertiary);
  border-radius: 4px;
  overflow: hidden;
}

.demo-fill {
  height: 100%;
  background: var(--accent-color);
  transition: width 0.3s ease;
}

.demo-value {
  min-width: 40px;
  text-align: right;
  font-size: 0.875rem;
  color: var(--text-primary);
  font-weight: 600;
}

.usage-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.usage-metric {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: 8px;
}

.usage-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.usage-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--text-primary);
}

.usage-change {
  font-size: 0.875rem;
  font-weight: 600;
}

.usage-change.positive {
  color: #10b981;
}

.usage-change.negative {
  color: #ef4444;
}

.activity-feed {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-height: 300px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  background: var(--bg-tertiary);
  border-radius: 8px;
}

.activity-icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.activity-icon.user {
  background: #dbeafe;
  color: #3b82f6;
}

.activity-icon.review {
  background: #fef3c7;
  color: #f59e0b;
}

.activity-icon.like {
  background: #fecaca;
  color: #ef4444;
}

.activity-icon.view {
  background: #d1fae5;
  color: #10b981;
}

.activity-icon .icon {
  width: 16px;
  height: 16px;
}

.activity-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.activity-text {
  color: var(--text-primary);
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.activity-time {
  color: var(--text-secondary);
  font-size: 0.75rem;
}

.export-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
}

.export-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.export-options {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
}

.export-btn:hover {
  background: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.export-btn .icon {
  width: 16px;
  height: 16px;
}

@media (max-width: 1024px) {
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .detailed-analytics {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .analytics-dashboard {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .metrics-overview {
    grid-template-columns: 1fr;
  }
  
  .metric-card {
    flex-direction: column;
    text-align: center;
  }
  
  .usage-stats {
    grid-template-columns: 1fr;
  }
  
  .export-options {
    flex-direction: column;
  }
  
  .export-btn {
    justify-content: center;
  }
}
</style>