<template>
  <div class="user-settings">
    <div class="settings-header">
      <h1 class="settings-title">Settings</h1>
      <p class="settings-subtitle">Manage your account preferences and privacy settings</p>
    </div>

    <div class="settings-container">
      <!-- Settings Navigation -->
      <div class="settings-nav">
        <button 
          v-for="section in settingSections" 
          :key="section.id"
          class="nav-item"
          :class="{ active: activeSection === section.id }"
          @click="activeSection = section.id"
        >
          <component :is="section.icon" class="nav-icon" />
          <span>{{ section.label }}</span>
        </button>
      </div>

      <!-- Settings Content -->
      <div class="settings-content">
        <!-- Profile Settings -->
        <div v-if="activeSection === 'profile'" class="settings-section">
          <h2 class="section-title">Profile Settings</h2>
          
          <div class="setting-group">
            <label class="setting-label">Profile Picture</label>
            <div class="profile-picture-setting">
              <img :src="userSettings.avatar" alt="Profile" class="current-avatar" />
              <div class="avatar-actions">
                <button class="btn-secondary" @click="uploadAvatar">Change Picture</button>
                <button class="btn-text" @click="removeAvatar">Remove</button>
              </div>
            </div>
          </div>

          <div class="setting-group">
            <label class="setting-label" for="displayName">Display Name</label>
            <input 
              id="displayName"
              v-model="userSettings.displayName" 
              type="text" 
              class="setting-input"
              placeholder="Enter your display name"
            />
          </div>

          <div class="setting-group">
            <label class="setting-label" for="bio">Bio</label>
            <textarea 
              id="bio"
              v-model="userSettings.bio" 
              class="setting-textarea"
              placeholder="Tell us about yourself..."
              rows="4"
            ></textarea>
          </div>

          <div class="setting-group">
            <label class="setting-label" for="location">Location</label>
            <input 
              id="location"
              v-model="userSettings.location" 
              type="text" 
              class="setting-input"
              placeholder="Your location"
            />
          </div>

          <div class="setting-group">
            <label class="setting-label">Preferred Languages</label>
            <div class="language-preferences">
              <div 
                v-for="language in availableLanguages" 
                :key="language.code"
                class="language-option"
              >
                <input 
                  :id="`lang-${language.code}`"
                  v-model="userSettings.preferredLanguages" 
                  :value="language.code"
                  type="checkbox" 
                  class="language-checkbox"
                />
                <label :for="`lang-${language.code}`" class="language-label">
                  {{ language.name }} ({{ language.nativeName }})
                </label>
              </div>
            </div>
          </div>
        </div>

        <!-- Notification Settings -->
        <div v-if="activeSection === 'notifications'" class="settings-section">
          <h2 class="section-title">Notification Preferences</h2>
          
          <div class="setting-group">
            <div class="setting-toggle">
              <label class="toggle-label">
                <span class="toggle-text">
                  <strong>Email Notifications</strong>
                  <small>Receive notifications via email</small>
                </span>
                <input 
                  v-model="userSettings.notifications.email" 
                  type="checkbox" 
                  class="toggle-input"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>



          <div class="setting-group">
            <label class="setting-label">Email Frequency</label>
            <select v-model="userSettings.notifications.frequency" class="setting-select">
              <option value="immediate">Immediate</option>
              <option value="daily">Daily Digest</option>
              <option value="weekly">Weekly Summary</option>
              <option value="never">Never</option>
            </select>
          </div>

          <div class="notification-types">
            <h3 class="subsection-title">Notification Types</h3>
            
            <div 
              v-for="type in notificationTypes" 
              :key="type.id"
              class="setting-toggle"
            >
              <label class="toggle-label">
                <span class="toggle-text">
                  <strong>{{ type.label }}</strong>
                  <small>{{ type.description }}</small>
                </span>
                <input 
                  v-model="userSettings.notifications.types[type.id]" 
                  type="checkbox" 
                  class="toggle-input"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>



        <!-- Display Settings -->
        <div v-if="activeSection === 'display'" class="settings-section">
          <h2 class="section-title">Display &amp; Accessibility</h2>
          
          <div class="setting-group">
            <label class="setting-label">Theme</label>
            <div class="theme-options">
              <div 
                v-for="theme in themeOptions" 
                :key="theme.value"
                class="theme-option"
                :class="{ active: userSettings.display.theme === theme.value }"
                @click="userSettings.display.theme = theme.value as 'light' | 'dark' | 'auto'"
              >
                <div class="theme-preview" :class="theme.value">
                  <div class="theme-bg"></div>
                  <div class="theme-accent"></div>
                </div>
                <span class="theme-name">{{ theme.label }}</span>
              </div>
            </div>
          </div>

          <div class="setting-group">
            <label class="setting-label">Language</label>
            <select v-model="userSettings.display.language" class="setting-select">
              <option 
                v-for="language in availableLanguages" 
                :key="language.code"
                :value="language.code"
              >
                {{ language.name }}
              </option>
            </select>
          </div>

          <div class="setting-group">
            <label class="setting-label">Font Size</label>
            <div class="font-size-control">
              <input 
                v-model="userSettings.display.fontSize" 
                type="range" 
                min="12" 
                max="20" 
                step="1" 
                class="font-size-slider"
              />
              <span class="font-size-value">{{ userSettings.display.fontSize }}px</span>
            </div>
          </div>

          <div class="setting-group">
            <div class="setting-toggle">
              <label class="toggle-label">
                <span class="toggle-text">
                  <strong>High Contrast</strong>
                  <small>Increase contrast for better visibility</small>
                </span>
                <input 
                  v-model="userSettings.display.highContrast" 
                  type="checkbox" 
                  class="toggle-input"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-group">
            <div class="setting-toggle">
              <label class="toggle-label">
                <span class="toggle-text">
                  <strong>Reduce Motion</strong>
                  <small>Minimize animations and transitions</small>
                </span>
                <input 
                  v-model="userSettings.display.reduceMotion" 
                  type="checkbox" 
                  class="toggle-input"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>

          <div class="setting-group">
            <div class="setting-toggle">
              <label class="toggle-label">
                <span class="toggle-text">
                  <strong>Auto-play Videos</strong>
                  <small>Automatically play video trailers</small>
                </span>
                <input 
                  v-model="userSettings.display.autoplayVideos" 
                  type="checkbox" 
                  class="toggle-input"
                />
                <span class="toggle-slider"></span>
              </label>
            </div>
          </div>
        </div>

        <!-- Account Settings -->
        <div v-if="activeSection === 'account'" class="settings-section">
          <h2 class="section-title">Account Management</h2>
          
          <div class="setting-group">
            <label class="setting-label" for="email">Email Address</label>
            <input 
              id="email"
              v-model="userSettings.email" 
              type="email" 
              class="setting-input"
              placeholder="your@email.com"
            />
          </div>

          <div class="setting-group">
            <label class="setting-label">Change Password</label>
            <button class="btn-secondary" @click="showChangePassword = true">
              Change Password
            </button>
          </div>

          <div class="setting-group">
            <label class="setting-label">Two-Factor Authentication</label>
            <div class="two-factor-setting">
              <span class="two-factor-status" :class="{ enabled: userSettings.twoFactorEnabled }">
                {{ userSettings.twoFactorEnabled ? 'Enabled' : 'Disabled' }}
              </span>
              <button 
                class="btn-secondary"
                @click="toggleTwoFactor"
              >
                {{ userSettings.twoFactorEnabled ? 'Disable' : 'Enable' }}
              </button>
            </div>
          </div>

          <div class="setting-group danger-zone">
            <h3 class="subsection-title danger">Danger Zone</h3>
            
            <div class="danger-actions">
              <div class="danger-action">
                <div class="danger-info">
                  <strong>Export Data</strong>
                  <small>Download a copy of your data</small>
                </div>
                <button class="btn-secondary" @click="exportData">
                  Export Data
                </button>
              </div>
              
              <div class="danger-action">
                <div class="danger-info">
                  <strong>Delete Account</strong>
                  <small>Permanently delete your account and all data</small>
                </div>
                <button class="btn-danger" @click="showDeleteAccount = true">
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Save Button -->
    <div class="settings-footer">
      <button 
        class="btn-primary save-btn"
        @click="saveSettings"
        :disabled="!hasChanges"
      >
        Save Changes
      </button>
      <button 
        class="btn-secondary"
        @click="resetSettings"
        :disabled="!hasChanges"
      >
        Reset
      </button>
    </div>

    <!-- Change Password Modal -->
    <div v-if="showChangePassword" class="modal-overlay" @click="showChangePassword = false">
      <div class="modal" @click.stop>
        <h3>Change Password</h3>
        <form @submit.prevent="changePassword">
          <input 
            v-model="passwordForm.current" 
            type="password" 
            placeholder="Current Password" 
            class="setting-input"
            required
          />
          <input 
            v-model="passwordForm.new" 
            type="password" 
            placeholder="New Password" 
            class="setting-input"
            required
          />
          <input 
            v-model="passwordForm.confirm" 
            type="password" 
            placeholder="Confirm New Password" 
            class="setting-input"
            required
          />
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="showChangePassword = false">
              Cancel
            </button>
            <button type="submit" class="btn-primary">
              Change Password
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Account Modal -->
    <div v-if="showDeleteAccount" class="modal-overlay" @click="showDeleteAccount = false">
      <div class="modal" @click.stop>
        <h3>Delete Account</h3>
        <p>This action cannot be undone. All your data will be permanently deleted.</p>
        <input 
          v-model="deleteConfirmation" 
          type="text" 
          placeholder="Type 'DELETE' to confirm" 
          class="setting-input"
        />
        <div class="modal-actions">
          <button type="button" class="btn-secondary" @click="showDeleteAccount = false">
            Cancel
          </button>
          <button 
            type="button" 
            class="btn-danger" 
            :disabled="deleteConfirmation !== 'DELETE'"
            @click="deleteAccount"
          >
            Delete Account
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useUIStore } from '@/stores/uiStore'
import { User, Bell, Shield, Monitor, Settings } from 'lucide-vue-next'

