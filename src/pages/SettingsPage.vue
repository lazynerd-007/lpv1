<template>
  <div class="settings-page min-h-screen bg-theme-background py-8">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Page Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Settings</h1>
        <p class="mt-2 text-gray-600 dark:text-gray-400">Manage your account preferences and privacy settings</p>
      </div>

      <!-- Settings Navigation -->
      <div class="mb-8">
        <nav class="flex space-x-8 border-b border-gray-200 dark:border-gray-700">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activeTab = tab.id"
            :class="[
              'py-2 px-1 border-b-2 font-medium text-sm transition-colors',
              activeTab === tab.id
                ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- Settings Content -->
      <div class="bg-theme-card shadow rounded-lg">
        <!-- Profile Information -->
        <div v-if="activeTab === 'profile'" class="p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">Profile Information</h2>
          
          <div class="space-y-6">
            <!-- Avatar Section -->
            <div class="flex items-center space-x-6">
              <div class="relative">
                <img
                  :src="profileData.avatar || '/default-avatar.png'"
                  alt="Profile picture"
                  class="w-20 h-20 rounded-full object-cover border-4 border-gray-200 dark:border-gray-600"
                />
                <button class="absolute bottom-0 right-0 bg-blue-500 hover:bg-blue-600 text-white p-2 rounded-full shadow-lg transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                </button>
              </div>
              <div>
                <h3 class="text-lg font-medium text-gray-900 dark:text-white">Profile Picture</h3>
                <p class="text-sm text-gray-500 dark:text-gray-400">Update your profile picture</p>
              </div>
            </div>

            <!-- Personal Information -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Full Name</label>
                <input
                  v-model="profileData.name"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Location</label>
                <input
                  v-model="profileData.location"
                  type="text"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  placeholder="e.g., Lagos, Nigeria"
                />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email</label>
                <input
                  v-model="profileData.email"
                  type="email"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                />
              </div>
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Bio</label>
                <textarea
                  v-model="profileData.bio"
                  rows="4"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  placeholder="Tell us about yourself..."
                ></textarea>
              </div>
            </div>

            <!-- Save Button -->
            <div class="flex justify-end">
              <button
                @click="saveProfile"
                class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md font-medium transition-colors"
              >
                Save Changes
              </button>
            </div>
          </div>
        </div>

        <!-- Notification Preferences -->
        <div v-if="activeTab === 'notifications'" class="p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">Notification Preferences</h2>
          
          <div class="space-y-6">
            <!-- Email Notifications -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Email Notifications</h3>
              <div class="space-y-4">
                <div v-for="notification in emailNotifications" :key="notification.id" class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ notification.title }}</h4>
                    <p class="text-sm text-gray-500 dark:text-gray-400">{{ notification.description }}</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      v-model="notification.enabled"
                      type="checkbox"
                      class="sr-only peer"
                    />
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>

            <!-- Push Notifications -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Push Notifications</h3>
              <div class="space-y-4">
                <div v-for="notification in pushNotifications" :key="notification.id" class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ notification.title }}</h4>
                    <p class="text-sm text-gray-500 dark:text-gray-400">{{ notification.description }}</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      v-model="notification.enabled"
                      type="checkbox"
                      class="sr-only peer"
                    />
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>

            <!-- Save Button -->
            <div class="flex justify-end">
              <button
                @click="saveNotifications"
                class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md font-medium transition-colors"
              >
                Save Preferences
              </button>
            </div>
          </div>
        </div>

        <!-- Privacy Settings -->
        <div v-if="activeTab === 'privacy'" class="p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">Privacy Settings</h2>
          
          <div class="space-y-6">
            <!-- Profile Visibility -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Profile Visibility</h3>
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Who can see your profile?</label>
                  <select
                    v-model="privacySettings.profileVisibility"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  >
                    <option value="public">Everyone</option>
                    <option value="friends">Friends only</option>
                    <option value="private">Only me</option>
                  </select>
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Who can see your watchlist?</label>
                  <select
                    v-model="privacySettings.watchlistVisibility"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  >
                    <option value="public">Everyone</option>
                    <option value="friends">Friends only</option>
                    <option value="private">Only me</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Data & Analytics -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Data & Analytics</h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">Analytics Tracking</h4>
                    <p class="text-sm text-gray-500 dark:text-gray-400">Allow us to collect anonymous usage data to improve our service</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      v-model="privacySettings.analyticsTracking"
                      type="checkbox"
                      class="sr-only peer"
                    />
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>
                <div class="flex items-center justify-between">
                  <div>
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">Personalized Recommendations</h4>
                    <p class="text-sm text-gray-500 dark:text-gray-400">Use your viewing history to suggest movies and shows</p>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input
                      v-model="privacySettings.personalizedRecommendations"
                      type="checkbox"
                      class="sr-only peer"
                    />
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"></div>
                  </label>
                </div>
              </div>
            </div>

            <!-- Save Button -->
            <div class="flex justify-end">
              <button
                @click="savePrivacy"
                class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md font-medium transition-colors"
              >
                Save Settings
              </button>
            </div>
          </div>
        </div>

        <!-- Account Management -->
        <div v-if="activeTab === 'account'" class="p-6">
          <h2 class="text-xl font-semibold text-gray-900 dark:text-white mb-6">Account Management</h2>
          
          <div class="space-y-8">
            <!-- Password Change -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Change Password</h3>
              <div class="space-y-4 max-w-md">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Current Password</label>
                  <input
                    v-model="passwordData.current"
                    type="password"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">New Password</label>
                  <input
                    v-model="passwordData.new"
                    type="password"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Confirm New Password</label>
                  <input
                    v-model="passwordData.confirm"
                    type="password"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                  />
                </div>
                <button
                  @click="changePassword"
                  class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-md font-medium transition-colors"
                >
                  Update Password
                </button>
              </div>
            </div>

            <!-- Two-Factor Authentication -->
            <div>
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Two-Factor Authentication</h3>
              <div class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-600 rounded-lg">
                <div>
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white">Enable 2FA</h4>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Add an extra layer of security to your account</p>
                </div>
                <button
                  @click="toggle2FA"
                  :class="[
                    'px-4 py-2 rounded-md font-medium transition-colors',
                    accountSettings.twoFactorEnabled
                      ? 'bg-red-500 hover:bg-red-600 text-white'
                      : 'bg-green-500 hover:bg-green-600 text-white'
                  ]"
                >
                  {{ accountSettings.twoFactorEnabled ? 'Disable' : 'Enable' }}
                </button>
              </div>
            </div>

            <!-- Role Management (Admin Only) -->
            <div v-if="userStore.isAdmin()" class="border-t border-gray-200 dark:border-gray-700 pt-6">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Role Management</h3>
              <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 mb-4">
                <div class="flex items-center mb-2">
                  <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
                  </svg>
                  <h4 class="text-sm font-medium text-blue-800 dark:text-blue-200">Administrator Access</h4>
                </div>
                <p class="text-sm text-blue-700 dark:text-blue-300">
                  As an administrator, you can assign roles to users. The 'Critic' role grants exclusive access to submit professional critiques.
                </p>
              </div>
              
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Your Current Role</label>
                  <div class="flex items-center space-x-2">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300">
                      <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clip-rule="evenodd" />
                        <path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z" />
                      </svg>
                      {{ userStore.currentUser?.role ? userStore.currentUser.role.charAt(0).toUpperCase() + userStore.currentUser.role.slice(1) : 'User' }}
                    </span>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Assign Role to User</label>
                  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <input
                      v-model="roleManagement.userId"
                      type="text"
                      placeholder="User ID or Email"
                      class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    />
                    <select
                      v-model="roleManagement.selectedRole"
                      class="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white"
                    >
                      <option value="">Select Role</option>
                      <option value="user">User</option>
                      <option value="critic">Critic</option>
                      <option value="moderator">Moderator</option>
                      <option value="admin">Admin</option>
                    </select>
                    <button
                      @click="assignRole"
                      :disabled="!roleManagement.userId || !roleManagement.selectedRole || isAssigningRole"
                      class="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white px-4 py-2 rounded-md font-medium transition-colors"
                    >
                      <span v-if="isAssigningRole" class="flex items-center justify-center">
                        <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Assigning...
                      </span>
                      <span v-else>Assign Role</span>
                    </button>
                  </div>
                </div>
                
                <div class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
                  <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">Role Descriptions</h4>
                  <div class="space-y-2 text-xs text-gray-600 dark:text-gray-400">
                    <div><strong>User:</strong> Standard access to browse and review movies</div>
                    <div><strong>Critic:</strong> Can submit professional critiques and reviews</div>
                    <div><strong>Moderator:</strong> Can moderate content and manage user reports</div>
                    <div><strong>Admin:</strong> Full system access including user and role management</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Account Deletion -->
            <div class="border-t border-gray-200 dark:border-gray-700 pt-6">
              <h3 class="text-lg font-medium text-red-600 dark:text-red-400 mb-4">Danger Zone</h3>
              <div class="border border-red-200 dark:border-red-800 rounded-lg p-4">
                <h4 class="text-sm font-medium text-red-900 dark:text-red-100 mb-2">Delete Account</h4>
                <p class="text-sm text-red-700 dark:text-red-300 mb-4">
                  Once you delete your account, there is no going back. Please be certain.
                </p>
                <button
                  @click="showDeleteConfirmation = true"
                  class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md font-medium transition-colors"
                >
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteConfirmation" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">Confirm Account Deletion</h3>
        <p class="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Are you sure you want to delete your account? This action cannot be undone and all your data will be permanently removed.
        </p>
        <div class="flex space-x-4">
          <button
            @click="showDeleteConfirmation = false"
            class="flex-1 bg-gray-300 hover:bg-gray-400 text-gray-800 px-4 py-2 rounded-md font-medium transition-colors"
          >
            Cancel
          </button>
          <button
            @click="deleteAccount"
            class="flex-1 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-md font-medium transition-colors"
          >
            Delete Account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import { useNotificationStore } from '../stores/notificationStore'

