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
            <h1 class="text-2xl font-bold text-slate-900">System Settings</h1>
          </div>
          <div class="flex items-center space-x-4">
            <button
              @click="saveAllSettings"
              :disabled="!hasUnsavedChanges"
              class="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed"
            >
              <Save class="w-4 h-4 mr-2" />
              Save Changes
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="grid grid-cols-1 gap-6 lg:grid-cols-4">
        <!-- Settings Navigation -->
        <div class="lg:col-span-1">
          <nav class="bg-white shadow rounded-lg">
            <div class="p-4">
              <h3 class="text-sm font-medium text-slate-900 mb-4">Settings Categories</h3>
              <ul class="space-y-1">
                <li v-for="category in settingsCategories" :key="category.id">
                  <button
                    @click="activeCategory = category.id"
                    :class="[
                      'w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors',
                      activeCategory === category.id
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                    ]"
                  >
                    <component :is="category.icon" class="w-4 h-4 inline mr-2" />
                    {{ category.name }}
                  </button>
                </li>
              </ul>
            </div>
          </nav>
        </div>

        <!-- Settings Content -->
        <div class="lg:col-span-3">
          <!-- General Settings -->
          <div v-if="activeCategory === 'general'" class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-slate-900 mb-6">General Settings</h3>
              
              <div class="space-y-6">
                <!-- Site Information -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Site Information</h4>
                  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                      <label for="site-name" class="block text-sm font-medium text-slate-700 mb-2">
                        Site Name
                      </label>
                      <input
                        id="site-name"
                        v-model="settings.general.siteName"
                        type="text"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label for="site-tagline" class="block text-sm font-medium text-slate-700 mb-2">
                        Site Tagline
                      </label>
                      <input
                        id="site-tagline"
                        v-model="settings.general.siteTagline"
                        type="text"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <!-- Contact Information -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Contact Information</h4>
                  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                      <label for="admin-email" class="block text-sm font-medium text-slate-700 mb-2">
                        Admin Email
                      </label>
                      <input
                        id="admin-email"
                        v-model="settings.general.adminEmail"
                        type="email"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label for="support-email" class="block text-sm font-medium text-slate-700 mb-2">
                        Support Email
                      </label>
                      <input
                        id="support-email"
                        v-model="settings.general.supportEmail"
                        type="email"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <!-- Feature Toggles -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Feature Toggles</h4>
                  <div class="space-y-4">
                    <div class="flex items-center justify-between">
                      <div>
                        <label class="text-sm font-medium text-slate-700">User Registration</label>
                        <p class="text-sm text-slate-500">Allow new users to register accounts</p>
                      </div>
                      <button
                        @click="settings.general.allowRegistration = !settings.general.allowRegistration"
                        :class="[
                          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                          settings.general.allowRegistration ? 'bg-blue-600' : 'bg-slate-200'
                        ]"
                      >
                        <span
                          :class="[
                            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                            settings.general.allowRegistration ? 'translate-x-5' : 'translate-x-0'
                          ]"
                        />
                      </button>
                    </div>

                    <div class="flex items-center justify-between">
                      <div>
                        <label class="text-sm font-medium text-slate-700">Email Verification</label>
                        <p class="text-sm text-slate-500">Require email verification for new accounts</p>
                      </div>
                      <button
                        @click="settings.general.requireEmailVerification = !settings.general.requireEmailVerification"
                        :class="[
                          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                          settings.general.requireEmailVerification ? 'bg-blue-600' : 'bg-slate-200'
                        ]"
                      >
                        <span
                          :class="[
                            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                            settings.general.requireEmailVerification ? 'translate-x-5' : 'translate-x-0'
                          ]"
                        />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Security Settings -->
          <div v-if="activeCategory === 'security'" class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-slate-900 mb-6">Security Settings</h3>
              
              <div class="space-y-6">
                <!-- Password Policy -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Password Policy</h4>
                  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                      <label for="min-password-length" class="block text-sm font-medium text-slate-700 mb-2">
                        Minimum Password Length
                      </label>
                      <input
                        id="min-password-length"
                        v-model.number="settings.security.minPasswordLength"
                        type="number"
                        min="6"
                        max="50"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label for="password-expiry" class="block text-sm font-medium text-slate-700 mb-2">
                        Password Expiry (days)
                      </label>
                      <input
                        id="password-expiry"
                        v-model.number="settings.security.passwordExpiryDays"
                        type="number"
                        min="0"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <!-- Session Management -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Session Management</h4>
                  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                      <label for="session-timeout" class="block text-sm font-medium text-slate-700 mb-2">
                        Session Timeout (minutes)
                      </label>
                      <input
                        id="session-timeout"
                        v-model.number="settings.security.sessionTimeoutMinutes"
                        type="number"
                        min="5"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label for="max-login-attempts" class="block text-sm font-medium text-slate-700 mb-2">
                        Max Login Attempts
                      </label>
                      <input
                        id="max-login-attempts"
                        v-model.number="settings.security.maxLoginAttempts"
                        type="number"
                        min="1"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <!-- Security Features -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Security Features</h4>
                  <div class="space-y-4">
                    <div class="flex items-center justify-between">
                      <div>
                        <label class="text-sm font-medium text-slate-700">Two-Factor Authentication</label>
                        <p class="text-sm text-slate-500">Require 2FA for admin accounts</p>
                      </div>
                      <button
                        @click="settings.security.require2FA = !settings.security.require2FA"
                        :class="[
                          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                          settings.security.require2FA ? 'bg-blue-600' : 'bg-slate-200'
                        ]"
                      >
                        <span
                          :class="[
                            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                            settings.security.require2FA ? 'translate-x-5' : 'translate-x-0'
                          ]"
                        />
                      </button>
                    </div>

                    <div class="flex items-center justify-between">
                      <div>
                        <label class="text-sm font-medium text-slate-700">IP Whitelist</label>
                        <p class="text-sm text-slate-500">Restrict admin access to specific IP addresses</p>
                      </div>
                      <button
                        @click="settings.security.enableIPWhitelist = !settings.security.enableIPWhitelist"
                        :class="[
                          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                          settings.security.enableIPWhitelist ? 'bg-blue-600' : 'bg-slate-200'
                        ]"
                      >
                        <span
                          :class="[
                            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                            settings.security.enableIPWhitelist ? 'translate-x-5' : 'translate-x-0'
                          ]"
                        />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Content Settings -->
          <div v-if="activeCategory === 'content'" class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-slate-900 mb-6">Content Settings</h3>
              
              <div class="space-y-6">
                <!-- Review Settings -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Review Settings</h4>
                  <div class="space-y-4">
                    <div class="flex items-center justify-between">
                      <div>
                        <label class="text-sm font-medium text-slate-700">Auto-approve Reviews</label>
                        <p class="text-sm text-slate-500">Automatically approve reviews from verified users</p>
                      </div>
                      <button
                        @click="settings.content.autoApproveReviews = !settings.content.autoApproveReviews"
                        :class="[
                          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                          settings.content.autoApproveReviews ? 'bg-blue-600' : 'bg-slate-200'
                        ]"
                      >
                        <span
                          :class="[
                            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                            settings.content.autoApproveReviews ? 'translate-x-5' : 'translate-x-0'
                          ]"
                        />
                      </button>
                    </div>

                    <div>
                      <label for="max-review-length" class="block text-sm font-medium text-slate-700 mb-2">
                        Maximum Review Length (characters)
                      </label>
                      <input
                        id="max-review-length"
                        v-model.number="settings.content.maxReviewLength"
                        type="number"
                        min="100"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <!-- Moderation Settings -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Content Moderation</h4>
                  <div class="space-y-4">
                    <div class="flex items-center justify-between">
                      <div>
                        <label class="text-sm font-medium text-slate-700">Profanity Filter</label>
                        <p class="text-sm text-slate-500">Automatically filter inappropriate language</p>
                      </div>
                      <button
                        @click="settings.content.enableProfanityFilter = !settings.content.enableProfanityFilter"
                        :class="[
                          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                          settings.content.enableProfanityFilter ? 'bg-blue-600' : 'bg-slate-200'
                        ]"
                      >
                        <span
                          :class="[
                            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                            settings.content.enableProfanityFilter ? 'translate-x-5' : 'translate-x-0'
                          ]"
                        />
                      </button>
                    </div>

                    <div>
                      <label for="reports-threshold" class="block text-sm font-medium text-slate-700 mb-2">
                        Auto-hide Threshold (reports)
                      </label>
                      <input
                        id="reports-threshold"
                        v-model.number="settings.content.autoHideThreshold"
                        type="number"
                        min="1"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Email Settings -->
          <div v-if="activeCategory === 'email'" class="bg-white shadow rounded-lg">
            <div class="px-4 py-5 sm:p-6">
              <h3 class="text-lg leading-6 font-medium text-slate-900 mb-6">Email Settings</h3>
              
              <div class="space-y-6">
                <!-- SMTP Configuration -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">SMTP Configuration</h4>
                  <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                      <label for="smtp-host" class="block text-sm font-medium text-slate-700 mb-2">
                        SMTP Host
                      </label>
                      <input
                        id="smtp-host"
                        v-model="settings.email.smtpHost"
                        type="text"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                    <div>
                      <label for="smtp-port" class="block text-sm font-medium text-slate-700 mb-2">
                        SMTP Port
                      </label>
                      <input
                        id="smtp-port"
                        v-model.number="settings.email.smtpPort"
                        type="number"
                        class="block w-full px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                      />
                    </div>
                  </div>
                </div>

                <!-- Email Notifications -->
                <div>
                  <h4 class="text-sm font-medium text-slate-900 mb-4">Email Notifications</h4>
                  <div class="space-y-4">
                    <div class="flex items-center justify-between">
                      <div>
                        <label class="text-sm font-medium text-slate-700">Welcome Emails</label>
                        <p class="text-sm text-slate-500">Send welcome email to new users</p>
                      </div>
                      <button
                        @click="settings.email.sendWelcomeEmails = !settings.email.sendWelcomeEmails"
                        :class="[
                          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                          settings.email.sendWelcomeEmails ? 'bg-blue-600' : 'bg-slate-200'
                        ]"
                      >
                        <span
                          :class="[
                            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                            settings.email.sendWelcomeEmails ? 'translate-x-5' : 'translate-x-0'
                          ]"
                        />
                      </button>
                    </div>

                    <div class="flex items-center justify-between">
                      <div>
                        <label class="text-sm font-medium text-slate-700">Admin Notifications</label>
                        <p class="text-sm text-slate-500">Send notifications for admin actions</p>
                      </div>
                      <button
                        @click="settings.email.sendAdminNotifications = !settings.email.sendAdminNotifications"
                        :class="[
                          'relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2',
                          settings.email.sendAdminNotifications ? 'bg-blue-600' : 'bg-slate-200'
                        ]"
                      >
                        <span
                          :class="[
                            'pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out',
                            settings.email.sendAdminNotifications ? 'translate-x-5' : 'translate-x-0'
                          ]"
                        />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import {
  ArrowLeft,
  Save,
  Settings,
  Shield,
  FileText,
  Mail,
  Database
} from 'lucide-vue-next'