interface UserSettings {
  displayName: string
  bio: string
  location: string
  avatar: string
  email: string
  preferredLanguages: string[]
  notifications: {
    email: boolean
    push: boolean
    frequency: 'immediate' | 'daily' | 'weekly' | 'never'
    types: {
      reviews: boolean
      follows: boolean
      likes: boolean
      comments: boolean
      recommendations: boolean
    }
  }
  privacy: {
    publicProfile: boolean
    showActivity: boolean
    showReviews: boolean
    followPermission: 'everyone' | 'verified' | 'none'
    messagePermission: 'everyone' | 'followers' | 'none'
    analytics: boolean
  }
  display: {
    theme: 'light' | 'dark' | 'auto'
    language: string
    fontSize: number
    highContrast: boolean
    reduceMotion: boolean
    autoplayVideos: boolean
  }
  twoFactorEnabled: boolean
}

const userStore = useUserStore()
const uiStore = useUIStore()

const activeSection = ref('profile')
const showChangePassword = ref(false)
const showDeleteAccount = ref(false)
const deleteConfirmation = ref('')
const hasChanges = ref(false)

const passwordForm = ref({
  current: '',
  new: '',
  confirm: ''
})

const userSettings = ref<UserSettings>({
  displayName: 'John Doe',
  bio: 'Movie enthusiast and critic',
  location: 'Lagos, Nigeria',
  avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=professional%20headshot%20of%20a%20movie%20critic&image_size=square',
  email: 'john@example.com',
  preferredLanguages: ['en', 'yo'],
  notifications: {
    email: true,
    push: true,
    frequency: 'daily',
    types: {
      reviews: true,
      follows: true,
      likes: false,
      comments: true,
      recommendations: true
    }
  },
  privacy: {
    publicProfile: true,
    showActivity: true,
    showReviews: true,
    followPermission: 'everyone',
    messagePermission: 'followers',
    analytics: true
  },

  display: {
    theme: 'auto',
    language: 'en',
    fontSize: 16,
    highContrast: false,
    reduceMotion: false,
    autoplayVideos: true
  },
  twoFactorEnabled: false
})

