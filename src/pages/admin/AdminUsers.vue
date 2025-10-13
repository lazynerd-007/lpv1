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
            <h1 class="text-2xl font-bold text-slate-900">User Management</h1>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="exportUsers"
              class="inline-flex items-center px-3 py-2 border border-slate-300 shadow-sm text-sm leading-4 font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50"
            >
              <Download class="w-4 h-4 mr-2" />
              Export
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Search and Filters -->
      <div class="bg-white shadow rounded-lg mb-6">
        <div class="px-4 py-5 sm:p-6">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
            <!-- Search -->
            <div class="sm:col-span-2">
              <label for="search" class="block text-sm font-medium text-slate-700 mb-2">
                Search Users
              </label>
              <div class="relative">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-slate-400" />
                <input
                  id="search"
                  v-model="searchTerm"
                  type="text"
                  placeholder="Search by name or email..."
                  class="block w-full pl-10 pr-3 py-2 border border-slate-300 rounded-md leading-5 bg-white placeholder-slate-500 focus:outline-none focus:placeholder-slate-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                  @input="debouncedSearch"
                />
              </div>
            </div>

            <!-- Role Filter -->
            <div>
              <label for="role-filter" class="block text-sm font-medium text-slate-700 mb-2">
                Role
              </label>
              <select
                id="role-filter"
                v-model="selectedRole"
                @change="applyFilters"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="">All Roles</option>
                <option value="user">User</option>
                <option value="critic">Critic</option>
                <option value="moderator">Moderator</option>
                <option value="admin">Admin</option>
              </select>
            </div>

            <!-- Status Filter -->
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
                <option value="active">Active</option>
                <option value="suspended">Suspended</option>
                <option value="banned">Banned</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Users Table -->
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg leading-6 font-medium text-slate-900">
              Users ({{ adminStore.users.length }})
            </h3>
            <div class="flex items-center space-x-2">
              <button
                v-if="selectedUsers.length > 0"
                @click="showBulkActions = !showBulkActions"
                class="inline-flex items-center px-3 py-2 border border-slate-300 shadow-sm text-sm leading-4 font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50"
              >
                <Settings class="w-4 h-4 mr-2" />
                Bulk Actions ({{ selectedUsers.length }})
              </button>
            </div>
          </div>

          <!-- Bulk Actions Panel -->
          <div v-if="showBulkActions && selectedUsers.length > 0" class="mb-4 p-4 bg-slate-50 rounded-lg">
            <div class="flex items-center space-x-4">
              <span class="text-sm font-medium text-slate-700">
                {{ selectedUsers.length }} users selected:
              </span>
              <button
                @click="bulkUpdateRole"
                class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-blue-700 bg-blue-100 hover:bg-blue-200"
              >
                Change Role
              </button>
              <button
                @click="bulkSuspend"
                class="inline-flex items-center px-3 py-1 border border-transparent text-xs font-medium rounded text-red-700 bg-red-100 hover:bg-red-200"
              >
                Suspend
              </button>
              <button
                @click="clearSelection"
                class="inline-flex items-center px-3 py-1 border border-slate-300 text-xs font-medium rounded text-slate-700 bg-white hover:bg-slate-50"
              >
                Clear Selection
              </button>
            </div>
          </div>

          <!-- Loading State -->
          <div v-if="adminStore.isLoading" class="flex justify-center py-8">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>

          <!-- Users Table -->
          <div v-else class="overflow-hidden">
            <table class="min-w-full divide-y divide-slate-200">
              <thead class="bg-slate-50">
                <tr>
                  <th class="px-6 py-3 text-left">
                    <input
                      type="checkbox"
                      :checked="allUsersSelected"
                      @change="toggleAllUsers"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded"
                    />
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    User
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Role
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Reviews
                  </th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Last Login
                  </th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-slate-200">
                <tr v-for="user in adminStore.users" :key="user.id" class="hover:bg-slate-50">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <input
                      type="checkbox"
                      :value="user.id"
                      v-model="selectedUsers"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-slate-300 rounded"
                    />
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="flex items-center">
                      <div class="flex-shrink-0 h-10 w-10">
                        <img
                          :src="user.avatar"
                          :alt="user.name"
                          class="h-10 w-10 rounded-full object-cover"
                        />
                      </div>
                      <div class="ml-4">
                        <div class="text-sm font-medium text-slate-900">{{ user.name }}</div>
                        <div class="text-sm text-slate-500">{{ user.email }}</div>
                      </div>
                    </div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getRoleBadgeClass(user.role)"
                    >
                      {{ user.role }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span
                      class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                      :class="getStatusBadgeClass(user.status)"
                    >
                      {{ user.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                    {{ user.reviewCount }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {{ formatDate(user.lastLogin) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <div class="flex justify-end space-x-2">
                      <router-link
                        :to="`/admin/users/${user.id}`"
                        class="text-blue-600 hover:text-blue-900"
                      >
                        <Eye class="w-4 h-4" />
                      </router-link>
                      <button
                        @click="editUser(user)"
                        class="text-slate-600 hover:text-slate-900"
                      >
                        <Edit class="w-4 h-4" />
                      </button>
                      <button
                        @click="suspendUser(user)"
                        class="text-red-600 hover:text-red-900"
                        :disabled="user.status === 'suspended'"
                      >
                        <Ban class="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- Empty State -->
            <div v-if="adminStore.users.length === 0" class="text-center py-8">
              <Users class="mx-auto h-12 w-12 text-slate-400" />
              <h3 class="mt-2 text-sm font-medium text-slate-900">No users found</h3>
              <p class="mt-1 text-sm text-slate-500">
                Try adjusting your search or filter criteria.
              </p>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-slate-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <h3 class="text-lg font-medium text-slate-900 mb-4">Edit User</h3>
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-slate-700 mb-2">Role</label>
              <select
                v-model="editingUser.role"
                class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              >
                <option value="user">User</option>
                <option value="critic">Critic</option>
                <option value="moderator">Moderator</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          </div>
          <div class="flex justify-end space-x-3 mt-6">
            <button
              @click="showEditModal = false"
              class="px-4 py-2 text-sm font-medium text-slate-700 bg-white border border-slate-300 rounded-md hover:bg-slate-50"
            >
              Cancel
            </button>
            <button
              @click="saveUserChanges"
              class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md hover:bg-blue-700"
            >
              Save Changes
            </button>
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
  Download,
  Search,
  Settings,
  Eye,
  Edit,
  Ban,
  Users
} from 'lucide-vue-next'

const adminStore = useAdminStore()

// State
const searchTerm = ref('')
const selectedRole = ref('')
const selectedStatus = ref('')
const selectedUsers = ref<string[]>([])
const showBulkActions = ref(false)
const showEditModal = ref(false)
const editingUser = ref<any>({})

// Computed
const allUsersSelected = computed(() => {
  return adminStore.users.length > 0 && selectedUsers.value.length === adminStore.users.length
})

// Methods
const debouncedSearch = (() => {
  let timeout: NodeJS.Timeout
  return () => {
    clearTimeout(timeout)
    timeout = setTimeout(() => {
      applyFilters()
    }, 300)
  }
})()

const applyFilters = async () => {
  await adminStore.fetchUsers({
    search: searchTerm.value,
    role: selectedRole.value,
    status: selectedStatus.value
  })
}

const toggleAllUsers = () => {
  if (allUsersSelected.value) {
    selectedUsers.value = []
  } else {
    selectedUsers.value = adminStore.users.map(user => user.id)
  }
}

const clearSelection = () => {
  selectedUsers.value = []
  showBulkActions.value = false
}

const editUser = (user: any) => {
  editingUser.value = { ...user }
  showEditModal.value = true
}

const saveUserChanges = async () => {
  await adminStore.updateUserRole(editingUser.value.id, editingUser.value.role)
  showEditModal.value = false
  await applyFilters()
}

const suspendUser = async (user: any) => {
  if (confirm(`Are you sure you want to suspend ${user.name}?`)) {
    await adminStore.suspendUser(user.id, 'Suspended by admin')
    await applyFilters()
  }
}

const bulkUpdateRole = () => {
  // TODO: Implement bulk role update
  console.log('Bulk update role for:', selectedUsers.value)
}

const bulkSuspend = () => {
  if (confirm(`Are you sure you want to suspend ${selectedUsers.value.length} users?`)) {
    // TODO: Implement bulk suspend
    console.log('Bulk suspend:', selectedUsers.value)
  }
}

const exportUsers = () => {
  // TODO: Implement user export
  console.log('Export users')
}

const getRoleBadgeClass = (role: string) => {
  const classes = {
    user: 'bg-slate-100 text-slate-800',
    critic: 'bg-blue-100 text-blue-800',
    moderator: 'bg-yellow-100 text-yellow-800',
    admin: 'bg-red-100 text-red-800'
  }
  return classes[role as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const getStatusBadgeClass = (status: string) => {
  const classes = {
    active: 'bg-green-100 text-green-800',
    suspended: 'bg-red-100 text-red-800',
    banned: 'bg-red-100 text-red-800'
  }
  return classes[status as keyof typeof classes] || 'bg-slate-100 text-slate-800'
}

const formatDate = (dateString: string) => {
  if (!dateString) return 'Never'
  return new Date(dateString).toLocaleDateString()
}

// Lifecycle
onMounted(() => {
  adminStore.fetchUsers()
})
</script>