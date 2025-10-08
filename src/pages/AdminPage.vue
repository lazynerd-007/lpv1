<template>
  <div class="admin-page">
    <!-- Admin Header -->
    <div class="admin-header">
      <div class="header-content">
        <div class="header-title">
          <Shield class="icon" />
          <h1>Admin Dashboard</h1>
        </div>
        <div class="header-actions">
          <button 
            class="action-btn"
            @click="refreshData"
            :disabled="isLoading"
          >
            <RefreshCw class="icon" :class="{ 'animate-spin': isLoading }" />
            Refresh
          </button>
          <button class="action-btn primary" @click="showQuickActions = !showQuickActions">
            <Zap class="icon" />
            Quick Actions
          </button>
        </div>
      </div>
      
      <!-- Quick Actions Panel -->
      <div v-if="showQuickActions" class="quick-actions-panel">
        <div class="quick-action" @click="broadcastMessage">
          <MessageCircle class="icon" />
          <span>Broadcast Message</span>
        </div>
        <div class="quick-action" @click="exportData">
          <Download class="icon" />
          <span>Export Data</span>
        </div>
        <div class="quick-action" @click="systemMaintenance">
          <Settings class="icon" />
          <span>System Maintenance</span>
        </div>
        <div class="quick-action" @click="viewLogs">
          <FileText class="icon" />
          <span>View Logs</span>
        </div>
      </div>
    </div>

    <!-- Admin Navigation Tabs -->
    <div class="admin-nav">
      <button 
        v-for="tab in adminTabs" 
        :key="tab.id"
        class="nav-tab"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        <component :is="tab.icon" class="icon" />
        {{ tab.label }}
        <span v-if="tab.badge" class="tab-badge">{{ tab.badge }}</span>
      </button>
    </div>

    <!-- Admin Content -->
    <div class="admin-content">
      <!-- Analytics Dashboard -->
      <div v-if="activeTab === 'analytics'" class="tab-content">
        <AnalyticsDashboard />
      </div>

      <!-- Review Moderation -->
      <div v-if="activeTab === 'moderation'" class="tab-content">
        <AdminPanel />
      </div>

      <!-- User Management -->
      <div v-if="activeTab === 'users'" class="tab-content">
        <div class="section-header">
          <h2>User Management</h2>
          <div class="section-actions">
            <div class="search-box">
              <Search class="icon" />
              <input 
                v-model="userSearchQuery" 
                placeholder="Search users..."
                class="search-input"
              />
            </div>
            <select v-model="userFilter" class="filter-select">
              <option value="all">All Users</option>
              <option value="active">Active</option>
              <option value="suspended">Suspended</option>
              <option value="critics">Critics</option>
              <option value="admins">Admins</option>
            </select>
          </div>
        </div>
        
        <div class="users-table">
          <div class="table-header">
            <div class="header-cell">User</div>
            <div class="header-cell">Role</div>
            <div class="header-cell">Status</div>
            <div class="header-cell">Reviews</div>
            <div class="header-cell">Joined</div>
            <div class="header-cell">Actions</div>
          </div>
          
          <div 
            v-for="user in filteredUsers" 
            :key="user.id"
            class="table-row"
          >
            <div class="user-cell">
              <img :src="user.avatar" :alt="user.name" class="user-avatar" />
              <div class="user-info">
                <span class="user-name">{{ user.name }}</span>
                <span class="user-email">{{ user.email }}</span>
              </div>
            </div>
            <div class="role-cell">
              <span class="role-badge" :class="user.role">{{ user.role }}</span>
              <CriticBadge 
                v-if="user.role === 'critic'" 
                :is-verified="user.isVerified"
                :verification-level="user.verificationLevel"
                size="small"
              />
            </div>
            <div class="status-cell">
              <span class="status-badge" :class="user.status">{{ user.status }}</span>
            </div>
            <div class="reviews-cell">{{ user.reviewCount }}</div>
            <div class="joined-cell">{{ formatDate(user.joinedAt) }}</div>
            <div class="actions-cell">
              <button 
                class="action-btn small"
                @click="viewUserDetails(user)"
              >
                <Eye class="icon" />
              </button>
              <button 
                class="action-btn small"
                @click="editUser(user)"
              >
                <Edit class="icon" />
              </button>
              <button 
                class="action-btn small danger"
                @click="suspendUser(user)"
                v-if="user.status !== 'suspended'"
              >
                <Ban class="icon" />
              </button>
              <button 
                class="action-btn small success"
                @click="unsuspendUser(user)"
                v-else
              >
                <CheckCircle class="icon" />
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Content Management -->
      <div v-if="activeTab === 'content'" class="tab-content">
        <div class="section-header">
          <h2>Content Management</h2>
          <div class="section-actions">
            <button class="action-btn" @click="bulkActions = !bulkActions">
              <CheckSquare class="icon" />
              Bulk Actions
            </button>
            <button class="action-btn primary" @click="createContent">
              <Plus class="icon" />
              Add Content
            </button>
          </div>
        </div>
        
        <div class="content-grid">
          <div 
            v-for="content in contentItems" 
            :key="content.id"
            class="content-card"
          >
            <div class="content-header">
              <span class="content-type" :class="content.type">{{ content.type }}</span>
              <div class="content-actions">
                <button class="action-btn small" @click="editContent(content)">
                  <Edit class="icon" />
                </button>
                <button class="action-btn small danger" @click="deleteContent(content)">
                  <Trash2 class="icon" />
                </button>
              </div>
            </div>
            
            <div class="content-body">
              <h3 class="content-title">{{ content.title }}</h3>
              <p class="content-description">{{ content.description }}</p>
              
              <div class="content-meta">
                <span class="meta-item">
                  <Calendar class="icon" />
                  {{ formatDate(content.createdAt) }}
                </span>
                <span class="meta-item">
                  <User class="icon" />
                  {{ content.author }}
                </span>
                <span class="meta-item">
                  <Eye class="icon" />
                  {{ content.views }}
                </span>
              </div>
            </div>
            
            <div class="content-footer">
              <span class="content-status" :class="content.status">{{ content.status }}</span>
              <button 
                class="action-btn small"
                @click="toggleContentStatus(content)"
              >
                {{ content.status === 'published' ? 'Unpublish' : 'Publish' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- System Settings -->
      <div v-if="activeTab === 'settings'" class="tab-content">
        <div class="settings-sections">
          <div class="settings-section">
            <h3>General Settings</h3>
            <div class="setting-group">
              <label class="setting-label">Site Name</label>
              <input v-model="systemSettings.siteName" class="setting-input" />
            </div>
            <div class="setting-group">
              <label class="setting-label">Site Description</label>
              <textarea v-model="systemSettings.siteDescription" class="setting-textarea"></textarea>
            </div>
            <div class="setting-group">
              <label class="setting-label">Maintenance Mode</label>
              <label class="toggle-switch">
                <input 
                  type="checkbox" 
                  v-model="systemSettings.maintenanceMode"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
          
          <div class="settings-section">
            <h3>Review Settings</h3>
            <div class="setting-group">
              <label class="setting-label">Auto-approve Reviews</label>
              <label class="toggle-switch">
                <input 
                  type="checkbox" 
                  v-model="systemSettings.autoApproveReviews"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
            <div class="setting-group">
              <label class="setting-label">Minimum Review Length</label>
              <input 
                type="number" 
                v-model="systemSettings.minReviewLength" 
                class="setting-input"
              />
            </div>
            <div class="setting-group">
              <label class="setting-label">Profanity Filter</label>
              <label class="toggle-switch">
                <input 
                  type="checkbox" 
                  v-model="systemSettings.profanityFilter"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
          
          <div class="settings-section">
            <h3>User Settings</h3>
            <div class="setting-group">
              <label class="setting-label">Allow User Registration</label>
              <label class="toggle-switch">
                <input 
                  type="checkbox" 
                  v-model="systemSettings.allowRegistration"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
            <div class="setting-group">
              <label class="setting-label">Email Verification Required</label>
              <label class="toggle-switch">
                <input 
                  type="checkbox" 
                  v-model="systemSettings.emailVerification"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
            <div class="setting-group">
              <label class="setting-label">Default User Role</label>
              <select v-model="systemSettings.defaultRole" class="setting-select">
                <option value="user">User</option>
                <option value="critic">Critic</option>
              </select>
            </div>
          </div>
        </div>
        
        <div class="settings-actions">
          <button class="action-btn" @click="resetSettings">
            <RotateCcw class="icon" />
            Reset to Defaults
          </button>
          <button class="action-btn primary" @click="saveSettings">
            <Save class="icon" />
            Save Settings
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  Shield, 
  RefreshCw, 
  Zap, 
  MessageCircle, 
  Download, 
  Settings, 
  FileText,
  BarChart3,
  Flag,
  Users,
  Database,
  Search,
  Eye,
  Edit,
  Ban,
  CheckCircle,
  CheckSquare,
  Plus,
  Trash2,
  Calendar,
  User,
  RotateCcw,
  Save
} from 'lucide-vue-next'
import AnalyticsDashboard from '@/components/AnalyticsDashboard.vue'
import AdminPanel from '@/components/AdminPanel.vue'
import CriticBadge from '@/components/CriticBadge.vue'
import { useUIStore } from '@/stores/uiStore'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'

interface AdminUser {
  id: string
  name: string
  email: string
  avatar: string
  role: 'user' | 'critic' | 'admin'
  status: 'active' | 'suspended' | 'pending'
  isVerified: boolean
  verificationLevel: 'basic' | 'professional' | 'expert'
  reviewCount: number
  joinedAt: string
}

interface ContentItem {
  id: string
  type: 'movie' | 'tv' | 'article' | 'announcement'
  title: string
  description: string
  author: string
  status: 'draft' | 'published' | 'archived'
  views: number
  createdAt: string
}

interface SystemSettings {
  siteName: string
  siteDescription: string
  maintenanceMode: boolean
  autoApproveReviews: boolean
  minReviewLength: number
  profanityFilter: boolean
  allowRegistration: boolean
  emailVerification: boolean
  defaultRole: 'user' | 'critic'
}

const uiStore = useUIStore()
const authStore = useAuthStore()
const router = useRouter()

const activeTab = ref('analytics')
const isLoading = ref(false)
const showQuickActions = ref(false)
const userSearchQuery = ref('')
const userFilter = ref('all')
const bulkActions = ref(false)

const adminTabs = ref([
  { id: 'analytics', label: 'Analytics', icon: BarChart3, badge: null },
  { id: 'moderation', label: 'Moderation', icon: Flag, badge: '12' },
  { id: 'users', label: 'Users', icon: Users, badge: null },
  { id: 'content', label: 'Content', icon: Database, badge: null },
  { id: 'settings', label: 'Settings', icon: Settings, badge: null }
])

// Mock data
const users = ref<AdminUser[]>([
  {
    id: '1',
    name: 'Adebayo Johnson',
    email: 'adebayo@example.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20man%20professional%20headshot&image_size=square',
    role: 'critic',
    status: 'active',
    isVerified: true,
    verificationLevel: 'expert',
    reviewCount: 156,
    joinedAt: '2023-01-15T00:00:00Z'
  },
  {
    id: '2',
    name: 'Funmi Adebisi',
    email: 'funmi@example.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20woman%20professional%20headshot&image_size=square',
    role: 'user',
    status: 'active',
    isVerified: false,
    verificationLevel: 'basic',
    reviewCount: 23,
    joinedAt: '2023-03-22T00:00:00Z'
  },
  {
    id: '3',
    name: 'Chidi Okafor',
    email: 'chidi@example.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20man%20professional%20headshot&image_size=square',
    role: 'admin',
    status: 'active',
    isVerified: true,
    verificationLevel: 'professional',
    reviewCount: 89,
    joinedAt: '2022-11-08T00:00:00Z'
  }
])

const contentItems = ref<ContentItem[]>([
  {
    id: '1',
    type: 'movie',
    title: 'The Wedding Party',
    description: 'Nigerian romantic comedy film',
    author: 'Admin',
    status: 'published',
    views: 1234,
    createdAt: '2024-01-10T00:00:00Z'
  },
  {
    id: '2',
    type: 'article',
    title: 'Top 10 Nollywood Movies of 2024',
    description: 'Comprehensive list of the best Nigerian films this year',
    author: 'Editorial Team',
    status: 'draft',
    views: 567,
    createdAt: '2024-01-12T00:00:00Z'
  },
  {
    id: '3',
    type: 'announcement',
    title: 'Platform Update v2.1',
    description: 'New features and improvements',
    author: 'System',
    status: 'published',
    views: 890,
    createdAt: '2024-01-08T00:00:00Z'
  }
])

const systemSettings = ref<SystemSettings>({
  siteName: 'LemonNPie',
  siteDescription: 'Nigerian Movie Review Platform',
  maintenanceMode: false,
  autoApproveReviews: false,
  minReviewLength: 50,
  profanityFilter: true,
  allowRegistration: true,
  emailVerification: true,
  defaultRole: 'user'
})

const filteredUsers = computed(() => {
  let filtered = users.value
  
  if (userFilter.value !== 'all') {
    filtered = filtered.filter(user => {
      switch (userFilter.value) {
        case 'active': return user.status === 'active'
        case 'suspended': return user.status === 'suspended'
        case 'critics': return user.role === 'critic'
        case 'admins': return user.role === 'admin'
        default: return true
      }
    })
  }
  
  if (userSearchQuery.value) {
    const query = userSearchQuery.value.toLowerCase()
    filtered = filtered.filter(user => 
      user.name.toLowerCase().includes(query) ||
      user.email.toLowerCase().includes(query)
    )
  }
  
  return filtered
})

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const refreshData = async () => {
  isLoading.value = true
  // Simulate API call
  await new Promise(resolve => setTimeout(resolve, 1000))
  isLoading.value = false
  uiStore.showToast({ message: 'Data refreshed successfully', type: 'success' })
}

const broadcastMessage = () => {
  uiStore.showToast({ message: 'Broadcast message feature coming soon', type: 'info' })
}

const exportData = () => {
  uiStore.showToast({ message: 'Exporting data...', type: 'info' })
}

const systemMaintenance = () => {
  uiStore.showToast({ message: 'System maintenance mode toggled', type: 'info' })
}

const viewLogs = () => {
  uiStore.showToast({ message: 'Opening system logs...', type: 'info' })
}

const viewUserDetails = (user: AdminUser) => {
  uiStore.showToast({ message: `Viewing details for ${user.name}`, type: 'info' })
}

const editUser = (user: AdminUser) => {
  uiStore.showToast({ message: `Editing user ${user.name}`, type: 'info' })
}

const suspendUser = (user: AdminUser) => {
  user.status = 'suspended'
  uiStore.showToast({ message: `User ${user.name} suspended`, type: 'warning' })
}

const unsuspendUser = (user: AdminUser) => {
  user.status = 'active'
  uiStore.showToast({ message: `User ${user.name} unsuspended`, type: 'success' })
}

const createContent = () => {
  uiStore.showToast({ message: 'Create content feature coming soon', type: 'info' })
}

const editContent = (content: ContentItem) => {
  uiStore.showToast({ message: `Editing ${content.title}`, type: 'info' })
}

const deleteContent = (content: ContentItem) => {
  const index = contentItems.value.findIndex(item => item.id === content.id)
  if (index > -1) {
    contentItems.value.splice(index, 1)
    uiStore.showToast({ message: `${content.title} deleted`, type: 'success' })
  }
}

const toggleContentStatus = (content: ContentItem) => {
  content.status = content.status === 'published' ? 'draft' : 'published'
  uiStore.showToast({ message: `${content.title} ${content.status}`, type: 'success' })
}

const resetSettings = () => {
  // Reset to default values
  systemSettings.value = {
    siteName: 'LemonNPie',
    siteDescription: 'Nigerian Movie Review Platform',
    maintenanceMode: false,
    autoApproveReviews: false,
    minReviewLength: 50,
    profanityFilter: true,
    allowRegistration: true,
    emailVerification: true,
    defaultRole: 'user'
  }
  uiStore.showToast({ message: 'Settings reset to defaults', type: 'info' })
}

const saveSettings = () => {
  uiStore.showToast({ message: 'Settings saved successfully', type: 'success' })
}

onMounted(() => {
  // Check if user has admin access
  if (!authStore.user || authStore.user.role !== 'admin') {
    router.push('/')
    uiStore.showToast({ message: 'Access denied. Admin privileges required.', type: 'error' })
  }
})
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
  background: var(--bg-primary);
}

