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
            <h1 class="text-2xl font-bold text-slate-900">Reports &amp; Logs</h1>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="exportLogs"
              class="inline-flex items-center px-4 py-2 border border-slate-300 rounded-md shadow-sm text-sm font-medium text-slate-700 bg-white hover:bg-slate-50"
            >
              <Download class="w-4 h-4 mr-2" />
              Export Logs
            </button>
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
                <AlertTriangle class="h-6 w-6 text-red-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Open Reports</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ openReports }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <FileText class="h-6 w-6 text-blue-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">System Logs</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ systemLogs }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Shield class="h-6 w-6 text-green-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Security Events</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ securityEvents }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Activity class="h-6 w-6 text-purple-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">User Actions</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ userActions }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="border-b border-slate-200">
          <nav class="-mb-px flex space-x-8 px-6">
            <button
              v-for="tab in tabs"
              :key="tab.id"
              @click="activeTab = tab.id"
              :class="[
                'py-4 px-1 border-b-2 font-medium text-sm',
                activeTab === tab.id
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
              ]"
            >
              {{ tab.name }}
              <span
                v-if="tab.count"
                :class="[
                  'ml-2 py-0.5 px-2.5 rounded-full text-xs font-medium',
                  activeTab === tab.id
                    ? 'bg-blue-100 text-blue-600'
                    : 'bg-slate-100 text-slate-600'
                ]"
              >
                {{ tab.count }}
              </span>
            </button>
          </nav>
        </div>
      </div>

      <!-- User Reports Tab -->
      <div v-if="activeTab === 'reports'" class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg leading-6 font-medium text-slate-900">User Reports</h3>
            <div class="flex items-center space-x-2">
              <select
                v-model="reportFilter"
                class="border border-slate-300 rounded-md px-3 py-2 text-sm"
              >
                <option value="all">All Reports</option>
                <option value="open">Open</option>
                <option value="in_progress">In Progress</option>
                <option value="resolved">Resolved</option>
              </select>
              <div class="relative">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  v-model="searchTerm"
                  type="text"
                  placeholder="Search reports..."
                  class="pl-10 pr-3 py-2 border border-slate-300 rounded-md leading-5 bg-white placeholder-slate-500 focus:outline-none focus:placeholder-slate-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>
          </div>

          <div class="overflow-hidden">
            <table class="min-w-full divide-y divide-slate-200">
              <thead class="bg-slate-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Report
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Type
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Reporter
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Priority
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Date
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-slate-200">
                <tr v-for="report in filteredReports" :key="report.id" class="hover:bg-slate-50">
                  <td class="px-6 py-4">
                    <div class="text-sm font-medium text-slate-900">{{ report.title }}</div>
                    <div class="text-sm text-slate-500 truncate max-w-xs">{{ report.description }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getReportTypeBadgeClass(report.type)"
                    >
                      {{ report.type }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-slate-900">{{ report.reporterName }}</div>
                    <div class="text-sm text-slate-500">{{ report.reporterEmail }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getPriorityBadgeClass(report.priority)"
                    >
                      {{ report.priority }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getStatusBadgeClass(report.status)"
                    >
                      {{ report.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {{ formatDate(report.createdAt) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                      <button
                        @click="viewReport(report)"
                        class="text-blue-600 hover:text-blue-900"
                      >
                        <Eye class="w-4 h-4" />
                      </button>
                      <button
                        @click="resolveReport(report)"
                        class="text-green-600 hover:text-green-900"
                        :disabled="report.status === 'resolved'"
                      >
                        <CheckCircle class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Audit Logs Tab -->
      <div v-if="activeTab === 'audit'" class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg leading-6 font-medium text-slate-900">Audit Trail</h3>
            <div class="flex items-center space-x-2">
              <select
                v-model="auditFilter"
                class="border border-slate-300 rounded-md px-3 py-2 text-sm"
              >
                <option value="all">All Actions</option>
                <option value="user">User Actions</option>
                <option value="admin">Admin Actions</option>
                <option value="system">System Events</option>
              </select>
              <input
                v-model="dateFilter"
                type="date"
                class="border border-slate-300 rounded-md px-3 py-2 text-sm"
              />
            </div>
          </div>

          <div class="space-y-4">
            <div
              v-for="log in filteredAuditLogs"
              :key="log.id"
              class="border border-slate-200 rounded-lg p-4"
            >
              <div class="flex items-start justify-between">
                <div class="flex items-start space-x-3">
                  <div
                    class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
                    :class="getActionIconClass(log.action)"
                  >
                    <component :is="getActionIcon(log.action)" class="w-4 h-4" />
                  </div>
                  <div class="flex-1">
                    <div class="flex items-center space-x-2">
                      <span class="text-sm font-medium text-slate-900">{{ log.userName }}</span>
                      <span class="text-sm text-slate-500">{{ log.action }}</span>
                      <span
                        v-if="log.targetType"
                        class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-100 text-slate-800"
                      >
                        {{ log.targetType }}
                      </span>
                    </div>
                    <p class="text-sm text-slate-600 mt-1">{{ log.description }}</p>
                    <div class="flex items-center space-x-4 mt-2 text-xs text-slate-500">
                      <span>IP: {{ log.ipAddress }}</span>
                      <span>{{ formatDateTime(log.timestamp) }}</span>
                    </div>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <span
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                    :class="getSeverityBadgeClass(log.severity)"
                  >
                    {{ log.severity }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredAuditLogs.length === 0" class="text-center py-8">
              <FileText class="mx-auto h-12 w-12 text-slate-400" />
              <h3 class="mt-2 text-sm font-medium text-slate-900">No logs found</h3>
              <p class="mt-1 text-sm text-slate-500">
                Try adjusting your filters to see more results.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- System Logs Tab -->
      <div v-if="activeTab === 'system'" class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg leading-6 font-medium text-slate-900">System Logs</h3>
            <div class="flex items-center space-x-2">
              <select
                v-model="logLevel"
                class="border border-slate-300 rounded-md px-3 py-2 text-sm"
              >
                <option value="all">All Levels</option>
                <option value="error">Error</option>
                <option value="warning">Warning</option>
                <option value="info">Info</option>
                <option value="debug">Debug</option>
              </select>
              <button
                @click="refreshLogs"
                class="inline-flex items-center px-3 py-2 border border-slate-300 rounded-md text-sm font-medium text-slate-700 bg-white hover:bg-slate-50"
              >
                <RefreshCw class="w-4 h-4 mr-1" />
                Refresh
              </button>
            </div>
          </div>

          <div class="bg-slate-900 rounded-lg p-4 font-mono text-sm overflow-x-auto">
            <div
              v-for="log in filteredSystemLogs"
              :key="log.id"
              class="mb-2"
              :class="getLogLevelClass(log.level)"
            >
              <span class="text-slate-400">[{{ formatDateTime(log.timestamp) }}]</span>
              <span class="ml-2 font-semibold">[{{ log.level.toUpperCase() }}]</span>
              <span class="ml-2">{{ log.message }}</span>
              <div v-if="log.details" class="ml-8 mt-1 text-slate-400">
                {{ log.details }}
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="filteredSystemLogs.length === 0" class="text-center py-8 text-slate-400">
              No system logs found for the selected level.
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Report Detail Modal -->
    <div v-if="showReportModal" class="fixed inset-0 bg-slate-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-3/4 max-w-4xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-slate-900">Report Details</h3>
            <button
              @click="showReportModal = false"
              class="text-slate-400 hover:text-slate-600"
            >
              <XCircle class="w-6 h-6" />
            </button>
          </div>
          
          <div v-if="selectedReport" class="space-y-6">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-slate-700">Report Type</label>
                <p class="mt-1 text-sm text-slate-900">{{ selectedReport.type }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">Priority</label>
                <p class="mt-1 text-sm text-slate-900">{{ selectedReport.priority }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">Reporter</label>
                <p class="mt-1 text-sm text-slate-900">{{ selectedReport.reporterName }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-slate-700">Date</label>
                <p class="mt-1 text-sm text-slate-900">{{ formatDateTime(selectedReport.createdAt) }}</p>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700">Description</label>
              <p class="mt-1 text-sm text-slate-900">{{ selectedReport.description }}</p>
            </div>

            <div v-if="selectedReport.evidence">
              <label class="block text-sm font-medium text-slate-700">Evidence</label>
              <div class="mt-1 space-y-2">
                <a
                  v-for="evidence in selectedReport.evidence"
                  :key="evidence"
                  :href="evidence"
                  target="_blank"
                  class="block text-sm text-blue-600 hover:text-blue-800"
                >
                  {{ evidence }}
                </a>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Admin Notes</label>
              <textarea
                v-model="adminNotes"
                rows="4"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Add notes about this report..."
              ></textarea>
            </div>

            <div class="flex justify-end space-x-3">
              <button
                @click="showReportModal = false"
                class="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-md hover:bg-slate-50"
              >
                Close
              </button>
              <button
                @click="updateReportStatus('in_progress')"
                class="px-4 py-2 text-sm font-medium text-white bg-yellow-600 border border-transparent rounded-md hover:bg-yellow-700"
              >
                Mark In Progress
              </button>
              <button
                @click="updateReportStatus('resolved')"
                class="px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700"
              >
                Resolve
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  ArrowLeft,
  Download,
  AlertTriangle,
  FileText,
  Shield,
  Activity,
  Search,
  Eye,
  CheckCircle,
  XCircle,
  RefreshCw,
  User,
  Settings,
  Lock,
  Trash2
} from 'lucide-vue-next'

// State
const activeTab = ref('reports')
const searchTerm = ref('')
const reportFilter = ref('all')
const auditFilter = ref('all')
const dateFilter = ref('')
const logLevel = ref('all')
const showReportModal = ref(false)
const selectedReport = ref<any>(null)
const adminNotes = ref('')

const tabs = [
  { id: 'reports', name: 'User Reports', count: 12 },
  { id: 'audit', name: 'Audit Trail', count: null },
  { id: 'system', name: 'System Logs', count: null }
]

// Mock data
const userReports = ref([
  {
    id: '1',
    title: 'Inappropriate Review Content',
    description: 'User posted offensive language in movie review for "The Dark Knight"',
    type: 'Content Violation',
    reporterName: 'John Doe',
    reporterEmail: 'john.doe@email.com',
    priority: 'high',
    status: 'open',
    createdAt: '2024-01-15T10:30:00Z',
    evidence: ['https://example.com/screenshot1.png']
  },
  {
    id: '2',
    title: 'Spam Reviews',
    description: 'Multiple fake reviews from same user account',
    type: 'Spam',
    reporterName: 'Jane Smith',
    reporterEmail: 'jane.smith@email.com',
    priority: 'medium',
    status: 'in_progress',
    createdAt: '2024-01-14T15:45:00Z',
    evidence: []
  }
])

const auditLogs = ref([
  {
    id: '1',
    userName: 'Admin User',
    action: 'User Suspended',
    description: 'Suspended user account for policy violation',
    targetType: 'User',
    ipAddress: '192.168.1.100',
    timestamp: '2024-01-15T14:30:00Z',
    severity: 'high'
  },
  {
    id: '2',
    userName: 'Moderator',
    action: 'Content Approved',
    description: 'Approved flagged review after manual review',
    targetType: 'Review',
    ipAddress: '192.168.1.101',
    timestamp: '2024-01-15T13:15:00Z',
    severity: 'low'
  }
])

const systemLogs = ref([
  {
    id: '1',
    level: 'error',
    message: 'Database connection timeout',
    details: 'Connection to primary database failed after 30 seconds',
    timestamp: '2024-01-15T14:45:00Z'
  },
  {
    id: '2',
    level: 'warning',
    message: 'High memory usage detected',
    details: 'Memory usage at 85% of available capacity',
    timestamp: '2024-01-15T14:30:00Z'
  },
  {
    id: '3',
    level: 'info',
    message: 'Backup completed successfully',
    details: 'Daily backup completed in 45 minutes',
    timestamp: '2024-01-15T02:00:00Z'
  }
])

// Computed
const openReports = computed(() => userReports.value.filter(r => r.status === 'open').length)
const systemLogsCount = computed(() => systemLogs.value.length)
const securityEvents = computed(() => auditLogs.value.filter(l => l.severity === 'high').length)
const userActions = computed(() => auditLogs.value.filter(l => l.targetType === 'User').length)

const filteredReports = computed(() => {
  let filtered = userReports.value

  if (reportFilter.value !== 'all') {
    filtered = filtered.filter(report => report.status === reportFilter.value)
  }

  if (searchTerm.value) {
    const search = searchTerm.value.toLowerCase()
    filtered = filtered.filter(report =>
      report.title.toLowerCase().includes(search) ||
      report.description.toLowerCase().includes(search) ||
      report.reporterName.toLowerCase().includes(search)
    )
  }

  return filtered
})

const filteredAuditLogs = computed(() => {
  let filtered = auditLogs.value

  if (auditFilter.value !== 'all') {
    if (auditFilter.value === 'user') {
      filtered = filtered.filter(log => log.targetType === 'User')
    } else if (auditFilter.value === 'admin') {
      filtered = filtered.filter(log => log.userName.includes('Admin'))
    } else if (auditFilter.value === 'system') {
      filtered = filtered.filter(log => log.userName === 'System')
    }
  }

  if (dateFilter.value) {
    const filterDate = new Date(dateFilter.value).toDateString()
    filtered = filtered.filter(log => 
      new Date(log.timestamp).toDateString() === filterDate
    )
  }

  return filtered
})

const filteredSystemLogs = computed(() => {
  if (logLevel.value === 'all') {
    return systemLogs.value
  }
  return systemLogs.value.filter(log => log.level === logLevel.value)
})

// Methods
const exportLogs = () => {
  // TODO: Implement log export functionality
  console.log('Exporting logs...')
}

const viewReport = (report: any) => {
  selectedReport.value = report
  adminNotes.value = report.adminNotes || ''
  showReportModal.value = true
}

const resolveReport = async (report: any) => {
  if (confirm(`Are you sure you want to resolve this report?`)) {
    report.status = 'resolved'
    // TODO: Implement API call
    console.log('Resolved report:', report.id)
  }
}

const updateReportStatus = async (status: string) => {
  if (!selectedReport.value) return

  selectedReport.value.status = status
  selectedReport.value.adminNotes = adminNotes.value
  
  // TODO: Implement API call
  console.log('Updated report status:', status)
  
  showReportModal.value = false
}

const refreshLogs = () => {
  // TODO: Implement log refresh
  console.log('Refreshing system logs...')
}

const getReportTypeBadgeClass = (type: string) => {
  const classes = {
    'Content Violation': 'bg-red-100 text-red-800',
    'Spam': 'bg-yellow-100 text-yellow-800',
    'Harassment': 'bg-orange-100 text-orange-800',
    'Copyright': 'bg-purple-100 text-purple-800'
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

const getStatusBadgeClass = (status: string) => {
  const classes = {
    open: 'bg-red-100 text-red-800',
    in_progress: 'bg-yellow-100 text-yellow-800',
    resolved: 'bg-green-100 text-green-800'
  }
  return classes[status as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const getSeverityBadgeClass = (severity: string) => {
  const classes = {
    high: 'bg-red-100 text-red-800',
    medium: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }
  return classes[severity as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const getActionIconClass = (action: string) => {
  const classes = {
    'User Suspended': 'bg-red-100 text-red-600',
    'Content Approved': 'bg-green-100 text-green-600',
    'Settings Changed': 'bg-blue-100 text-blue-600',
    'Login': 'bg-slate-100 text-slate-600'
  }
  return classes[action as keyof typeof classes] || 'bg-slate-100 text-slate-600'
}

const getActionIcon = (action: string) => {
  const icons = {
    'User Suspended': User,
    'Content Approved': CheckCircle,
    'Settings Changed': Settings,
    'Login': Lock
  }
  return icons[action as keyof typeof icons] || Activity
}

const getLogLevelClass = (level: string) => {
  const classes = {
    error: 'text-red-400',
    warning: 'text-yellow-400',
    info: 'text-blue-400',
    debug: 'text-slate-400'
  }
  return classes[level as keyof typeof classes] || 'text-slate-300'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}
</script>