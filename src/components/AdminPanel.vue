<template>
  <div class="admin-panel">
    <div class="admin-header">
      <h2 class="admin-title">Admin Panel</h2>
      <div class="admin-stats">
        <div class="stat-card">
          <span class="stat-number">{{ systemMetrics?.pending_reports || 0 }}</span>
          <span class="stat-label">Pending Reports</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">{{ systemMetrics?.flagged_reviews || 0 }}</span>
          <span class="stat-label">Flagged Reviews</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">{{ verificationRequestsCount }}</span>
          <span class="stat-label">Verification Requests</span>
        </div>
      </div>
    </div>

    <div class="admin-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        class="tab-button"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
        <span v-if="tab.count > 0" class="tab-count">{{ tab.count }}</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading admin data...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state">
      <p class="error-message">{{ error }}</p>
      <button @click="loadData" class="retry-btn">Retry</button>
    </div>

    <!-- Review Moderation Tab -->
    <div v-else-if="activeTab === 'reviews'" class="tab-content">
      <div class="content-header">
        <h3>Review Moderation</h3>
        <div class="filters">
          <select v-model="reviewFilter" class="filter-select" @change="loadReviews">
            <option value="">All Reviews</option>
            <option value="pending">Pending Approval</option>
            <option value="flagged">Flagged Reviews</option>
            <option value="approved">Approved Reviews</option>
            <option value="rejected">Rejected Reviews</option>
          </select>
          <label class="checkbox-filter">
            <input type="checkbox" v-model="showFlaggedOnly" @change="loadReviews" />
            Show Flagged Only
          </label>
        </div>
      </div>
      
      <div class="review-list">
        <div v-if="reviewsLoading" class="loading-reviews">
          <div class="spinner"></div>
          <p>Loading reviews...</p>
        </div>
        <div v-else-if="reviewsData?.reviews?.length === 0" class="no-data">
          <p>No reviews found matching the current filters.</p>
        </div>
        <div 
          v-else
          v-for="review in reviewsData?.reviews" 
          :key="review.id"
          class="review-item"
          :class="{ 
            flagged: review.is_flagged, 
            reported: review.is_reported,
            pending: review.moderation_status === 'pending',
            approved: review.moderation_status === 'approved',
            rejected: review.moderation_status === 'rejected'
          }"
        >
          <div class="review-header">
            <div class="user-info">
              <img :src="review.user_avatar || defaultAvatar" :alt="review.user_name" class="user-avatar" />
              <div>
                <span class="user-name">{{ review.user_name }}</span>
                <span class="review-date">{{ formatDate(review.created_at) }}</span>
                <span class="movie-title">{{ review.movie_title }}</span>
              </div>
            </div>
            <div class="review-status">
              <span v-if="review.is_flagged" class="status-badge flagged">Flagged</span>
              <span v-if="review.is_reported" class="status-badge reported">Reported ({{ review.report_count || 0 }})</span>
              <span class="status-badge" :class="review.moderation_status">{{ review.moderation_status }}</span>
              <span class="rating">{{ review.lemon_pie_rating }}/10</span>
            </div>
          </div>
          
          <div class="review-content">
            <p>{{ review.review_text }}</p>
          </div>
          
          <div class="review-actions">
            <button 
              @click="moderateReview(review.id, 'approve')"
              class="action-btn approve"
              :disabled="review.moderation_status === 'approved' || moderatingReviews.has(review.id)"
            >
              {{ moderatingReviews.has(review.id) ? 'Processing...' : 'Approve' }}
            </button>
            <button 
              @click="moderateReview(review.id, review.is_flagged ? 'unflag' : 'flag')"
              class="action-btn flag"
              :class="{ active: review.is_flagged }"
              :disabled="moderatingReviews.has(review.id)"
            >
              {{ review.is_flagged ? 'Unflag' : 'Flag' }}
            </button>
            <button 
              @click="moderateReview(review.id, 'reject')"
              class="action-btn reject"
              :disabled="review.moderation_status === 'rejected' || moderatingReviews.has(review.id)"
            >
              Reject
            </button>
            <button 
              @click="viewReportDetails(review.id)"
              class="action-btn details"
              v-if="review.is_reported"
            >
              View Reports
            </button>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="reviewsData && reviewsData.total_pages > 1" class="pagination">
        <button 
          @click="changePage(reviewsData.page - 1)" 
          :disabled="reviewsData.page <= 1"
          class="page-btn"
        >
          Previous
        </button>
        <span class="page-info">
          Page {{ reviewsData.page }} of {{ reviewsData.total_pages }}
        </span>
        <button 
          @click="changePage(reviewsData.page + 1)" 
          :disabled="reviewsData.page >= reviewsData.total_pages"
          class="page-btn"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Users Tab -->
    <div v-else-if="activeTab === 'users'" class="tab-content">
      <div class="content-header">
        <h3>User Management</h3>
        <div class="filters">
          <input 
            type="text" 
            v-model="userSearch" 
            placeholder="Search users..." 
            class="search-input"
            @input="debounceUserSearch"
          />
          <select v-model="userFilter" class="filter-select" @change="loadUsers">
            <option value="">All Users</option>
            <option value="user">Users</option>
            <option value="critic">Critics</option>
            <option value="moderator">Moderators</option>
            <option value="admin">Admins</option>
          </select>
          <label class="checkbox-filter">
            <input type="checkbox" v-model="showActiveOnly" @change="loadUsers" />
            Active Only
          </label>
        </div>
      </div>
      
      <div class="user-list">
        <div v-if="usersLoading" class="loading-users">
          <div class="spinner"></div>
          <p>Loading users...</p>
        </div>
        <div v-else-if="usersData?.users?.length === 0" class="no-data">
          <p>No users found matching the current filters.</p>
        </div>
        <div 
          v-else
          v-for="user in usersData?.users" 
          :key="user.id"
          class="user-item"
          :class="{ 
            suspended: user.is_suspended,
            inactive: !user.is_active,
            verified: user.is_verified
          }"
        >
          <div class="user-header">
            <div class="user-info">
              <img :src="user.avatar || defaultAvatar" :alt="user.name" class="user-avatar" />
              <div>
                <span class="user-name">{{ user.name }}</span>
                <span class="user-email">{{ user.email }}</span>
                <span class="user-joined">Joined {{ formatDate(user.created_at) }}</span>
                <span v-if="user.last_login" class="user-last-login">Last login: {{ formatDate(user.last_login) }}</span>
              </div>
            </div>
            <div class="user-status">
              <span class="role-badge" :class="user.role">{{ user.role }}</span>
              <span v-if="user.is_verified" class="status-badge verified">Verified</span>
              <span v-if="user.is_suspended" class="status-badge suspended">Suspended</span>
              <span v-if="!user.is_active" class="status-badge inactive">Inactive</span>
              <div class="user-stats">
                <span>{{ user.review_count }} reviews</span>
                <span>{{ user.followers_count }} followers</span>
              </div>
            </div>
          </div>
          
          <div class="user-actions">
            <select 
              :value="user.role" 
              @change="updateUserRole(user.id, $event.target.value)"
              class="role-select"
              :disabled="user.id === currentUserId || updatingUsers.has(user.id)"
            >
              <option value="user">User</option>
              <option value="critic">Critic</option>
              <option value="moderator">Moderator</option>
              <option value="admin">Admin</option>
            </select>
            <button 
              @click="user.is_verified ? null : toggleUserVerification(user.id)"
              class="action-btn verify"
              :class="{ active: user.is_verified }"
              :disabled="user.is_verified || updatingUsers.has(user.id)"
            >
              {{ user.is_verified ? 'Verified' : 'Verify' }}
            </button>
            <button 
              @click="toggleUserSuspension(user.id, user.is_suspended)"
              class="action-btn suspend"
              :class="{ active: user.is_suspended }"
              :disabled="user.id === currentUserId || updatingUsers.has(user.id)"
            >
              {{ updatingUsers.has(user.id) ? 'Processing...' : (user.is_suspended ? 'Unsuspend' : 'Suspend') }}
            </button>
            <button 
              @click="viewUserDetails(user.id)"
              class="action-btn details"
            >
              Details
            </button>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="usersData && usersData.total_pages > 1" class="pagination">
        <button 
          @click="changeUsersPage(usersData.page - 1)" 
          :disabled="usersData.page <= 1"
          class="page-btn"
        >
          Previous
        </button>
        <span class="page-info">
          Page {{ usersData.page }} of {{ usersData.total_pages }}
        </span>
        <button 
          @click="changeUsersPage(usersData.page + 1)" 
          :disabled="usersData.page >= usersData.total_pages"
          class="page-btn"
        >
          Next
        </button>
      </div>
    </div>

    <!-- Reports Tab -->
    <div v-else-if="activeTab === 'reports'" class="tab-content">
      <div class="content-header">
        <h3>Reports Management</h3>
        <div class="filters">
          <select v-model="reportFilter" class="filter-select" @change="loadReports">
            <option value="">All Reports</option>
            <option value="pending">Pending</option>
            <option value="resolved">Resolved</option>
            <option value="dismissed">Dismissed</option>
          </select>
        </div>
      </div>
      
      <div class="report-list">
        <div v-if="reportsLoading" class="loading-reports">
          <div class="spinner"></div>
          <p>Loading reports...</p>
        </div>
        <div v-else-if="reportsData?.reports?.length === 0" class="no-data">
          <p>No reports found matching the current filters.</p>
        </div>
        <div 
          v-else
          v-for="report in reportsData?.reports" 
          :key="report.id"
          class="report-item"
          :class="{ 
            pending: report.status === 'pending',
            resolved: report.status === 'resolved',
            dismissed: report.status === 'dismissed'
          }"
        >
          <div class="report-header">
            <div class="report-info">
              <span class="report-type">{{ report.type }}</span>
              <span class="report-reason">{{ report.reason }}</span>
              <span class="report-date">{{ formatDate(report.created_at) }}</span>
            </div>
            <div class="report-status">
              <span class="status-badge" :class="report.status">{{ report.status }}</span>
            </div>
          </div>
          
          <div class="report-content">
            <p><strong>Reporter:</strong> {{ report.reporter_name }}</p>
            <p v-if="report.reported_user_name"><strong>Reported User:</strong> {{ report.reported_user_name }}</p>
            <p><strong>Description:</strong> {{ report.description }}</p>
            <p v-if="report.resolved_at"><strong>Resolved:</strong> {{ formatDate(report.resolved_at) }} by {{ report.resolved_by }}</p>
          </div>
          
          <div class="report-actions" v-if="report.status === 'pending'">
            <button 
              @click="resolveReport(report.id, 'resolve')"
              class="action-btn approve"
              :disabled="resolvingReports.has(report.id)"
            >
              {{ resolvingReports.has(report.id) ? 'Processing...' : 'Resolve' }}
            </button>
            <button 
              @click="resolveReport(report.id, 'dismiss')"
              class="action-btn dismiss"
              :disabled="resolvingReports.has(report.id)"
            >
              Dismiss
            </button>
            <button 
              @click="viewReportedContent(report.content_id)"
              class="action-btn details"
            >
              View Content
            </button>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="reportsData && reportsData.total_pages > 1" class="pagination">
        <button 
          @click="changeReportsPage(reportsData.page - 1)" 
          :disabled="reportsData.page <= 1"
          class="page-btn"
        >
          Previous
        </button>
        <span class="page-info">
          Page {{ reportsData.page }} of {{ reportsData.total_pages }}
        </span>
        <button 
          @click="changeReportsPage(reportsData.page + 1)" 
          :disabled="reportsData.page >= reportsData.total_pages"
          class="page-btn"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import { 
  adminService, 
  type AdminDashboard, 
  type SystemMetrics,
  type ReviewModerationResponse,
  type UserListResponse,
  type ReportListResponse
} from '@/services/adminService'