.admin-header {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 1.5rem 2rem;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1400px;
  margin: 0 auto;
}

.header-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-title .icon {
  width: 32px;
  height: 32px;
  color: var(--accent-color);
}

.header-title h1 {
  font-size: 1.75rem;
  font-weight: bold;
  color: var(--text-primary);
  margin: 0;
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
}

.action-btn:hover {
  background: var(--bg-hover);
}

.action-btn.primary {
  background: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.action-btn.primary:hover {
  background: var(--accent-hover);
}

.action-btn.small {
  padding: 0.5rem;
  font-size: 0.75rem;
}

.action-btn.danger {
  background: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

.action-btn.danger:hover {
  background: #fee2e2;
}

.action-btn.success {
  background: #f0fdf4;
  color: #16a34a;
  border-color: #bbf7d0;
}

.action-btn.success:hover {
  background: #dcfce7;
}

.action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.action-btn .icon {
  width: 16px;
  height: 16px;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.quick-actions-panel {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.quick-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  color: var(--text-primary);
}

.quick-action:hover {
  background: var(--bg-hover);
  border-color: var(--accent-color);
}

.quick-action .icon {
  width: 16px;
  height: 16px;
}

.admin-nav {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
  padding: 0 2rem;
  display: flex;
  gap: 0.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.nav-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 1.5rem;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.875rem;
  font-weight: 500;
  position: relative;
}

.nav-tab:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.nav-tab.active {
  color: var(--accent-color);
  border-bottom-color: var(--accent-color);
}

.nav-tab .icon {
  width: 16px;
  height: 16px;
}

.tab-badge {
  background: var(--accent-color);
  color: white;
  font-size: 0.75rem;
  padding: 0.125rem 0.375rem;
  border-radius: 10px;
  min-width: 18px;
  text-align: center;
}

.admin-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.tab-content {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.section-actions {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-box .icon {
  position: absolute;
  left: 0.75rem;
  width: 16px;
  height: 16px;
  color: var(--text-secondary);
}

.search-input {
  padding: 0.5rem 0.75rem 0.5rem 2.5rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 0.875rem;
  width: 250px;
}

.filter-select {
  padding: 0.5rem 0.75rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 0.875rem;
  cursor: pointer;
}

.users-table {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  overflow: hidden;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1.5fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1.5fr;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  align-items: center;
}

.table-row:last-child {
  border-bottom: none;
}

.table-row:hover {
  background: var(--bg-hover);
}

.user-cell {
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

.user-info {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.user-email {
  color: var(--text-secondary);
  font-size: 0.75rem;
}

.role-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.role-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.role-badge.user {
  background: #f3f4f6;
  color: #374151;
}

.role-badge.critic {
  background: #fef3c7;
  color: #d97706;
}

.role-badge.admin {
  background: #dbeafe;
  color: #2563eb;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status-badge.active {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.suspended {
  background: #fee2e2;
  color: #991b1b;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.reviews-cell,
.joined-cell {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.content-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
}

.content-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.2s ease;
}

.content-card:hover {
  border-color: var(--accent-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.content-type {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.content-type.movie {
  background: #dbeafe;
  color: #2563eb;
}

.content-type.tv {
  background: #f3e8ff;
  color: #7c3aed;
}

.content-type.article {
  background: #d1fae5;
  color: #065f46;
}

.content-type.announcement {
  background: #fef3c7;
  color: #d97706;
}

.content-actions {
  display: flex;
  gap: 0.5rem;
}

.content-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.5rem 0;
}

.content-description {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0 0 1rem 0;
  line-height: 1.5;
}

.content-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: var(--text-secondary);
  font-size: 0.75rem;
}

.meta-item .icon {
  width: 12px;
  height: 12px;
}

.content-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color);
}

.content-status {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
}

.content-status.draft {
  background: #f3f4f6;
  color: #374151;
}

.content-status.published {
  background: #d1fae5;
  color: #065f46;
}

.content-status.archived {
  background: #fee2e2;
  color: #991b1b;
}

.settings-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.settings-section {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
}

.settings-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 1rem 0;
}

.setting-group {
  margin-bottom: 1rem;
}

.setting-label {
  display: block;
  color: var(--text-primary);
  font-weight: 500;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.setting-input,
.setting-select {
  width: 100%;
  padding: 0.75rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.setting-textarea {
  width: 100%;
  padding: 0.75rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-primary);
  font-size: 0.875rem;
  min-height: 80px;
  resize: vertical;
}

.toggle-switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  transition: 0.4s;
  border-radius: 24px;
}

.toggle-slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: 0.4s;
  border-radius: 50%;
}

input:checked + .toggle-slider {
  background-color: var(--accent-color);
}

input:checked + .toggle-slider:before {
  transform: translateX(20px);
}

.settings-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding: 1.5rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

@media (max-width: 1024px) {
  .admin-content {
    padding: 1rem;
  }
  
  .header-content {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .admin-nav {
    overflow-x: auto;
    padding: 0 1rem;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 2fr 1fr 1fr 2fr;
  }
  
  .reviews-cell,
  .joined-cell {
    display: none;
  }
  
  .content-grid {
    grid-template-columns: 1fr;
  }
  
  .settings-sections {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .admin-header {
    padding: 1rem;
  }
  
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .quick-actions-panel {
    flex-direction: column;
  }
  
  .section-actions {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-input {
    width: 100%;
  }
  
  .table-header,
  .table-row {
    grid-template-columns: 1fr 1fr;
    gap: 0.5rem;
  }
  
  .role-cell,
  .status-cell {
    display: none;
  }
  
  .settings-actions {
    flex-direction: column;
  }
}
</style>