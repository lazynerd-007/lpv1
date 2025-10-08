import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: string
  email: string
  name: string
  avatar?: string
  role: 'user' | 'critic' | 'admin'
  isVerified: boolean
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value)
  const currentUserId = computed(() => user.value?.id || null)
  const isVerifiedCritic = computed(() => user.value?.role === 'critic' && user.value?.isVerified)

  // Actions
  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null

    try {
      // Mock login - in real app this would call an API
      const mockUser: User = {
        id: 'user-123',
        email,
        name: email.split('@')[0],
        avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${email}`,
        role: 'user',
        isVerified: false
      }
      
      user.value = mockUser
      localStorage.setItem('auth-user', JSON.stringify(mockUser))
    } catch (err) {
      error.value = 'Login failed'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    user.value = null
    localStorage.removeItem('auth-user')
  }

  const initializeAuth = () => {
    const savedUser = localStorage.getItem('auth-user')
    if (savedUser) {
      try {
        user.value = JSON.parse(savedUser)
      } catch (err) {
        console.error('Failed to parse saved user:', err)
        localStorage.removeItem('auth-user')
      }
    }
  }

  // Initialize auth on store creation
  initializeAuth()

  return {
    // State
    user,
    isLoading,
    error,
    
    // Getters
    isAuthenticated,
    currentUserId,
    isVerifiedCritic,
    
    // Actions
    login,
    logout,
    initializeAuth
  }
})