const userStore = useUserStore()
const uiStore = useUIStore()

// State
const loading = ref(true)
const error = ref<string | null>(null)
const activeTab = ref('reviews')

// Data
const dashboard = ref<AdminDashboard | null>(null)
const systemMetrics = ref<SystemMetrics | null>(null)
const reviewsData = ref<ReviewModerationResponse | null>(null)
const usersData = ref<UserListResponse | null>(null)
const reportsData = ref<ReportListResponse | null>(null)

// Loading states
const reviewsLoading = ref(false)
const usersLoading = ref(false)
const reportsLoading = ref(false)

// Filters
const reviewFilter = ref('')
const showFlaggedOnly = ref(false)
const userFilter = ref('')
const userSearch = ref('')
const showActiveOnly = ref(false)
const reportFilter = ref('')

// Processing states
const moderatingReviews = ref(new Set<string>())
const updatingUsers = ref(new Set<string>())
const resolvingReports = ref(new Set<string>())

// Pagination
const currentPage = ref(1)
const usersPage = ref(1)
const reportsPage = ref(1)

// Constants
const defaultAvatar = 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=default%20user%20avatar&image_size=square'
const currentUserId = computed(() => userStore.user?.id)

// Computed
const verificationRequestsCount = computed(() => {
  return usersData.value?.users?.filter(user => 
    user.role === 'critic' && !user.is_verified
  ).length || 0
})