const router = useRouter()
const userStore = useUserStore()
const notificationStore = useNotificationStore()

// Active tab state
const activeTab = ref('profile')

// Tab configuration
const tabs = [
  { id: 'profile', name: 'Profile' },
  { id: 'notifications', name: 'Notifications' },
  { id: 'privacy', name: 'Privacy' },
  { id: 'account', name: 'Account' }
]

// Profile data
const profileData = reactive({
  avatar: userStore.currentUser?.avatar || '',
  name: userStore.currentUser?.name || '',
  email: userStore.currentUser?.email || '',
  bio: userStore.currentUser?.bio || '',
  location: userStore.currentUser?.location || ''
})

// Email notifications
const emailNotifications = reactive([
  {
    id: 'new-reviews',
    title: 'New Reviews',
    description: 'Get notified when someone reviews a movie you\'ve watched',
    enabled: true
  },
  {
    id: 'watchlist-updates',
    title: 'Watchlist Updates',
    description: 'Notifications about new releases in your watchlist',
    enabled: true
  },
  {
    id: 'recommendations',
    title: 'Recommendations',
    description: 'Weekly personalized movie recommendations',
    enabled: false
  },
  {
    id: 'newsletter',
    title: 'Newsletter',
    description: 'Monthly newsletter with movie news and updates',
    enabled: true
  }
])