const originalSettings = ref<UserSettings>(JSON.parse(JSON.stringify(userSettings.value)))

const settingSections = [
  { id: 'profile', label: 'Profile', icon: User },
  { id: 'notifications', label: 'Notifications', icon: Bell },
  { id: 'display', label: 'Display', icon: Monitor },
  { id: 'account', label: 'Account', icon: Settings }
]

const availableLanguages = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'yo', name: 'Yoruba', nativeName: 'Yorùbá' },
  { code: 'ig', name: 'Igbo', nativeName: 'Igbo' },
  { code: 'ha', name: 'Hausa', nativeName: 'Hausa' },
  { code: 'fr', name: 'French', nativeName: 'Français' }
]

const notificationTypes = [
  {
    id: 'reviews',
    label: 'New Reviews',
    description: 'When someone reviews a movie you\'ve watched'
  },
  {
    id: 'follows',
    label: 'New Followers',
    description: 'When someone follows you'
  },
  {
    id: 'likes',
    label: 'Review Likes',
    description: 'When someone likes your review'
  },
  {
    id: 'comments',
    label: 'Comments',
    description: 'When someone comments on your review'
  },
  {
    id: 'recommendations',
    label: 'Recommendations',
    description: 'Personalized movie recommendations'
  }
]

const themeOptions = [
  { value: 'light', label: 'Light' },
  { value: 'dark', label: 'Dark' },
  { value: 'auto', label: 'Auto' }
]