const tabs = computed(() => [
  { 
    id: 'reviews', 
    label: 'Reviews', 
    count: systemMetrics.value?.flagged_reviews || 0 
  },
  { 
    id: 'users', 
    label: 'Users', 
    count: verificationRequestsCount.value 
  },
  { 
    id: 'reports', 
    label: 'Reports', 
    count: systemMetrics.value?.pending_reports || 0 
  }
])

const pendingReports = computed(() => 
  reports.value.filter(report => report.status === 'pending')
)

const flaggedReviews = computed(() => 
  reviews.value.filter(review => review.isFlagged || review.isReported)
)

const verificationRequests = computed(() => 
  users.value.filter(user => user.role === 'critic' && !user.isVerified)
)

const filteredReviews = computed(() => {
  let filtered = reviews.value
  
  switch (reviewFilter.value) {
    case 'flagged':
      filtered = filtered.filter(review => review.isFlagged)
      break
    case 'reported':
      filtered = filtered.filter(review => review.isReported)
      break
    case 'pending':
      filtered = filtered.filter(review => !review.isApproved)
      break
  }
  
  return filtered
})

const filteredUsers = computed(() => {
  let filtered = users.value
  
  switch (userFilter.value) {
    case 'critics':
      filtered = filtered.filter(user => user.role === 'critic')
      break
    case 'verified':
      filtered = filtered.filter(user => user.isVerified)
      break
    case 'suspended':
      filtered = filtered.filter(user => user.isSuspended)
      break
  }
  
  return filtered
})

