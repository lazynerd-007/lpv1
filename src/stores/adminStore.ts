import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

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
  
  const users = ref<any[]>([])
  const adminUsers = ref<AdminUser[]>([])
  const moderationLogs = ref<ModerationLog[]>([])
  const userReports = ref<UserReport[]>([])
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

  // Computed
  const pendingReports = computed(() => 
    userReports.value.filter(report => report.status === 'pending')
  )

  const flaggedReviews = computed(() => 
    moderationLogs.value.filter(log => log.action === 'flag')
  )

  const recentActions = computed(() => 
    moderationLogs.value
      .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      .slice(0, 10)
  )

  // Mock data for development
  const initializeMockData = () => {
    // Mock system metrics
    systemMetrics.value = {
      totalUsers: 1247,
      totalReviews: 3892,
      totalMovies: 456,
      activeUsers: 89,
      flaggedContent: 12,
      pendingReports: 5,
      systemHealth: 'healthy',
      serverStatus: 'online'
    }

    // Mock user analytics
    userAnalytics.value = {
      newUsersToday: 23,
      newUsersThisWeek: 156,
      newUsersThisMonth: 678,
      activeUsersToday: 89,
      activeUsersThisWeek: 445,
      activeUsersThisMonth: 1247,
      userRetentionRate: 78.5,
      averageSessionDuration: 24.5
    }

    // Mock content analytics
    contentAnalytics.value = {
      reviewsToday: 45,
      reviewsThisWeek: 289,
      reviewsThisMonth: 1234,
      averageRating: 4.2,
      mostReviewedMovies: [
        { id: '1', title: 'The Wedding Party', reviewCount: 234 },
        { id: '2', title: 'King of Boys', reviewCount: 189 },
        { id: '3', title: 'Lionheart', reviewCount: 156 }
      ],
      topRatedMovies: [
        { id: '4', title: 'October 1', rating: 4.8 },
        { id: '5', title: 'Half of a Yellow Sun', rating: 4.7 },
        { id: '6', title: 'The Figurine', rating: 4.6 }
      ]
    }

    // Mock user reports
    userReports.value = [
      {
        id: '1',
        reporter_id: 'user1',
        reported_content_id: 'review1',
        report_type: 'review',
        reason: 'Inappropriate content',
        description: 'Contains offensive language',
        status: 'pending',
        created_at: new Date().toISOString()
      },
      {
        id: '2',
        reporter_id: 'user2',
        reported_user_id: 'user3',
        report_type: 'user',
        reason: 'Spam',
        description: 'User is posting spam reviews',
        status: 'investigating',
        created_at: new Date(Date.now() - 86400000).toISOString()
      }
    ]

    // Mock moderation logs
    moderationLogs.value = [
      {
        id: '1',
        moderator_id: 'admin1',
        review_id: 'review1',
        action: 'flag',
        reason: 'Inappropriate content',
        notes: 'Flagged for review',
        created_at: new Date().toISOString()
      }
    ]
  }

  // Actions
  const fetchSystemMetrics = async () => {
    isLoading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      initializeMockData()
    } catch (err) {
      error.value = 'Failed to fetch system metrics'
    } finally {
      isLoading.value = false
    }
  }

  const fetchUsers = async (filters?: { search?: string; role?: string; status?: string }) => {
    isLoading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // Mock users data
      const mockUsers = [
        {
          id: '1',
          name: 'Adebayo Johnson',
          email: 'adebayo@example.com',
          role: 'user',
          status: 'active',
          joinDate: '2023-01-15',
          lastLogin: '2024-01-15',
          reviewCount: 23,
          avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20man%20profile%20picture%20professional%20headshot&image_size=square'
        },
        {
          id: '2',
          name: 'Funmi Adebayo',
          email: 'funmi@example.com',
          role: 'critic',
          status: 'active',
          joinDate: '2023-02-20',
          lastLogin: '2024-01-14',
          reviewCount: 67,
          avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20woman%20profile%20picture%20professional%20headshot&image_size=square'
        },
        {
          id: '3',
          name: 'Chidi Okafor',
          email: 'chidi@example.com',
          role: 'moderator',
          status: 'active',
          joinDate: '2023-03-10',
          lastLogin: '2024-01-13',
          reviewCount: 12,
          avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20man%20profile%20picture%20professional%20headshot&image_size=square'
        }
      ]

      // Apply filters if provided
      let filteredUsers = mockUsers
      if (filters?.search) {
        const searchTerm = filters.search.toLowerCase()
        filteredUsers = filteredUsers.filter(user => 
          user.name.toLowerCase().includes(searchTerm) || 
          user.email.toLowerCase().includes(searchTerm)
        )
      }
      if (filters?.role) {
        filteredUsers = filteredUsers.filter(user => user.role === filters.role)
      }
      if (filters?.status) {
        filteredUsers = filteredUsers.filter(user => user.status === filters.status)
      }

      users.value = filteredUsers
    } catch (err) {
      error.value = 'Failed to fetch users'
    } finally {
      isLoading.value = false
    }
  }

  const updateUserRole = async (userId: string, newRole: string) => {
    isLoading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const userIndex = users.value.findIndex(user => user.id === userId)
      if (userIndex !== -1) {
        users.value[userIndex].role = newRole
      }
    } catch (err) {
      error.value = 'Failed to update user role'
    } finally {
      isLoading.value = false
    }
  }

  const suspendUser = async (userId: string, reason: string) => {
    isLoading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const userIndex = users.value.findIndex(user => user.id === userId)
      if (userIndex !== -1) {
        users.value[userIndex].status = 'suspended'
      }
    } catch (err) {
      error.value = 'Failed to suspend user'
    } finally {
      isLoading.value = false
    }
  }

  const moderateContent = async (reviewId: string, action: string, reason?: string, notes?: string) => {
    isLoading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const newLog: ModerationLog = {
        id: Date.now().toString(),
        moderator_id: 'current-admin',
        review_id: reviewId,
        action: action as any,
        reason,
        notes,
        created_at: new Date().toISOString()
      }
      
      moderationLogs.value.unshift(newLog)
    } catch (err) {
      error.value = 'Failed to moderate content'
    } finally {
      isLoading.value = false
    }
  }

  const resolveReport = async (reportId: string, resolution: string) => {
    isLoading.value = true
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const reportIndex = userReports.value.findIndex(report => report.id === reportId)
      if (reportIndex !== -1) {
        userReports.value[reportIndex].status = 'resolved'
        userReports.value[reportIndex].resolved_at = new Date().toISOString()
      }
    } catch (err) {
      error.value = 'Failed to resolve report'
    } finally {
      isLoading.value = false
    }
  }

  // Initialize mock data on store creation
  initializeMockData()

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
    moderateContent,
    resolveReport
  }
})