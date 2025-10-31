import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { adminService } from '@/services/adminService'
import type { 
  AdminDashboard, 
  SystemMetrics as APISystemMetrics, 
  UserAnalytics as APIUserAnalytics, 
  ContentAnalytics as APIContentAnalytics,
  UserListItem,
  ReviewModerationItem,
  ReportItem
} from '@/services/adminService'

// Types for admin functionality
export interface AdminUser {
  id: string
  email: string
  name: string
  role: 'super_admin' | 'admin' | 'moderator'
  created_at: string
  last_login?: string
  is_active: boolean
}

export interface AdminAction {
  id: string
  admin_id: string
  action_type: string
  action_data: Record<string, any>
  created_at: string
}

export interface ModerationLog {
  id: string
  moderator_id: string
  review_id: string
  action: 'approve' | 'reject' | 'flag' | 'unflag'
  reason?: string
  notes?: string
  created_at: string
}

export interface UserReport {
  id: string
  reporter_id: string
  reported_user_id?: string
  reported_content_id?: string
  report_type: 'user' | 'review' | 'comment'
  reason: string
  description?: string
  status: 'pending' | 'investigating' | 'resolved' | 'dismissed'
  created_at: string
  resolved_at?: string
}

export interface ContentChange {
  id: string
  movie_id: string
  admin_id: string
  change_type: 'create' | 'update' | 'delete'
  old_data?: Record<string, any>
  new_data?: Record<string, any>
  created_at: string
}

export interface SystemMetrics {
  totalUsers: number
  totalReviews: number
  totalMovies: number
  activeUsers: number
  flaggedContent: number
  pendingReports: number
  systemHealth: 'healthy' | 'warning' | 'critical'
  serverStatus: 'online' | 'offline' | 'maintenance'
}

export interface UserAnalytics {
  newUsersToday: number
  newUsersThisWeek: number
  newUsersThisMonth: number
  activeUsersToday: number
  activeUsersThisWeek: number
  activeUsersThisMonth: number
  userRetentionRate: number
  averageSessionDuration: number
}

export interface ContentAnalytics {
  reviewsToday: number
  reviewsThisWeek: number
  reviewsThisMonth: number
  averageRating: number
  mostReviewedMovies: Array<{ id: string; title: string; reviewCount: number }>
  topRatedMovies: Array<{ id: string; title: string; rating: number }>
}