const filteredReports = computed(() => {
  let filtered = reports.value
  
  if (reportFilter.value !== 'all') {
    filtered = filtered.filter(report => report.status === reportFilter.value)
  }
  
  return filtered
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const approveReview = (reviewId: string) => {
  const review = reviews.value.find(r => r.id === reviewId)
  if (review) {
    review.isApproved = true
    review.isFlagged = false
    uiStore.showToast({ message: 'Review approved successfully', type: 'success' })
  }
}

const flagReview = (reviewId: string) => {
  const review = reviews.value.find(r => r.id === reviewId)
  if (review) {
    review.isFlagged = !review.isFlagged
    const action = review.isFlagged ? 'flagged' : 'unflagged'
    uiStore.showToast({ message: `Review ${action} successfully`, type: 'success' })
  }
}

const deleteReview = (reviewId: string) => {
  const index = reviews.value.findIndex(r => r.id === reviewId)
  if (index !== -1) {
    reviews.value.splice(index, 1)
    uiStore.showToast({ message: 'Review deleted successfully', type: 'success' })
  }
}

const viewReportDetails = (reviewId: string) => {
  // Implementation for viewing report details
  uiStore.showToast({ message: 'Opening report details...', type: 'info' })
}

const toggleUserVerification = (userId: string) => {
  const user = users.value.find(u => u.id === userId)
  if (user) {
    user.isVerified = !user.isVerified
    const action = user.isVerified ? 'verified' : 'unverified'
    uiStore.showToast({ message: `User ${action} successfully`, type: 'success' })
  }
}

const suspendUser = (userId: string) => {
  const user = users.value.find(u => u.id === userId)
  if (user) {
    user.isSuspended = !user.isSuspended
    const action = user.isSuspended ? 'suspended' : 'unsuspended'
    uiStore.showToast({ message: `User ${action} successfully`, type: 'success' })
  }
}

const viewUserDetails = (userId: string) => {
  // Implementation for viewing user details
  uiStore.showToast({ message: 'Opening user details...', type: 'info' })
}

const resolveReport = (reportId: string) => {
  const report = reports.value.find(r => r.id === reportId)
  if (report) {
    report.status = 'resolved'
    uiStore.showToast({ message: 'Report resolved successfully', type: 'success' })
  }
}

const dismissReport = (reportId: string) => {
  const report = reports.value.find(r => r.id === reportId)
  if (report) {
    report.status = 'dismissed'
    uiStore.showToast({ message: 'Report dismissed successfully', type: 'success' })
  }
}

const viewReportedContent = (contentId: string) => {
  // Implementation for viewing reported content
  uiStore.showToast({ message: 'Opening reported content...', type: 'info' })
}

onMounted(() => {
  // Load admin data
})
// Methods
const loadData = async () => {
  loading.value = true
  error.value = null
  
  try {
    // Load dashboard and system metrics
    const [dashboardData, metricsData] = await Promise.all([
      adminService.getDashboard(),
      adminService.getSystemMetrics()
    ])
    
    dashboard.value = dashboardData
    systemMetrics.value = metricsData
    
    // Load initial data based on active tab
    await loadTabData()
  } catch (err) {
    console.error('Error loading admin data:', err)
    error.value = 'Failed to load admin data. Please try again.'
  } finally {
    loading.value = false
  }
}

const loadTabData = async () => {
  switch (activeTab.value) {
    case 'reviews':
      await loadReviews()
      break
    case 'users':
      await loadUsers()
      break
    case 'reports':
      await loadReports()
      break
  }
}

const loadReviews = async () => {
  reviewsLoading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      per_page: 20,
      status: reviewFilter.value || undefined,
      flagged_only: showFlaggedOnly.value || undefined
    }
    
    reviewsData.value = await adminService.getReviewsForModeration(params)
  } catch (err) {
    console.error('Error loading reviews:', err)
    uiStore.showToast({ message: 'Failed to load reviews', type: 'error' })
  } finally {
    reviewsLoading.value = false
  }
}

