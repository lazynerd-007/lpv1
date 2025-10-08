<template>
  <div class="admin-panel">
    <div class="admin-header">
      <h2 class="admin-title">Admin Panel</h2>
      <div class="admin-stats">
        <div class="stat-card">
          <span class="stat-number">{{ pendingReports.length }}</span>
          <span class="stat-label">Pending Reports</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">{{ flaggedReviews.length }}</span>
          <span class="stat-label">Flagged Reviews</span>
        </div>
        <div class="stat-card">
          <span class="stat-number">{{ verificationRequests.length }}</span>
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

    <!-- Review Moderation Tab -->
    <div v-if="activeTab === 'reviews'" class="tab-content">
      <div class="content-header">
        <h3>Review Moderation</h3>
        <div class="filters">
          <select v-model="reviewFilter" class="filter-select">
            <option value="all">All Reviews</option>
            <option value="flagged">Flagged Reviews</option>
            <option value="reported">Reported Reviews</option>
            <option value="pending">Pending Approval</option>
          </select>
        </div>
      </div>
      
      <div class="review-list">
        <div 
          v-for="review in filteredReviews" 
          :key="review.id"
          class="review-item"
          :class="{ flagged: review.isFlagged, reported: review.isReported }"
        >
          <div class="review-header">
            <div class="user-info">
              <img :src="review.userAvatar" :alt="review.userName" class="user-avatar" />
              <div>
                <span class="user-name">{{ review.userName }}</span>
                <span class="review-date">{{ formatDate(review.createdAt) }}</span>
              </div>
            </div>
            <div class="review-status">
              <span v-if="review.isFlagged" class="status-badge flagged">Flagged</span>
              <span v-if="review.isReported" class="status-badge reported">Reported</span>
              <span class="rating">{{ review.lemonPieRating }}/10</span>
            </div>
          </div>
          
          <div class="review-content">
            <p>{{ review.reviewText }}</p>
          </div>
          
          <div class="review-actions">
            <button 
              @click="approveReview(review.id)"
              class="action-btn approve"
              :disabled="review.isApproved"
            >
              Approve
            </button>
            <button 
              @click="flagReview(review.id)"
              class="action-btn flag"
              :class="{ active: review.isFlagged }"
            >
              {{ review.isFlagged ? 'Unflag' : 'Flag' }}
            </button>
            <button 
              @click="deleteReview(review.id)"
              class="action-btn delete"
            >
              Delete
            </button>
            <button 
              @click="viewReportDetails(review.id)"
              class="action-btn details"
              v-if="review.isReported"
            >
              View Reports
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- User Management Tab -->
    <div v-if="activeTab === 'users'" class="tab-content">
      <div class="content-header">
        <h3>User Management</h3>
        <div class="filters">
          <select v-model="userFilter" class="filter-select">
            <option value="all">All Users</option>
            <option value="critics">Critics</option>
            <option value="verified">Verified Users</option>
            <option value="suspended">Suspended Users</option>
          </select>
        </div>
      </div>
      
      <div class="user-list">
        <div 
          v-for="user in filteredUsers" 
          :key="user.id"
          class="user-item"
        >
          <div class="user-info">
            <img :src="user.avatar" :alt="user.name" class="user-avatar" />
            <div class="user-details">
              <span class="user-name">{{ user.name }}</span>
              <span class="user-email">{{ user.email }}</span>
              <span class="user-role">{{ user.role }}</span>
            </div>
          </div>
          
          <div class="user-stats">
            <span class="stat">{{ user.reviewCount || 0 }} reviews</span>
            <span class="stat">{{ user.followersCount || 0 }} followers</span>
          </div>
          
          <div class="user-actions">
            <button 
              @click="toggleUserVerification(user.id)"
              class="action-btn verify"
              :class="{ active: user.isVerified }"
            >
              {{ user.isVerified ? 'Unverify' : 'Verify' }}
            </button>
            <button 
              @click="suspendUser(user.id)"
              class="action-btn suspend"
              :class="{ active: user.isSuspended }"
            >
              {{ user.isSuspended ? 'Unsuspend' : 'Suspend' }}
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
    </div>

    <!-- Reports Tab -->
    <div v-if="activeTab === 'reports'" class="tab-content">
      <div class="content-header">
        <h3>Content Reports</h3>
        <div class="filters">
          <select v-model="reportFilter" class="filter-select">
            <option value="all">All Reports</option>
            <option value="pending">Pending</option>
            <option value="resolved">Resolved</option>
            <option value="dismissed">Dismissed</option>
          </select>
        </div>
      </div>
      
      <div class="report-list">
        <div 
          v-for="report in filteredReports" 
          :key="report.id"
          class="report-item"
        >
          <div class="report-header">
            <span class="report-type">{{ report.type }}</span>
            <span class="report-date">{{ formatDate(report.createdAt) }}</span>
            <span class="report-status" :class="report.status">{{ report.status }}</span>
          </div>
          
          <div class="report-content">
            <p><strong>Reason:</strong> {{ report.reason }}</p>
            <p><strong>Description:</strong> {{ report.description }}</p>
            <p><strong>Reported by:</strong> {{ report.reporterName }}</p>
          </div>
          
          <div class="report-actions">
            <button 
              @click="resolveReport(report.id)"
              class="action-btn approve"
              :disabled="report.status === 'resolved'"
            >
              Resolve
            </button>
            <button 
              @click="dismissReport(report.id)"
              class="action-btn dismiss"
              :disabled="report.status === 'dismissed'"
            >
              Dismiss
            </button>
            <button 
              @click="viewReportedContent(report.contentId)"
              class="action-btn details"
            >
              View Content
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'

