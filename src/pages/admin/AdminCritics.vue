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
            <h1 class="text-2xl font-bold text-slate-900">Critic Management</h1>
          </div>
          <div class="flex items-center space-x-4">
            <span class="text-sm text-slate-600">
              {{ pendingApplications }} pending applications
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
                <Award class="h-6 w-6 text-blue-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Active Critics</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ activeCritics }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Clock class="h-6 w-6 text-yellow-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Pending Applications</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ pendingApplications }}</dd>
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
                  <dt class="text-sm font-medium text-slate-500 truncate">Approved This Month</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ approvedThisMonth }}</dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white overflow-hidden shadow rounded-lg">
          <div class="p-5">
            <div class="flex items-center">
              <div class="flex-shrink-0">
                <Star class="h-6 w-6 text-purple-400" />
              </div>
              <div class="ml-5 w-0 flex-1">
                <dl>
                  <dt class="text-sm font-medium text-slate-500 truncate">Avg. Rating</dt>
                  <dd class="text-lg font-medium text-slate-900">{{ averageRating }}</dd>
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

      <!-- Active Critics Tab -->
      <div v-if="activeTab === 'active'" class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg leading-6 font-medium text-slate-900">Active Critics</h3>
            <div class="flex items-center space-x-2">
              <div class="relative">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  v-model="searchTerm"
                  type="text"
                  placeholder="Search critics..."
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
                    Critic
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Specialization
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Reviews
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Rating
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Joined
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-slate-200">
                <tr v-for="critic in activeCriticsList" :key="critic.id" class="hover:bg-slate-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-10 w-10">
                        <img
                          :src="critic.avatar"
                          :alt="critic.name"
                          class="h-10 w-10 rounded-full object-cover"
                        />
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-slate-900">{{ critic.name }}</div>
                        <div class="text-sm text-slate-500">{{ critic.email }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex flex-wrap gap-1">
                      <span
                        v-for="spec in critic.specializations"
                        :key="spec"
                        class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                      >
                        {{ spec }}
                      </span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                    {{ critic.reviewCount }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <Star class="w-4 h-4 mr-1 text-yellow-400" />
                      <span class="text-sm text-slate-900">{{ critic.rating }}</span>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getStatusBadgeClass(critic.status)"
                    >
                      {{ critic.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {{ formatDate(critic.joinedAt) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                      <button
                        @click="viewCriticProfile(critic)"
                        class="text-blue-600 hover:text-blue-900"
                      >
                        <Eye class="w-4 h-4" />
                      </button>
                      <button
                        @click="suspendCritic(critic)"
                        class="text-red-600 hover:text-red-900"
                        :disabled="critic.status === 'suspended'"
                      >
                        <Ban class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Pending Applications Tab -->
      <div v-if="activeTab === 'applications'" class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-slate-900 mb-4">Pending Applications</h3>
          
          <div class="space-y-6">
            <div
              v-for="application in pendingApplicationsList"
              :key="application.id"
              class="border border-slate-200 rounded-lg p-6"
            >
              <div class="flex items-start justify-between">
                <div class="flex items-start space-x-4">
                  <img
                    :src="application.avatar"
                    :alt="application.name"
                    class="h-12 w-12 rounded-full object-cover"
                  />
                  <div class="flex-1">
                    <h4 class="text-lg font-medium text-slate-900">{{ application.name }}</h4>
                    <p class="text-sm text-slate-500 mb-2">{{ application.email }}</p>
                    
                    <div class="mb-4">
                      <h5 class="text-sm font-medium text-slate-700 mb-2">Specializations:</h5>
                      <div class="flex flex-wrap gap-2">
                        <span
                          v-for="spec in application.requestedSpecializations"
                          :key="spec"
                          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-100 text-slate-800"
                        >
                          {{ spec }}
                        </span>
                      </div>
                    </div>

                    <div class="mb-4">
                      <h5 class="text-sm font-medium text-slate-700 mb-2">Experience:</h5>
                      <p class="text-sm text-slate-600">{{ application.experience }}</p>
                    </div>

                    <div class="mb-4">
                      <h5 class="text-sm font-medium text-slate-700 mb-2">Portfolio/Samples:</h5>
                      <div class="space-y-1">
                        <a
                          v-for="link in application.portfolioLinks"
                          :key="link"
                          :href="link"
                          target="_blank"
                          class="block text-sm text-blue-600 hover:text-blue-800"
                        >
                          {{ link }}
                        </a>
                      </div>
                    </div>

                    <div class="text-xs text-slate-500">
                      Applied: {{ formatDate(application.appliedAt) }}
                    </div>
                  </div>
                </div>

                <div class="flex space-x-2 ml-4">
                  <button
                    @click="approveApplication(application)"
                    class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-green-600 hover:bg-green-700"
                  >
                    <CheckCircle class="w-4 h-4 mr-1" />
                    Approve
                  </button>
                  <button
                    @click="rejectApplication(application)"
                    class="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
                  >
                    <XCircle class="w-4 h-4 mr-1" />
                    Reject
                  </button>
                </div>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="pendingApplicationsList.length === 0" class="text-center py-8">
              <UserCheck class="mx-auto h-12 w-12 text-slate-400" />
              <h3 class="mt-2 text-sm font-medium text-slate-900">No pending applications</h3>
              <p class="mt-1 text-sm text-slate-500">
                All critic applications have been reviewed.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Application Review Modal -->
    <div v-if="showReviewModal" class="fixed inset-0 bg-slate-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-3/4 max-w-2xl shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-medium text-slate-900">Review Application</h3>
            <button
              @click="showReviewModal = false"
              class="text-slate-400 hover:text-slate-600"
            >
              <XCircle class="w-6 h-6" />
            </button>
          </div>
          
          <div v-if="selectedApplication" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Review Notes</label>
              <textarea
                v-model="reviewNotes"
                rows="4"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                placeholder="Add notes about this application..."
              ></textarea>
            </div>

            <div class="flex justify-end space-x-3">
              <button
                @click="showReviewModal = false"
                class="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-md hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                @click="finalizeReview('rejected')"
                class="px-4 py-2 text-sm font-medium text-white bg-red-600 border border-transparent rounded-md hover:bg-red-700"
              >
                Reject
              </button>
              <button
                @click="finalizeReview('approved')"
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
import { ref, computed } from 'vue'
import {
  ArrowLeft,
  Award,
  Clock,
  CheckCircle,
  Star,
  Search,
  Eye,
  Ban,
  XCircle,
  UserCheck
} from 'lucide-vue-next'

// State
const activeTab = ref('active')
const searchTerm = ref('')
const showReviewModal = ref(false)
const selectedApplication = ref<any>(null)
const reviewNotes = ref('')

const tabs = [
  { id: 'active', name: 'Active Critics', count: 24 },
  { id: 'applications', name: 'Applications', count: 5 }
]

// Mock data
const activeCriticsList = ref([
  {
    id: '1',
    name: 'Sarah Johnson',
    email: 'sarah.johnson@email.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20woman%20critic%20portrait&image_size=square',
    specializations: ['Drama', 'Thriller'],
    reviewCount: 156,
    rating: 4.8,
    status: 'active',
    joinedAt: '2023-06-15T10:00:00Z'
  },
  {
    id: '2',
    name: 'Michael Chen',
    email: 'michael.chen@email.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20man%20critic%20portrait&image_size=square',
    specializations: ['Action', 'Sci-Fi'],
    reviewCount: 203,
    rating: 4.9,
    status: 'active',
    joinedAt: '2023-04-22T14:30:00Z'
  }
])

const pendingApplicationsList = ref([
  {
    id: '1',
    name: 'Emma Wilson',
    email: 'emma.wilson@email.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=young%20woman%20professional%20portrait&image_size=square',
    requestedSpecializations: ['Horror', 'Comedy'],
    experience: 'Film studies graduate with 3 years of experience writing for local publications. Specialized in horror and comedy genres with published reviews in CinemaScope Magazine.',
    portfolioLinks: [
      'https://cinemascope.com/author/emma-wilson',
      'https://emmawilsonreviews.blog'
    ],
    appliedAt: '2024-01-10T09:00:00Z'
  },
  {
    id: '2',
    name: 'David Rodriguez',
    email: 'david.rodriguez@email.com',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=hispanic%20man%20professional%20portrait&image_size=square',
    requestedSpecializations: ['Documentary', 'Drama'],
    experience: 'Documentary filmmaker and critic with 5 years of experience. Regular contributor to Film Quarterly and Documentary Magazine.',
    portfolioLinks: [
      'https://filmquarterly.com/author/david-rodriguez',
      'https://davidrodriguezfilms.com'
    ],
    appliedAt: '2024-01-08T16:45:00Z'
  }
])

// Computed
const activeCritics = computed(() => activeCriticsList.value.length)
const pendingApplications = computed(() => pendingApplicationsList.value.length)
const approvedThisMonth = computed(() => 8) // Mock data
const averageRating = computed(() => 4.7) // Mock data

// Methods
const viewCriticProfile = (critic: any) => {
  // TODO: Navigate to critic profile or show modal
  console.log('View critic profile:', critic.name)
}

const suspendCritic = async (critic: any) => {
  if (confirm(`Are you sure you want to suspend ${critic.name}?`)) {
    // TODO: Implement suspend logic
    console.log('Suspend critic:', critic.name)
    critic.status = 'suspended'
  }
}

const approveApplication = (application: any) => {
  selectedApplication.value = application
  showReviewModal.value = true
}

const rejectApplication = (application: any) => {
  selectedApplication.value = application
  showReviewModal.value = true
}

const finalizeReview = async (decision: 'approved' | 'rejected') => {
  if (!selectedApplication.value) return

  try {
    // TODO: Implement API call to approve/reject application
    console.log(`${decision} application for:`, selectedApplication.value.name)
    console.log('Review notes:', reviewNotes.value)

    if (decision === 'approved') {
      // Move to active critics list
      activeCriticsList.value.push({
        id: selectedApplication.value.id,
        name: selectedApplication.value.name,
        email: selectedApplication.value.email,
        avatar: selectedApplication.value.avatar,
        specializations: selectedApplication.value.requestedSpecializations,
        reviewCount: 0,
        rating: 0,
        status: 'active',
        joinedAt: new Date().toISOString()
      })
    }

    // Remove from pending applications
    const index = pendingApplicationsList.value.findIndex(app => app.id === selectedApplication.value.id)
    if (index !== -1) {
      pendingApplicationsList.value.splice(index, 1)
    }

    showReviewModal.value = false
    selectedApplication.value = null
    reviewNotes.value = ''
  } catch (error) {
    console.error('Error processing application:', error)
  }
}

const getStatusBadgeClass = (status: string) => {
  const classes = {
    active: 'bg-green-100 text-green-800',
    suspended: 'bg-red-100 text-red-800',
    pending: 'bg-yellow-100 text-yellow-800'
  }
  return classes[status as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}
</script>