watch(
  userSettings,
  () => {
    hasChanges.value = JSON.stringify(userSettings.value) !== JSON.stringify(originalSettings.value)
  },
  { deep: true }
)

const uploadAvatar = () => {
  // Implementation for avatar upload
  uiStore.showToast({ message: 'Avatar upload feature coming soon', type: 'info' })
}

const removeAvatar = () => {
  userSettings.value.avatar = 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=default%20user%20avatar&image_size=square'
}

const toggleTwoFactor = () => {
  userSettings.value.twoFactorEnabled = !userSettings.value.twoFactorEnabled
  const status = userSettings.value.twoFactorEnabled ? 'enabled' : 'disabled'
  uiStore.showToast({ message: `Two-factor authentication ${status}`, type: 'success' })
}

const changePassword = () => {
  if (passwordForm.value.new !== passwordForm.value.confirm) {
    uiStore.showToast({ message: 'Passwords do not match', type: 'error' })
    return
  }
  
  // Implementation for password change
  uiStore.showToast({ message: 'Password changed successfully', type: 'success' })
  showChangePassword.value = false
  passwordForm.value = { current: '', new: '', confirm: '' }
}

const exportData = () => {
  // Implementation for data export
  uiStore.showToast({ message: 'Data export started. You will receive an email when ready.', type: 'info' })
}

const deleteAccount = () => {
  // Implementation for account deletion
  uiStore.showToast({ message: 'Account deletion initiated', type: 'success' })
  showDeleteAccount.value = false
}

const saveSettings = () => {
  // Implementation for saving settings
  originalSettings.value = JSON.parse(JSON.stringify(userSettings.value))
  hasChanges.value = false
  uiStore.showToast({ message: 'Settings saved successfully', type: 'success' })
}

const resetSettings = () => {
  userSettings.value = JSON.parse(JSON.stringify(originalSettings.value))
  hasChanges.value = false
  uiStore.showToast({ message: 'Settings reset', type: 'info' })
}

onMounted(() => {
  // Load user settings from store
  if (userStore.currentUser) {
    userSettings.value.displayName = userStore.currentUser.name
    userSettings.value.email = userStore.currentUser.email
    userSettings.value.avatar = userStore.currentUser.avatar
  }
})
</script>

<style scoped>
.user-settings {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.settings-header {
  margin-bottom: 2rem;
}

.settings-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.settings-subtitle {
  color: var(--text-secondary);
  font-size: 1.125rem;
}

.settings-container {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.settings-nav {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1rem;
  height: fit-content;
  position: sticky;
  top: 2rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem;
  background: none;
  border: none;
  border-radius: 8px;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 0.25rem;
}

.nav-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--accent-color);
  color: white;
}

.nav-icon {
  width: 20px;
  height: 20px;
}

.settings-content {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
}

.settings-section {
  max-width: 600px;
}

.section-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
}

.subsection-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.subsection-title.danger {
  color: #ef4444;
}

.setting-group {
  margin-bottom: 2rem;
}

.setting-label {
  display: block;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.setting-input,
.setting-textarea,
.setting-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: 1rem;
  transition: border-color 0.2s ease;
}

.setting-input:focus,
.setting-textarea:focus,
.setting-select:focus {
  outline: none;
  border-color: var(--accent-color);
}

.setting-textarea {
  resize: vertical;
  min-height: 100px;
}

.profile-picture-setting {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.current-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--border-color);
}