// Push notifications
const pushNotifications = reactive([
  {
    id: 'instant-reviews',
    title: 'Instant Reviews',
    description: 'Real-time notifications for new reviews',
    enabled: false
  },
  {
    id: 'friend-activity',
    title: 'Friend Activity',
    description: 'When friends add movies to their watchlist',
    enabled: true
  },
  {
    id: 'trending',
    title: 'Trending Movies',
    description: 'Notifications about trending movies and shows',
    enabled: true
  }
])

// Privacy settings
const privacySettings = reactive({
  profileVisibility: 'public',
  watchlistVisibility: 'friends',
  analyticsTracking: true,
  personalizedRecommendations: true
})

// Account settings
const accountSettings = reactive({
  twoFactorEnabled: false
})

// Password change data
const passwordData = reactive({
  current: '',
  new: '',
  confirm: ''
})

// Modal state
const showDeleteConfirmation = ref(false)

// Role management data
const roleManagement = reactive({
  userId: '',
  selectedRole: ''
})

const isAssigningRole = ref(false)

// Methods
const saveProfile = () => {
  // Update user store with new profile data
  userStore.updateProfile(profileData)
  notificationStore.addNotification({
    type: 'success',
    title: 'Profile Updated',
    message: 'Profile updated successfully!',
    isRead: false
  })
}

