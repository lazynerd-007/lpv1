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
            <h1 class="text-2xl font-bold text-slate-900">Content Moderation</h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-slate-600">
              {{ pendingCount }} pending reviews
            </span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 gap-5 sm:grid-cols-4 mb-6">
        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <AlertTriangle class="h-6 w-6 text-yellow-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Pending Reviews</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ pendingCount }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <CheckCircle class="h-6 w-6 text-green-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Approved Today</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ approvedToday }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <XCircle class="h-6 w-6 text-red-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Rejected Today</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ rejectedToday }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Flag class="h-6 w-6 text-orange-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Reports</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ reportsCount }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
            <div>
              <label for="content-type" class="block text-sm font-medium text-slate-700 mb-2">
                Content Type
              </label>
              <select
                id="content-type"
                v-model="selectedContentType"
                @change="applyFilters"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Types</option>
                <option value="review">Reviews</option>
                <option value="comment">Comments</option>
                <option value="profile">Profiles</option>
              </select>
            </div>

            <div>
              <label for="status-filter" class="block text-sm font-medium text-slate-700 mb-2">
                Status
              </label>
              <select
                id="status-filter"
                v-model="selectedStatus"
                @change="applyFilters"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Status</option>
                <option value="pending">Pending</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>

            <div>
              <label for="priority-filter" class="block text-sm font-medium text-slate-700 mb-2">
                Priority
              </label>
              <select
                id="priority-filter"
                v-model="selectedPriority"
                @change="applyFilters"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Priorities</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
            </div>

            <div class="flex items-end">
              <button
                @click="clearFilters"
                class="w-full px-4 py-2 border border-slate-300 shadow-sm text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50"
              >
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Content List -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg leading-6 font-medium text-slate-900">
              Flagged Content ({{ moderationItems.length }})
            </h3>
            <div class="flex items-center space-x-2">
              <button
                v-if="selectedItems.length > 0"
                @click="bulkApprove"
                class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
              >
                <CheckCircle class="w-4 h-4 mr-2" />
                Approve ({{ selectedItems.length }})
              </button>
              <button
                v-if="selectedItems.length > 0"
                @click="bulkReject"
                class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
              >
                <XCircle class="w-4 h-4 mr-2" />
                Reject ({{ selectedItems.length }})
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="adminStore.isLoading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>

          <!-- Content Items -->
          <div v-else class="space-y-4">
            <div
              v-for="item in moderationItems"
              :key="item.id"
              class="border border-slate-200 rounded-lg p-4 hover:bg-slate-50"
            >
              <div class="flex items-start justify-between">
                <div class="flex items-start space-x-3">
                  <input
                    type="checkbox"
                    :value="item.id"
                    v-model="selectedItems"
                    class="mt-1 h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded"
                  />
                  <div class="flex-1">
                    <div class="flex items-center space-x-2 mb-2">
                      <span
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                        :class="getContentTypeBadgeClass(item.contentType)"
                      >
                        {{ item.contentType }}
                      </span>
                      <span
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                        :class="getPriorityBadgeClass(item.priority)"
                      >
                        {{ item.priority }} priority
                      </span>
                      <span class="text-xs text-slate-500">
                        {{ formatDate(item.reportedAt) }}
                      </span>
                    </div>
                    
                    <h4 class="text-sm font-medium text-slate-900 mb-2">
                      {{ item.title }}
                    </h4>
                    
                    <p class="text-sm text-slate-600 mb-3 line-clamp-3">
                      {{ item.content }}
                    </p>
                    
                    <div class="flex items-center text-xs text-slate-500 space-x-4">
                      <span>By: {{ item.authorName }}</span>
                      <span>Reports: {{ item.reportCount }}</span>
                      <span>Reason: {{ item.reportReason }}</span>
                    </div>
                  </div>
                </div>
                
                <div class="flex items-center space-x-2 ml-4">
                  <button
                    @click="viewDetails(item)"
                    class="p-2 text-slate-400 hover:text-slate-600"
                    title="View Details"
                  >
                    <Eye class="w-4 h-4" />
                  </button>
                  <button
                    @click="approveContent(item)"
                    class="p-2 text-green-600 hover:text-green-800"
                    title="Approve"
                  >
                    <CheckCircle class="w-4 h-4" />
                  </button>
                  <button
                    @click="rejectContent(item)"
                    class="p-2 text-red-600 hover:text-red-800"
                    title="Reject"
                  >
                    <XCircle class="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="moderationItems.length === 0" class="text-center py-8">
              <Shield class="mx-auto h-12 w-12 text-slate-400" />
              <h3 class="mt-2 text-sm font-medium text-slate-900">No flagged content</h3>
              <p class="mt-1 text-sm text-slate-500">
                All content has been reviewed or no reports match your filters.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Content Details Modal -->
    <div v-if="showDetailsModal" class="fixed inset-0 bg-slate-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-3/4 max-w-4xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-slate-900">Content Details</h3>
            <button
              @click="showDetailsModal = false"
              class="text-slate-400 hover:text-slate-600"
            >
              <XCircle class="w-6 h-6" />
            </button>
          </div>
          
          <div v-if="selectedItem" class="space-y-6">
            <!-- Content Info -->
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700">Content Type</label>
                <p class="mt-1 text-sm text-slate-900">{{ selectedItem.contentType }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">Author</label>
                <p class="mt-1 text-sm text-slate-900">{{ selectedItem.authorName }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">Reported At</label>
                <p class="mt-1 text-sm text-slate-900">{{ formatDate(selectedItem.reportedAt) }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">Report Count</label>
                <p class="mt-1 text-sm text-slate-900">{{ selectedItem.reportCount }}</p>
              </div>
            </div>

            <!-- Content -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Content</label>
              <div class="p-4 bg-slate-50 rounded-lg">
                <p class="text-sm text-slate-900">{{ selectedItem.content }}</p>
              </div>
            </div>

            <!-- Report Reason -->
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Report Reason</label>
              <p class="text-sm text-slate-900">{{ selectedItem.reportReason }}</p>
            </div>

            <!-- Actions -->
            <div class="flex justify-end space-x-3">
              <button
                @click="showDetailsModal = false"
                class="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-md hover:bg-slate-50"
              >
                Close
              </button>
              <button
                @click="rejectContent(selectedItem)"
                class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700"
              >
                Reject
              </button>
              <button
                @click="approveContent(selectedItem)"
                class="px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700"
              >
                Approve
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import {
  ArrowLeft,
  AlertTriangle,
  CheckCircle,
  XCircle,
  Flag,
  Eye,
  Shield
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// State
const selectedContentType = ref('')
const selectedStatus = ref('')
const selectedPriority = ref('')
const selectedItems = ref<string[]>([])
const showDetailsModal = ref(false)
const selectedItem = ref<any>(null)

// Mock data for demonstration
const moderationItems = ref([
  {
    id: '1',
    contentType: 'review',
    title: 'Review for "The Dark Knight"',
    content: 'This movie is absolutely terrible and anyone who likes it has no taste in cinema...',
    authorName: 'John Doe',
    reportedAt: '2024-01-15T10:30:00Z',
    reportCount: 3,
    reportReason: 'Inappropriate language',
    priority: 'medium',
    status: 'pending'
  },
  {
    id: '2',
    contentType: 'comment',
    title: 'Comment on "Inception" review',
    content: 'You are completely wrong about this movie. Your opinion is trash...',
    authorName: 'Jane Smith',
    reportedAt: '2024-01-15T09:15:00Z',
    reportCount: 5,
    reportReason: 'Harassment',
    priority: 'high',
    status: 'pending'
  }
])

// Computed
const pendingCount = computed(() => 
  moderationItems.value.filter(item => item.status === 'pending').length
)

const approvedToday = computed(() => 12) // Mock data
const rejectedToday = computed(() => 3) // Mock data
const reportsCount = computed(() => 8) // Mock data

// Methods
const applyFilters = () => {
  // TODO: Implement filtering logic
  console.log('Applying filters:', {
    contentType: selectedContentType.value,
    status: selectedStatus.value,
    priority: selectedPriority.value
  })
}

const clearFilters = () => {
  selectedContentType.value = ''
  selectedStatus.value = ''
  selectedPriority.value = ''
  applyFilters()
}

const viewDetails = (item: any) => {
  selectedItem.value = item
  showDetailsModal.value = true
}

const approveContent = async (item: any) => {
  await adminStore.moderateContent(item.id, 'approved', 'Content approved by moderator')
  // Remove from list or update status
  const index = moderationItems.value.findIndex(i => i.id === item.id)
  if (index !== -1) {
    moderationItems.value[index].status = 'approved'
  }
  showDetailsModal.value = false
}

const rejectContent = async (item: any) => {
  await adminStore.moderateContent(item.id, 'rejected', 'Content rejected by moderator')
  // Remove from list or update status
  const index = moderationItems.value.findIndex(i => i.id === item.id)
  if (index !== -1) {
    moderationItems.value[index].status = 'rejected'
  }
  showDetailsModal.value = false
}

const bulkApprove = async () => {
  if (confirm(`Are you sure you want to approve ${selectedItems.value.length} items?`)) {
    for (const itemId of selectedItems.value) {
      await adminStore.moderateContent(itemId, 'approved', 'Bulk approved by moderator')
    }
    selectedItems.value = []
    // Refresh the list
    applyFilters()
  }
}

const bulkReject = async () => {
  if (confirm(`Are you sure you want to reject ${selectedItems.value.length} items?`)) {
    for (const itemId of selectedItems.value) {
      await adminStore.moderateContent(itemId, 'rejected', 'Bulk rejected by moderator')
    }
    selectedItems.value = []
    // Refresh the list
    applyFilters()
  }
}

const getContentTypeBadgeClass = (type: string) => {
  const classes = {
    review: 'bg-blue-100 text-blue-800',
    comment: 'bg-green-100 text-green-800',
    profile: 'bg-purple-100 text-purple-800'
  }
  return classes[type as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const getPriorityBadgeClass = (priority: string) => {
  const classes = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }
  return classes[priority as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

// Lifecycle
onMounted(() => {
  // Load moderation data
  applyFilters()
})
</script>