// State
const activeCategory = ref('general')
const originalSettings = ref<any>({})

const settingsCategories = [
  { id: 'general', name: 'General', icon: Settings },
  { id: 'security', name: 'Security', icon: Shield },
  { id: 'content', name: 'Content', icon: FileText },
  { id: 'email', name: 'Email', icon: Mail }
]

const settings = ref({
  general: {
    siteName: 'LemonPie',
    siteTagline: 'Your Ultimate Movie & Series Review Platform',
    adminEmail: 'admin@lemonpie.com',
    supportEmail: 'support@lemonpie.com',
    allowRegistration: true,
    requireEmailVerification: true
  },
  security: {
    minPasswordLength: 8,
    passwordExpiryDays: 90,
    sessionTimeoutMinutes: 30,
    maxLoginAttempts: 5,
    require2FA: false,
    enableIPWhitelist: false
  },
  content: {
    autoApproveReviews: false,
    maxReviewLength: 5000,
    enableProfanityFilter: true,
    autoHideThreshold: 3
  },
  email: {
    smtpHost: 'smtp.gmail.com',
    smtpPort: 587,
    sendWelcomeEmails: true,
    sendAdminNotifications: true
  }
})

// Computed
const hasUnsavedChanges = computed(() => {
  return JSON.stringify(settings.value) !== JSON.stringify(originalSettings.value)
})

// Methods
const saveAllSettings = async () => {
  try {
    // TODO: Implement API call to save settings
    console.log('Saving settings:', settings.value)
    
    // Update original settings to match current
    originalSettings.value = JSON.parse(JSON.stringify(settings.value))
    
    // Show success message
    alert('Settings saved successfully!')
  } catch (error) {
    console.error('Error saving settings:', error)
    alert('Error saving settings. Please try again.')
  }
}

// Watch for changes to track unsaved state
watch(
  settings,
  () => {
    // Settings changed
  },
  { deep: true }
)

// Initialize original settings
originalSettings.value = JSON.parse(JSON.stringify(settings.value))
</script>