const saveNotifications = () => {
  // Save notification preferences
  notificationStore.addNotification({
    type: 'success',
    title: 'Settings Saved',
    message: 'Notification preferences saved!',
    isRead: false
  })
}

const savePrivacy = () => {
  // Save privacy settings
  notificationStore.addNotification({
    type: 'success',
    title: 'Privacy Updated',
    message: 'Privacy settings updated!',
    isRead: false
  })
}

const changePassword = () => {
  if (passwordData.new !== passwordData.confirm) {
    notificationStore.addNotification({
      type: 'error',
      title: 'Password Mismatch',
      message: 'New passwords do not match!',
      isRead: false
    })
    return
  }
  
  if (passwordData.new.length < 8) {
    notificationStore.addNotification({
      type: 'error',
      title: 'Invalid Password',
      message: 'Password must be at least 8 characters long!',
      isRead: false
    })
    return
  }
  
  // Update password
  notificationStore.addNotification({
    type: 'success',
    title: 'Password Updated',
    message: 'Password updated successfully!',
    isRead: false
  })
  
  // Clear form
  passwordData.current = ''
  passwordData.new = ''
  passwordData.confirm = ''
}

const toggle2FA = () => {
  accountSettings.twoFactorEnabled = !accountSettings.twoFactorEnabled
  notificationStore.addNotification({
    type: 'success',
    title: '2FA Updated',
    message: `Two-factor authentication ${accountSettings.twoFactorEnabled ? 'enabled' : 'disabled'}!`,
    isRead: false
  })
}

const assignRole = async () => {
  if (!roleManagement.userId || !roleManagement.selectedRole) {
    notificationStore.addNotification({
      type: 'error',
      title: 'Missing Information',
      message: 'Please provide both user ID and role selection!',
      isRead: false
    })
    return
  }
  
  isAssigningRole.value = true
  
  try {
    // Simulate role assignment (in real app, this would be an API call)
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Use the assignRole method from userStore
    const success = userStore.assignRole(roleManagement.userId, roleManagement.selectedRole)
    
    if (success) {
      notificationStore.addNotification({
        type: 'success',
        title: 'Role Assigned',
        message: `Successfully assigned ${roleManagement.selectedRole} role to user ${roleManagement.userId}!`,
        isRead: false
      })
      
      // Clear form
      roleManagement.userId = ''
      roleManagement.selectedRole = ''
    } else {
      notificationStore.addNotification({
        type: 'error',
        title: 'Role Assignment Failed',
        message: 'Failed to assign role. User may not exist or you may not have permission.',
        isRead: false
      })
    }
  } catch (error) {
    notificationStore.addNotification({
      type: 'error',
      title: 'Assignment Error',
      message: 'An error occurred while assigning the role. Please try again.',
      isRead: false
    })
  } finally {
    isAssigningRole.value = false
  }
}

const deleteAccount = () => {
  // Perform account deletion
  notificationStore.addNotification({
    type: 'success',
    title: 'Account Deletion',
    message: 'Account deletion initiated. You will be logged out shortly.',
    isRead: false
  })
  
  // Close modal and redirect
  showDeleteConfirmation.value = false
  
  // Simulate logout and redirect
  setTimeout(() => {
    userStore.logout()
    router.push('/login')
  }, 2000)
}
</script>

<style scoped>
/* Custom toggle switch styles are handled by Tailwind classes */
</style>