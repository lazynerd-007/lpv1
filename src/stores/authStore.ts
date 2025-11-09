import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
  id: string
  email: string
  name: string
  bio?: string
  location?: string
  role: 'user' | 'critic' | 'admin' | 'moderator'
  isActive: boolean
}

interface LoginResponse {
  user: User
  tokens: {
    access_token: string
    refresh_token: string
    token_type: string
    expires_in: number
  }
}

const API_BASE_URL = 'http://localhost:8000/api/v1'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!user.value && !!accessToken.value)
  const currentUserId = computed(() => user.value?.id || null)
  const isVerifiedCritic = computed(() => user.value?.role === 'critic')
  const isAdmin = computed(() => user.value?.role === 'admin')

  // Actions
  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        
        // Handle validation errors (422)
        if (response.status === 422 && errorData.detail) {
          const validationErrors = Array.isArray(errorData.detail)
            ? errorData.detail.map((err: any) => err.msg).join(', ')
            : errorData.detail
          throw new Error(validationErrors)
        }
        
        // Handle other errors
        throw new Error(errorData.message || errorData.error || 'Login failed')
      }

      const data: LoginResponse = await response.json()
      
      user.value = data.user
      accessToken.value = data.tokens.access_token
      refreshToken.value = data.tokens.refresh_token
      
      // Store tokens in localStorage
      localStorage.setItem('auth-user', JSON.stringify(data.user))
      localStorage.setItem('access-token', data.tokens.access_token)
      if (refreshToken.value) {
        localStorage.setItem('refresh-token', refreshToken.value)
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Login failed'
      console.error('Login error:', err)
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      if (accessToken.value) {
        await fetch(`${API_BASE_URL}/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`,
            'Content-Type': 'application/json',
          },
        })
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local state regardless of API call success
      user.value = null
      accessToken.value = null
      refreshToken.value = null
      localStorage.removeItem('auth-user')
      localStorage.removeItem('access-token')
      localStorage.removeItem('refresh-token')
    }
  }

  const register = async (email: string, password: string, name: string, bio?: string, location?: string) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, name, bio, location }),
      })

      if (!response.ok) {
        const errorData = await response.json()
        
        // Handle validation errors (422)
        if (response.status === 422 && errorData.detail) {
          const validationErrors = Array.isArray(errorData.detail)
            ? errorData.detail.map((err: any) => err.msg).join(', ')
            : errorData.detail
          throw new Error(validationErrors)
        }
        
        // Handle other errors
        throw new Error(errorData.message || errorData.error || 'Registration failed')
      }

      const data: LoginResponse = await response.json()
      
      user.value = data.user
      accessToken.value = data.tokens.access_token
      refreshToken.value = data.tokens.refresh_token
      
      // Store tokens in localStorage
      localStorage.setItem('auth-user', JSON.stringify(data.user))
      localStorage.setItem('access-token', data.tokens.access_token)
      if (refreshToken.value) {
        localStorage.setItem('refresh-token', refreshToken.value)
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Registration failed'
      console.error('Registration error:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getCurrentUser = async () => {
    if (!accessToken.value) return null

    try {
      const response = await fetch(`${API_BASE_URL}/me`, {
        headers: {
          'Authorization': `Bearer ${accessToken.value}`,
        },
      })

      if (!response.ok) {
        throw new Error('Failed to get current user')
      }

      const userData = await response.json()
      user.value = userData
      return userData
    } catch (err) {
      console.error('Get current user error:', err)
      // If token is invalid, clear auth state
      logout()
      return null
    }
  }

  const initializeAuth = () => {
    const savedUser = localStorage.getItem('auth-user')
    const savedAccessToken = localStorage.getItem('access-token')
    const savedRefreshToken = localStorage.getItem('refresh-token')

    if (savedUser && savedAccessToken) {
      try {
        user.value = JSON.parse(savedUser)
        accessToken.value = savedAccessToken
        refreshToken.value = savedRefreshToken
        
        // Verify token is still valid
        getCurrentUser()
      } catch (err) {
        console.error('Failed to parse saved auth data:', err)
        logout()
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
    accessToken,
    refreshToken,
    
    // Getters
    isAuthenticated,
    currentUserId,
    isVerifiedCritic,
    isAdmin,
    
    // Actions
    login,
    register,
    logout,
    getCurrentUser,
    initializeAuth
  }
})