const loadUsers = async () => {
  usersLoading.value = true
  
  try {
    const params = {
      page: usersPage.value,
      per_page: 20,
      role: userFilter.value || undefined,
      search: userSearch.value || undefined,
      active_only: showActiveOnly.value || undefined
    }
    
    usersData.value = await adminService.getUsersList(params)
  } catch (err) {
    console.error('Error loading users:', err)
    uiStore.showToast({ message: 'Failed to load users', type: 'error' })
  } finally {
    usersLoading.value = false
  }
}

const loadReports = async () => {
  reportsLoading.value = true
  
  try {
    const params = {
      page: reportsPage.value,
      per_page: 20,
      status: reportFilter.value || undefined
    }
    
    reportsData.value = await adminService.getReportsList(params)
  } catch (err) {
    console.error('Error loading reports:', err)
    uiStore.showToast({ message: 'Failed to load reports', type: 'error' })
  } finally {
    reportsLoading.value = false
  }
}

const moderateReview = async (reviewId: string, action: string) => {
  moderatingReviews.value.add(reviewId)
  
  try {
    await adminService.moderateReview(reviewId, { action })
    
    // Reload reviews to get updated data
    await loadReviews()
    
    const actionText = action === 'approve' ? 'approved' : action === 'reject' ? 'rejected' : action === 'flag' ? 'flagged' : 'unflagged'
    uiStore.showToast({ message: `Review ${actionText} successfully`, type: 'success' })
  } catch (err) {
    console.error('Error moderating review:', err)
    uiStore.showToast({ message: 'Failed to moderate review', type: 'error' })
  } finally {
    moderatingReviews.value.delete(reviewId)
  }
}

const updateUserRole = async (userId: string, newRole: string) => {
  updatingUsers.value.add(userId)
  
  try {
    await adminService.updateUserRole(userId, { role: newRole })
    
    // Reload users to get updated data
    await loadUsers()
    
    uiStore.showToast({ message: `User role updated to ${newRole}`, type: 'success' })
  } catch (err) {
    console.error('Error updating user role:', err)
    uiStore.showToast({ message: 'Failed to update user role', type: 'error' })
  } finally {
    updatingUsers.value.delete(userId)
  }
}

const toggleUserSuspension = async (userId: string, isSuspended: boolean) => {
  updatingUsers.value.add(userId)
  
  try {
    if (isSuspended) {
      await adminService.activateUser(userId)
    } else {
      await adminService.suspendUser(userId)
    }
    
    // Reload users to get updated data
    await loadUsers()
    
    const action = isSuspended ? 'activated' : 'suspended'
    uiStore.showToast({ message: `User ${action} successfully`, type: 'success' })
  } catch (err) {
    console.error('Error updating user suspension:', err)
    uiStore.showToast({ message: 'Failed to update user status', type: 'error' })
  } finally {
    updatingUsers.value.delete(userId)
  }
}

