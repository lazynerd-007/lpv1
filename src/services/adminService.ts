import { apiService } from './api'

export interface AdminDashboard {
  system_metrics: SystemMetrics
  user_analytics: UserAnalytics
  content_analytics: ContentAnalytics
  recent_activity: RecentActivity[]
}

export interface SystemMetrics {
  total_users: number
  total_movies: number
  total_reviews: number
  total_reports: number
  active_users_today: number
  active_users_week: number
  active_users_month: number
  new_users_today: number
  new_users_week: number
  new_users_month: number
  reviews_today: number
  reviews_week: number
  reviews_month: number
  pending_reports: number
  flagged_reviews: number
}

export interface UserAnalytics {
  user_growth: any[]
  user_activity: any[]
  role_distribution: any[]
  top_reviewers: any[]
  user_retention: any[]
}

export interface ContentAnalytics {
  review_trends: any[]
  rating_distribution: any[]
  popular_movies: any[]
  genre_popularity: any[]
  content_moderation_stats: any[]
}

export interface RecentActivity {
  id: string
  type: string
  description: string
  timestamp: string
  user_id?: string
  user_name?: string
}

export interface ReviewModerationItem {
  id: string
  user_id: string
  user_name: string
  user_avatar: string
  movie_title: string
  review_text: string
  lemon_pie_rating: number
  created_at: string
  is_flagged: boolean
  is_reported: boolean
  moderation_status: string
  report_count?: number
}

export interface ReviewModerationResponse {
  reviews: ReviewModerationItem[]
  total: number
  page: number
  per_page: number
  total_pages: number
}

export interface UserListItem {
  id: string
  name: string
  email: string
  avatar: string
  role: string
  is_verified: boolean
  is_suspended: boolean
  is_active: boolean
  created_at: string
  last_login?: string
  review_count: number
  followers_count: number
}

export interface UserListResponse {
  users: UserListItem[]
  total: number
  page: number
  per_page: number
  total_pages: number
}

export interface ReportItem {
  id: string
  type: string
  content_id: string
  reason: string
  description: string
  reporter_name: string
  reported_user_name?: string
  status: string
  created_at: string
  resolved_at?: string
  resolved_by?: string
}

export interface ReportListResponse {
  reports: ReportItem[]
  total: number
  page: number
  per_page: number
  total_pages: number
}

export interface ModerationAction {
  action: 'approve' | 'reject' | 'flag' | 'unflag'
  reason?: string
}

export interface UserRoleUpdate {
  role: string
}

export interface UserSuspension {
  reason: string
  duration_days?: number
}

export interface ReportResolution {
  action: 'resolve' | 'dismiss'
  reason: string
  notify_reporter?: boolean
  notify_reported?: boolean
}

class AdminService {
  async getDashboard(): Promise<AdminDashboard> {
    const response = await apiService.request('/admin/dashboard')
    return response.data
  }

  async getSystemMetrics(): Promise<SystemMetrics> {
    const response = await apiService.request('/admin/metrics')
    return response.data
  }

  async getReviewsForModeration(params: {
    page?: number
    per_page?: number
    status?: string
    is_flagged?: boolean
    sort_by?: string
    sort_order?: string
  } = {}): Promise<ReviewModerationResponse> {
    const queryString = new URLSearchParams(params as any).toString()
    const response = await apiService.request(`/admin/moderation/reviews?${queryString}`)
    return response.data
  }

  async moderateReview(reviewId: string, action: ModerationAction): Promise<void> {
    await apiService.request(`/admin/moderation/reviews/${reviewId}`, {
      method: 'POST',
      body: JSON.stringify(action)
    })
  }

  async bulkModerateReviews(reviewIds: string[], action: ModerationAction): Promise<{ moderated_count: number }> {
    const response = await apiService.request('/admin/moderation/reviews/bulk', {
      method: 'POST',
      body: JSON.stringify({
        review_ids: reviewIds,
        action: action.action,
        reason: action.reason
      })
    })
    return response.data
  }

  async getUsersList(params: {
    page?: number
    per_page?: number
    search?: string
    role?: string
    is_active?: boolean
    sort_by?: string
    sort_order?: string
  } = {}): Promise<UserListResponse> {
    const queryString = new URLSearchParams(params as any).toString()
    const response = await apiService.request(`/admin/users?${queryString}`)
    return response.data
  }

  async updateUserRole(userId: string, role: string): Promise<void> {
    await apiService.request(`/admin/users/${userId}/role`, {
      method: 'PUT',
      body: JSON.stringify({ role })
    })
  }

  async suspendUser(userId: string, suspension: UserSuspension): Promise<void> {
    await apiService.request(`/admin/users/${userId}/suspend`, {
      method: 'POST',
      body: JSON.stringify(suspension)
    })
  }

  async activateUser(userId: string, reason: string): Promise<void> {
    await apiService.request(`/admin/users/${userId}/activate`, {
      method: 'POST',
      body: JSON.stringify({ reason })
    })
  }

  async getReportsList(params: {
    page?: number
    per_page?: number
    status?: string
    sort_by?: string
    sort_order?: string
  } = {}): Promise<ReportListResponse> {
    const queryString = new URLSearchParams(params as any).toString()
    const response = await apiService.request(`/admin/reports?${queryString}`)
    return response.data
  }

  async resolveReport(reportId: string, resolution: ReportResolution): Promise<void> {
    await apiService.request(`/admin/reports/${reportId}/resolve`, {
      method: 'POST',
      body: JSON.stringify(resolution)
    })
  }
}

export const adminService = new AdminService()