interface Review {
  id: string
  userId: string
  userName: string
  userAvatar: string
  reviewText: string
  lemonPieRating: number
  createdAt: string
  isFlagged: boolean
  isReported: boolean
  isApproved: boolean
}

interface User {
  id: string
  name: string
  email: string
  avatar: string
  role: string
  isVerified: boolean
  isSuspended: boolean
  reviewCount?: number
  followersCount?: number
}

interface Report {
  id: string
  type: 'review' | 'user' | 'comment'
  contentId: string
  reason: string
  description: string
  reporterName: string
  status: 'pending' | 'resolved' | 'dismissed'
  createdAt: string
}

const userStore = useUserStore()
const uiStore = useUIStore()

const activeTab = ref('reviews')
const reviewFilter = ref('all')
const userFilter = ref('all')
const reportFilter = ref('all')

// Mock data - in real app, this would come from API
const reviews = ref<Review[]>([
  {
    id: '1',
    userId: 'user1',
    userName: 'John Doe',
    userAvatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20a%20movie%20critic&image_size=square',
    reviewText: 'This movie was absolutely terrible. The acting was poor and the plot made no sense.',
    lemonPieRating: 2,
    createdAt: '2024-01-15T10:30:00Z',
    isFlagged: true,
    isReported: true,
    isApproved: false
  },
  {
    id: '2',
    userId: 'user2',
    userName: 'Jane Smith',
    userAvatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20a%20female%20movie%20critic&image_size=square',
    reviewText: 'Great Nollywood production with excellent cinematography and authentic cultural representation.',
    lemonPieRating: 8,
    createdAt: '2024-01-14T15:45:00Z',
    isFlagged: false,
    isReported: false,
    isApproved: true
  }
])

const users = ref<User[]>([
  {
    id: 'user1',
    name: 'John Doe',
    email: 'john@example.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20a%20movie%20critic&image_size=square',
    role: 'critic',
    isVerified: false,
    isSuspended: false,
    reviewCount: 15,
    followersCount: 120
  },
  {
    id: 'user2',
    name: 'Jane Smith',
    email: 'jane@example.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20a%20female%20movie%20critic&image_size=square',
    role: 'critic',
    isVerified: true,
    isSuspended: false,
    reviewCount: 45,
    followersCount: 890
  }
])

const reports = ref<Report[]>([
  {
    id: 'report1',
    type: 'review',
    contentId: '1',
    reason: 'Inappropriate language',
    description: 'Contains offensive language and personal attacks',
    reporterName: 'Anonymous User',
    status: 'pending',
    createdAt: '2024-01-15T11:00:00Z'
  }
])

const tabs = computed(() => [
  { id: 'reviews', label: 'Reviews', count: flaggedReviews.value.length },
  { id: 'users', label: 'Users', count: verificationRequests.value.length },
  { id: 'reports', label: 'Reports', count: pendingReports.value.length }
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
}

.content-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.filter-select {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 6px;
  padding: 0.5rem 1rem;
  color: var(--text-primary);
  cursor: pointer;
}

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

.review-header,
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
.review-date,
.user-role {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.review-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.status-badge.flagged {
  background: #fef2f2;
  color: #dc2626;
}

.status-badge.reported {
  background: #fffbeb;
  color: #d97706;
}

.rating {
  background: var(--accent-color);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.875rem;
}

.review-content p,
.report-content p {
  color: var(--text-primary);
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

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

.action-btn.flag:hover {
  background: #d97706;
}

.action-btn.flag.active {
  background: #dc2626;
}

.action-btn.delete {
  background: #ef4444;
  color: white;
}

.action-btn.delete:hover {
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

.action-btn.details:hover,
.action-btn.verify:hover,
.action-btn.suspend:hover,
.action-btn.dismiss:hover {
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

.user-details {
  display: flex;
  flex-direction: column;
}

.user-stats {
  display: flex;
  gap: 1rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
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

.report-date {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.report-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.report-status.pending {
  background: #fffbeb;
  color: #d97706;
}

.report-status.resolved {
  background: #f0fdf4;
  color: #16a34a;
}

.report-status.dismissed {
  background: #f8fafc;
  color: #64748b;
}

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
    gap: 1rem;
  }
  
  .review-header,
  .report-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .review-actions,
  .user-actions,
  .report-actions {
    flex-direction: column;
  }
  
  .action-btn {
    width: 100%;
  }
}
</style>