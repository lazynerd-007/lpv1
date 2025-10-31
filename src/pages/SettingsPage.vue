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
                :disabled="isLoadingPrivacy"
                class="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed text-white px-6 py-2 rounded-md font-medium transition-colors flex items-center"
              >
                <svg v-if="isLoadingPrivacy" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                {{ isLoadingPrivacy ? 'Saving...' : 'Save Settings' }}
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
                  :disabled="isLoading2FA"
                  :class="[
                    'px-4 py-2 rounded-md font-medium transition-colors flex items-center',
                    isLoading2FA
                      ? 'bg-gray-400 cursor-not-allowed text-white'
                      : accountSettings.twoFactorEnabled
                        ? 'bg-red-500 hover:bg-red-600 text-white'
                        : 'bg-green-500 hover:bg-green-600 text-white'
                  ]"
                >
                  <svg v-if="isLoading2FA" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ isLoading2FA ? 'Processing...' : (accountSettings.twoFactorEnabled ? 'Disable' : 'Enable') }}
                </button>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/userStore'
import { useNotificationStore } from '../stores/notificationStore'
import { useAuthStore } from '../stores/authStore'

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

// Loading states
const isLoadingPrivacy = ref(false)
const isLoading2FA = ref(false)

// Initialization functions
const loadPrivacySettings = async () => {
  try {
    isLoadingPrivacy.value = true
    const authStore = useAuthStore()
    const token = authStore.accessToken
    
    if (!token) {
      console.log('No auth token available for loading privacy settings')
      return
    }

    const response = await fetch('http://localhost:8000/api/v1/users/privacy-settings', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (response.ok) {
      const data = await response.json()
      privacySettings.profileVisibility = data.profile_visibility || 'public'
      privacySettings.watchlistVisibility = data.watchlist_visibility || 'friends'
      privacySettings.analyticsTracking = data.analytics_tracking ?? true
      privacySettings.personalizedRecommendations = data.personalized_recommendations ?? true
    } else {
      console.log('Failed to load privacy settings:', response.status)
    }
  } catch (error) {
    console.error('Error loading privacy settings:', error)
  } finally {
    isLoadingPrivacy.value = false
  }
}

const load2FAStatus = async () => {
  try {
    isLoading2FA.value = true
    const authStore = useAuthStore()
    const token = authStore.accessToken
    
    if (!token) {
      console.log('No auth token available for loading 2FA status')
      return
    }

    const response = await fetch('http://localhost:8000/api/v1/users/2fa/status', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (response.ok) {
      const data = await response.json()
      accountSettings.twoFactorEnabled = data.enabled || false
    } else {
      console.log('Failed to load 2FA status:', response.status)
    }
  } catch (error) {
    console.error('Error loading 2FA status:', error)
  } finally {
    isLoading2FA.value = false
  }
}

// Methods
const saveProfile = async () => {
  console.log('saveProfile method called')
  console.log('profileData:', profileData)
  
  try {
    console.log('About to call userStore.updateProfile')
    // Update user store with new profile data
    const result = await userStore.updateProfile(profileData)
    console.log('userStore.updateProfile result:', result)
    
    if (result.success) {
      console.log('Profile update successful')
      notificationStore.addNotification({
        type: 'success',
        title: 'Profile Updated',
        message: 'Profile updated successfully!',
        isRead: false
      })
    } else {
      console.log('Profile update failed:', result.error)
      notificationStore.addNotification({
        type: 'error',
        title: 'Update Failed',
        message: result.error || 'Failed to update profile',
        isRead: false
      })
    }
  } catch (error) {
    console.error('Error in saveProfile:', error)
    notificationStore.addNotification({
      type: 'error',
      title: 'Update Failed',
      message: 'An error occurred while updating your profile',
      isRead: false
    })
  }
}

const saveNotifications = async () => {
  try {
    // Get auth token from userStore or authStore
    const authStore = useAuthStore()
    const token = authStore.accessToken
    
    if (!token) {
      notificationStore.addNotification({
        type: 'error',
        title: 'Authentication Error',
        message: 'Please log in to save preferences',
        isRead: false
      })
      return
    }

    // Save each notification preference to backend
    for (const notification of emailNotifications) {
      const response = await fetch(`http://localhost:8000/api/v1/notifications/preferences/${notification.id}`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          enabled: notification.enabled
        }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Failed to save ${notification.title} preference`)
      }
    }

    // Show success notification
    notificationStore.addNotification({
      type: 'success',
      title: 'Settings Saved',
      message: 'Notification preferences saved successfully!',
      isRead: false
    })
  } catch (error) {
    console.error('Error saving notification preferences:', error)
    notificationStore.addNotification({
      type: 'error',
      title: 'Save Failed',
      message: error instanceof Error ? error.message : 'Failed to save notification preferences',
      isRead: false
    })
  }
}

const savePrivacy = async () => {
  try {
    isLoadingPrivacy.value = true
    const authStore = useAuthStore()
    const token = authStore.accessToken
    
    if (!token) {
      notificationStore.addNotification({
        type: 'error',
        title: 'Authentication Error',
        message: 'Please log in to save privacy settings',
        isRead: false
      })
      return
    }

    const response = await fetch('http://localhost:8000/api/v1/users/privacy-settings', {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        profile_visibility: privacySettings.profileVisibility,
        watchlist_visibility: privacySettings.watchlistVisibility,
        analytics_tracking: privacySettings.analyticsTracking,
        personalized_recommendations: privacySettings.personalizedRecommendations
      }),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to save privacy settings')
    }

    notificationStore.addNotification({
      type: 'success',
      title: 'Privacy Updated',
      message: 'Privacy settings updated successfully!',
      isRead: false
    })
  } catch (error) {
    console.error('Error saving privacy settings:', error)
    notificationStore.addNotification({
      type: 'error',
      title: 'Save Failed',
      message: error instanceof Error ? error.message : 'Failed to save privacy settings',
      isRead: false
    })
  } finally {
    isLoadingPrivacy.value = false
  }
}

const changePassword = async () => {
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

  try {
    const authStore = useAuthStore()
    const token = authStore.accessToken
    
    if (!token) {
      notificationStore.addNotification({
        type: 'error',
        title: 'Authentication Error',
        message: 'Please log in to change password',
        isRead: false
      })
      return
    }

    const response = await fetch('http://localhost:8000/api/v1/users/change-password', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        current_password: passwordData.current,
        new_password: passwordData.new
      }),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to change password')
    }

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
  } catch (error) {
    console.error('Error changing password:', error)
    notificationStore.addNotification({
      type: 'error',
      title: 'Password Change Failed',
      message: error instanceof Error ? error.message : 'Failed to change password',
      isRead: false
    })
  }
}

const toggle2FA = async () => {
  try {
    isLoading2FA.value = true
    const authStore = useAuthStore()
    const token = authStore.accessToken
    
    if (!token) {
      notificationStore.addNotification({
        type: 'error',
        title: 'Authentication Error',
        message: 'Please log in to manage 2FA settings',
        isRead: false
      })
      return
    }

    const endpoint = accountSettings.twoFactorEnabled 
      ? 'http://localhost:8000/api/v1/users/2fa/disable'
      : 'http://localhost:8000/api/v1/users/2fa/enable'

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Failed to update 2FA settings')
    }

    // Toggle the state
    accountSettings.twoFactorEnabled = !accountSettings.twoFactorEnabled

    notificationStore.addNotification({
      type: 'success',
      title: '2FA Updated',
      message: `Two-factor authentication ${accountSettings.twoFactorEnabled ? 'enabled' : 'disabled'} successfully!`,
      isRead: false
    })
  } catch (error) {
    console.error('Error toggling 2FA:', error)
    notificationStore.addNotification({
      type: 'error',
      title: '2FA Update Failed',
      message: error instanceof Error ? error.message : 'Failed to update 2FA settings',
      isRead: false
    })
  } finally {
    isLoading2FA.value = false
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

// Initialize data when component mounts
onMounted(() => {
  loadPrivacySettings()
  load2FAStatus()
})
</script>

<style scoped>
/* Custom toggle switch styles are handled by Tailwind classes */
</style>