const toggleUserVerification = async (userId: string) => {
  updatingUsers.value.add(userId)
  
  try {
    // This would need to be implemented in the backend
    // For now, we'll show a placeholder message
    uiStore.showToast({ message: 'User verification feature coming soon', type: 'info' })
  } catch (err) {
    console.error('Error updating user verification:', err)
    uiStore.showToast({ message: 'Failed to update user verification', type: 'error' })
  } finally {
    updatingUsers.value.delete(userId)
  }
}

const resolveReport = async (reportId: string, action: string) => {
  resolvingReports.value.add(reportId)
  
  try {
    await adminService.resolveReport(reportId, { action })
    
    // Reload reports to get updated data
    await loadReports()
    
    const actionText = action === 'resolve' ? 'resolved' : 'dismissed'
    uiStore.showToast({ message: `Report ${actionText} successfully`, type: 'success' })
  } catch (err) {
    console.error('Error resolving report:', err)
    uiStore.showToast({ message: 'Failed to resolve report', type: 'error' })
  } finally {
    resolvingReports.value.delete(reportId)
  }
}

// Pagination methods
const changePage = async (newPage: number) => {
  currentPage.value = newPage
  await loadReviews()
}

const changeUsersPage = async (newPage: number) => {
  usersPage.value = newPage
  await loadUsers()
}

const changeReportsPage = async (newPage: number) => {
  reportsPage.value = newPage
  await loadReports()
}

// Search debouncing
let searchTimeout: NodeJS.Timeout
const debounceUserSearch = () => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    usersPage.value = 1 // Reset to first page
    loadUsers()
  }, 500)
}

// Utility methods
const viewReportDetails = (reviewId: string) => {
  uiStore.showToast({ message: 'Report details feature coming soon', type: 'info' })
}

const viewUserDetails = (userId: string) => {
  uiStore.showToast({ message: 'User details feature coming soon', type: 'info' })
}