.avatar-actions {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.language-preferences {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 0.5rem;
}

.language-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.language-checkbox {
  width: 16px;
  height: 16px;
}

.language-label {
  color: var(--text-primary);
  cursor: pointer;
}

.setting-toggle {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem;
  background: var(--bg-tertiary);
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.toggle-label {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  cursor: pointer;
}

.toggle-text {
  display: flex;
  flex-direction: column;
}

.toggle-text strong {
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.toggle-text small {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.toggle-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: relative;
  width: 50px;
  height: 24px;
  background: var(--border-color);
  border-radius: 24px;
  transition: background 0.2s ease;
  margin-left: 1rem;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s ease;
}

.toggle-input:checked + .toggle-slider {
  background: var(--accent-color);
}

.toggle-input:checked + .toggle-slider::before {
  transform: translateX(26px);
}

.notification-types {
  margin-top: 1.5rem;
}

.theme-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  border: 2px solid var(--border-color);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-option:hover {
  border-color: var(--accent-color);
}

.theme-option.active {
  border-color: var(--accent-color);
  background: var(--bg-tertiary);
}

.theme-preview {
  width: 60px;
  height: 40px;
  border-radius: 6px;
  position: relative;
  overflow: hidden;
}

.theme-preview.light .theme-bg {
  background: #ffffff;
}

.theme-preview.light .theme-accent {
  background: #f59e0b;
}

.theme-preview.dark .theme-bg {
  background: #1f2937;
}

.theme-preview.dark .theme-accent {
  background: #f59e0b;
}

.theme-preview.auto .theme-bg {
  background: linear-gradient(45deg, #ffffff 50%, #1f2937 50%);
}

.theme-preview.auto .theme-accent {
  background: #f59e0b;
}

.theme-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.theme-accent {
  position: absolute;
  bottom: 4px;
  right: 4px;
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.theme-name {
  font-size: 0.875rem;
  color: var(--text-primary);
  font-weight: 500;
}

.font-size-control {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.font-size-slider {
  flex: 1;
  height: 6px;
  background: var(--border-color);
  border-radius: 3px;
  outline: none;
  -webkit-appearance: none;
  appearance: none;
}

.font-size-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  background: var(--accent-color);
  border-radius: 50%;
  cursor: pointer;
}

.font-size-value {
  font-weight: 600;
  color: var(--text-primary);
  min-width: 50px;
  text-align: center;
}

.two-factor-setting {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.two-factor-status {
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-weight: 600;
  font-size: 0.875rem;
  background: #fef2f2;
  color: #dc2626;
}

.two-factor-status.enabled {
  background: #f0fdf4;
  color: #16a34a;
}

.danger-zone {
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 1.5rem;
  background: #fef2f2;
}

.danger-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.danger-action {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: white;
  border-radius: 6px;
}

.danger-info strong {
  display: block;
  color: #dc2626;
  margin-bottom: 0.25rem;
}

.danger-info small {
  color: #6b7280;
}

.settings-footer {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  padding-top: 2rem;
  border-top: 1px solid var(--border-color);
}

.save-btn {
  min-width: 120px;
}

.btn-primary,
.btn-secondary,
.btn-text,
.btn-danger {
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
}

.btn-primary {
  background: var(--accent-color);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #d97706;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-secondary:hover {
  background: var(--accent-color);
  color: white;
  border-color: var(--accent-color);
}

.btn-text {
  background: none;
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
}

.btn-text:hover {
  color: var(--text-primary);
}

.btn-danger {
  background: #ef4444;
  color: white;
}

.btn-danger:hover:not(:disabled) {
  background: #dc2626;
}

.btn-danger:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--bg-secondary);
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal h3 {
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.modal p {
  color: var(--text-secondary);
  margin-bottom: 1rem;
}

.modal-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  .user-settings {
    padding: 1rem;
  }
  
  .settings-container {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .settings-nav {
    position: static;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 0.5rem;
  }
  
  .nav-item {
    flex-direction: column;
    text-align: center;
    padding: 0.5rem;
    margin-bottom: 0;
  }
  
  .nav-item span {
    font-size: 0.875rem;
  }
  
  .theme-options {
    grid-template-columns: 1fr;
  }
  
  .language-preferences {
    grid-template-columns: 1fr;
  }
  
  .settings-footer {
    flex-direction: column;
  }
  
  .modal {
    margin: 1rem;
    width: calc(100% - 2rem);
  }
  
  .modal-actions {
    flex-direction: column;
  }
}
</style>