export const useAdminStore = defineStore('admin', () => {
  // State
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const systemMetrics = ref<SystemMetrics>({
    totalUsers: 0,
    totalReviews: 0,
    totalMovies: 0,
    activeUsers: 0,
    flaggedContent: 0,
    pendingReports: 0,
    systemHealth: 'healthy',
    serverStatus: 'online'
  })
  
  const users = ref<UserListItem[]>([])
  const adminUsers = ref<AdminUser[]>([])
  const moderationLogs = ref<ModerationLog[]>([])
  const userReports = ref<ReportItem[]>([])
  const contentChanges = ref<ContentChange[]>([])
  const userAnalytics = ref<UserAnalytics>({
    newUsersToday: 0,
    newUsersThisWeek: 0,
    newUsersThisMonth: 0,
    activeUsersToday: 0,
    activeUsersThisWeek: 0,
    activeUsersThisMonth: 0,
    userRetentionRate: 0,
    averageSessionDuration: 0
  })
  const contentAnalytics = ref<ContentAnalytics>({
    reviewsToday: 0,
    reviewsThisWeek: 0,
    reviewsThisMonth: 0,
    averageRating: 0,
    mostReviewedMovies: [],
    topRatedMovies: []
  })
  const recentActions = ref<any[]>([])

  // Computed
  const pendingReports = computed(() => 
    userReports.value.filter(report => report.status === 'pending')
  )

  const flaggedReviews = computed(() => 
    moderationLogs.value.filter(log => log.action === 'flag')
  )
  // Actions
  const fetchSystemMetrics = async () => {
    isLoading.value = true
    error.value = null
    try {
      const dashboardData = await adminService.getDashboard()
      
      // Update system metrics
      systemMetrics.value = {
        totalUsers: dashboardData.system_metrics.total_users,
        totalReviews: dashboardData.system_metrics.total_reviews,
        totalMovies: dashboardData.system_metrics.total_movies,
        activeUsers: dashboardData.system_metrics.active_users_today,
        flaggedContent: dashboardData.system_metrics.flagged_reviews,
        pendingReports: dashboardData.system_metrics.pending_reports,
        systemHealth: 'healthy', // Default since API doesn't provide this
        serverStatus: 'online' // Default since API doesn't provide this
      }
      
      // Update analytics
      userAnalytics.value = {
        newUsersToday: dashboardData.system_metrics.new_users_today,
        newUsersThisWeek: dashboardData.system_metrics.new_users_week,
        newUsersThisMonth: dashboardData.system_metrics.new_users_month,
        activeUsersToday: dashboardData.system_metrics.active_users_today,
        activeUsersThisWeek: dashboardData.system_metrics.active_users_week,
        activeUsersThisMonth: dashboardData.system_metrics.active_users_month,
        userRetentionRate: dashboardData.user_analytics.user_retention?.weekly_retention || 0,
        averageSessionDuration: 0 // Not provided by API
      }
      
      contentAnalytics.value = {
        reviewsToday: dashboardData.system_metrics.reviews_today,
        reviewsThisWeek: dashboardData.system_metrics.reviews_week,
        reviewsThisMonth: dashboardData.system_metrics.reviews_month,
        averageRating: 0, // Not provided by API
        mostReviewedMovies: dashboardData.content_analytics.popular_movies?.map(movie => ({
          id: movie.id,
          title: movie.title,
          reviewCount: movie.review_count
        })) || [],
        topRatedMovies: dashboardData.content_analytics.popular_movies?.map(movie => ({
          id: movie.id,
          title: movie.title,
          rating: movie.avg_rating
        })) || []
      }
      
      // Update recent activity
      recentActions.value = dashboardData.recent_activity
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch system metrics'
      console.error('Failed to fetch system metrics:', err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchUsers = async (page = 1, limit = 10, search = '', role = '') => {
    isLoading.value = true
    error.value = null
    try {
      const response = await adminService.getUsersList(page, limit, search, role)
      users.value = response.users
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch users'
      console.error('Failed to fetch users:', err)
    } finally {
      isLoading.value = false
    }
  }

  const updateUserRole = async (userId: string, newRole: string) => {
    isLoading.value = true
    error.value = null
    try {
      await adminService.updateUserRole(userId, newRole)
      
      // Update user role in local state
      const userIndex = users.value.findIndex(user => user.id === userId)
      if (userIndex !== -1) {
        users.value[userIndex].role = newRole
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to update user role'
      console.error('Failed to update user role:', err)
    } finally {
      isLoading.value = false
    }
  }

  const suspendUser = async (userId: string) => {
    isLoading.value = true
    error.value = null
    try {
      await adminService.suspendUser(userId)
      
      // Update user status in local state
      const userIndex = users.value.findIndex(user => user.id === userId)
      if (userIndex !== -1) {
        users.value[userIndex].status = 'suspended'
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to suspend user'
      console.error('Failed to suspend user:', err)
    } finally {
      isLoading.value = false
    }
  }

  const activateUser = async (userId: string) => {
    isLoading.value = true
    error.value = null
    try {
      await adminService.activateUser(userId)
      
      // Update user status in local state
      const userIndex = users.value.findIndex(user => user.id === userId)
      if (userIndex !== -1) {
        users.value[userIndex].status = 'active'
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to activate user'
      console.error('Failed to activate user:', err)
    } finally {
      isLoading.value = false
    }
  }

  const moderateContent = async (reviewId: string, action: 'approve' | 'reject', reason?: string) => {
    isLoading.value = true
    error.value = null
    try {
      await adminService.moderateReview(reviewId, action, reason)
      
      // Add moderation log
      const newLog: ModerationLog = {
        id: Date.now().toString(),
        moderator_id: 'current_admin',
        review_id: reviewId,
        action,
        reason: reason || '',
        notes: '',
        created_at: new Date().toISOString()
      }
      
      moderationLogs.value.unshift(newLog)
    } catch (err: any) {
      error.value = err.message || 'Failed to moderate content'
      console.error('Failed to moderate content:', err)
    } finally {
      isLoading.value = false
    }
  }

  const resolveReport = async (reportId: string, resolution: string) => {
    isLoading.value = true
    error.value = null
    try {
      await adminService.resolveReport(reportId, resolution)
      
      // Update report status
      const reportIndex = userReports.value.findIndex(report => report.id === reportId)
      if (reportIndex !== -1) {
        userReports.value[reportIndex].status = 'resolved'
      }
    } catch (err: any) {
      error.value = err.message || 'Failed to resolve report'
      console.error('Failed to resolve report:', err)
    } finally {
      isLoading.value = false
    }
  }

  const fetchReports = async (page = 1, limit = 10, status = '') => {
    isLoading.value = true
    error.value = null
    try {
      const response = await adminService.getReportsList(page, limit, status)
      userReports.value = response.reports
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch reports'
      console.error('Failed to fetch reports:', err)
    } finally {
      isLoading.value = false
    }
  }



  return {
    // State
    isLoading,
    error,
    systemMetrics,
    users,
    adminUsers,
    moderationLogs,
    userReports,
    contentChanges,
    userAnalytics,
    contentAnalytics,
    
    // Computed
    pendingReports,
    flaggedReviews,
    recentActions,
    
    // Actions
    fetchSystemMetrics,
    fetchUsers,
    updateUserRole,
    suspendUser,
    activateUser,
    moderateContent,
    resolveReport,
    fetchReports
  }
})