const viewReportedContent = (contentId: string) => {
  uiStore.showToast({ message: 'Reported content viewer coming soon', type: 'info' })
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Watchers
watch(activeTab, async (newTab) => {
  await loadTabData()
})

// Lifecycle
onMounted(async () => {
  await loadData()
})
</script>

<style scoped>
.admin-panel {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.admin-header {
  margin-bottom: 2rem;
}

.admin-title {
  font-size: 2rem;
  font-weight: bold;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.admin-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 2rem;
  font-weight: bold;
  color: var(--accent-color);
}

.stat-label {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.admin-tabs {
  display: flex;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 2rem;
}

.tab-button {
  background: none;
  border: none;
  padding: 1rem 1.5rem;
  cursor: pointer;
  color: var(--text-secondary);
  font-weight: 500;
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab-button:hover {
  color: var(--text-primary);
}

.tab-button.active {
  color: var(--accent-color);
  border-bottom-color: var(--accent-color);
}

.tab-count {
  background: var(--accent-color);
  color: white;
  border-radius: 12px;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  font-weight: bold;
}

.tab-content {
  min-height: 400px;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.content-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.filters {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.filter-select,
.search-input,
.role-select {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  color: var(--text-primary);
  cursor: pointer;
}

.search-input {
  min-width: 200px;
}

.checkbox-filter {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-primary);
  cursor: pointer;
}

.checkbox-filter input[type="checkbox"] {
  cursor: pointer;
}

/* Loading and Error States */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
}

.loading-reviews,
.loading-users,
.loading-reports {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  text-align: center;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--border-color);
  border-top: 4px solid var(--accent-color);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  color: #ef4444;
  margin-bottom: 1rem;
}

.retry-btn {
  background: var(--accent-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
}

.retry-btn:hover {
  background: var(--accent-color-dark);
}

.no-data {
  text-align: center;
  padding: 2rem;
  color: var(--text-secondary);
}

/* Lists */
.review-list,
.user-list,
.report-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.review-item,
.user-item,
.report-item {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.review-item:hover,
.user-item:hover,
.report-item:hover {
  border-color: var(--accent-color);
}

.review-item.flagged {
  border-left: 4px solid #ef4444;
}

.review-item.reported {
  border-left: 4px solid #f59e0b;
}

.review-item.pending {
  border-left: 4px solid #3b82f6;
}

.review-item.approved {
  border-left: 4px solid #10b981;
}

.review-item.rejected {
  border-left: 4px solid #ef4444;
}

.user-item.suspended {
  border-left: 4px solid #ef4444;
}

.user-item.verified {
  border-left: 4px solid #10b981;
}

.report-item.pending {
  border-left: 4px solid #f59e0b;
}

.report-item.resolved {
  border-left: 4px solid #10b981;
}

.report-item.dismissed {
  border-left: 4px solid #6b7280;
}

/* Headers */
.review-header,
.user-header,
.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-weight: 600;
  color: var(--text-primary);
  display: block;
}

.user-email,
.user-joined,
.user-last-login,
.review-date,
.movie-title {
  color: var(--text-secondary);
  font-size: 0.875rem;
  display: block;
}

.review-status,
.user-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.user-status {
  flex-direction: column;
  align-items: flex-end;
}

.user-stats {
  display: flex;
  gap: 1rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* Badges */
.status-badge,
.role-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.flagged {
  background: #fef2f2;
  color: #dc2626;
}

.status-badge.reported {
  background: #fffbeb;
  color: #d97706;
}

.status-badge.pending {
  background: #eff6ff;
  color: #2563eb;
}

.status-badge.approved {
  background: #f0fdf4;
  color: #16a34a;
}

.status-badge.rejected {
  background: #fef2f2;
  color: #dc2626;
}

.status-badge.verified {
  background: #f0fdf4;
  color: #16a34a;
}

.status-badge.suspended {
  background: #fef2f2;
  color: #dc2626;
}

.status-badge.inactive {
  background: #f8fafc;
  color: #64748b;
}

.status-badge.resolved {
  background: #f0fdf4;
  color: #16a34a;
}

.status-badge.dismissed {
  background: #f8fafc;
  color: #64748b;
}

.role-badge.user {
  background: #f1f5f9;
  color: #475569;
}

.role-badge.critic {
  background: #fef3c7;
  color: #d97706;
}

.role-badge.moderator {
  background: #dbeafe;
  color: #2563eb;
}

.role-badge.admin {
  background: #fce7f3;
  color: #be185d;
}

.rating {
  background: var(--accent-color);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.875rem;
}

/* Content */
.review-content p,
.report-content p {
  color: var(--text-primary);
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

/* Actions */
.review-actions,
.user-actions,
.report-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}

.action-btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.875rem;
  transition: all 0.2s ease;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn.approve {
  background: #10b981;
  color: white;
}

.action-btn.approve:hover:not(:disabled) {
  background: #059669;
}

.action-btn.flag {
  background: #f59e0b;
  color: white;
}

.action-btn.flag:hover:not(:disabled) {
  background: #d97706;
}

.action-btn.flag.active {
  background: #dc2626;
}

.action-btn.reject {
  background: #ef4444;
  color: white;
}

.action-btn.reject:hover:not(:disabled) {
  background: #dc2626;
}

.action-btn.details,
.action-btn.verify,
.action-btn.suspend,
.action-btn.dismiss {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.action-btn.details:hover:not(:disabled),
.action-btn.verify:hover:not(:disabled),
.action-btn.suspend:hover:not(:disabled),
.action-btn.dismiss:hover:not(:disabled) {
  background: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.action-btn.verify.active {
  background: #10b981;
  color: white;
  border-color: #10b981;
}

.action-btn.suspend.active {
  background: #ef4444;
  color: white;
  border-color: #ef4444;
}

/* Pagination */
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding: 1rem;
}

.page-btn {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.page-btn:hover:not(:disabled) {
  background: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: var(--text-secondary);
  font-weight: 500;
}

/* Report specific styles */
.report-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.report-type {
  background: var(--accent-color);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.report-reason {
  color: var(--text-primary);
  font-weight: 500;
}

.report-date {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .admin-panel {
    padding: 1rem;
  }
  
  .admin-stats {
    grid-template-columns: 1fr;
  }
  
  .content-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filters {
    width: 100%;
    justify-content: flex-start;
  }
  
  .search-input {
    min-width: auto;
    width: 100%;
  }
  
  .review-header,
  .user-header,
  .report-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .review-status,
  .user-status {
    align-items: flex-start;
  }
  
  .review-actions,
  .user-actions,
  .report-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
  
  .pagination {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .page-btn {
    width: 100%;
  }
}