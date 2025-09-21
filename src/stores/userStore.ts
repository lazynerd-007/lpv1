import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { mockReviews, getMovieById, type Review } from '@/data/mockMovies'
import { 
  mockUsers, 
  loginAttempts, 
  AuthError, 
  type AuthResponse, 
  type MockUser,
  type AuthAttempt,
  RATE_LIMIT_CONFIG 
} from '@/data/mockAuth'

interface User {
  id: string
  name: string
  email: string
  bio?: string
  location?: string
  joinDate: string
  avatar?: string
  role: 'user' | 'admin' | 'moderator' | 'critic'
}

interface UserStats {
  totalReviews: number
  averageRating: number
  totalLikes: number
  moviesWatched: number
}

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const watchlist = ref<string[]>([]) // Movie IDs
  const favorites = ref<string[]>([]) // Movie IDs
  const userReviews = ref<Review[]>([])

  // Mock user data
  const mockUser: User = {
    id: '1',
    name: 'Adebayo Johnson',
    email: 'adebayo@example.com',
    bio: 'Passionate Nollywood enthusiast and film critic',
    location: 'Lagos, Nigeria',
    joinDate: '2023-01-15',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20man%20profile%20picture%20professional%20headshot&image_size=square',
    role: 'admin'
  }

  // Getters
  const userStats = computed((): UserStats => {
    const reviews = userReviews.value
    const totalReviews = reviews.length
    const averageRating = totalReviews > 0 
      ? reviews.reduce((sum, review) => sum + review.lemonPieRating, 0) / totalReviews 
      : 0
    const totalLikes = reviews.reduce((sum, review) => sum + (review.helpfulnessScore || 0), 0)
    const moviesWatched = new Set(reviews.map(r => r.movieId)).size

    return {
      totalReviews,
      averageRating,
      totalLikes,
      moviesWatched
    }
  })

  const watchlistMovies = computed(() => {
    return watchlist.value.map(id => getMovieById(id)).filter(Boolean)
  })

  const favoriteMovies = computed(() => {
    return favorites.value.map(id => getMovieById(id)).filter(Boolean)
  })

  const isInWatchlist = computed(() => (movieId: string) => {
    return watchlist.value.includes(movieId)
  })

  const isInFavorites = computed(() => (movieId: string) => {
    return favorites.value.includes(movieId)
  })

  // Actions
  const login = async (email: string, password: string): Promise<AuthResponse> => {
    try {
      // Simulate network delay
      await new Promise(resolve => setTimeout(resolve, Math.random() * 1000 + 500))
      
      // Input validation
      if (!email || !password) {
        return {
          success: false,
          error: {
            type: AuthError.VALIDATION_ERROR,
            message: 'Email and password are required',
            details: { missingFields: !email ? ['email'] : ['password'] }
          }
        }
      }
      
      // Email format validation
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (!emailRegex.test(email)) {
        return {
          success: false,
          error: {
            type: AuthError.VALIDATION_ERROR,
            message: 'Please enter a valid email address',
            details: { field: 'email' }
          }
        }
      }
      
      // Check rate limiting
      const now = Date.now()
      const recentAttempts = loginAttempts.filter(
        attempt => attempt.email === email && 
        now - attempt.timestamp < RATE_LIMIT_CONFIG.ATTEMPT_WINDOW
      )
      
      if (recentAttempts.length >= RATE_LIMIT_CONFIG.MAX_ATTEMPTS) {
        return {
          success: false,
          error: {
            type: AuthError.TOO_MANY_ATTEMPTS,
            message: `Too many login attempts. Please try again in ${Math.ceil(RATE_LIMIT_CONFIG.ATTEMPT_WINDOW / 60000)} minutes.`,
            details: { 
              attempts: recentAttempts.length,
              resetTime: new Date(recentAttempts[0].timestamp + RATE_LIMIT_CONFIG.ATTEMPT_WINDOW)
            }
          }
        }
      }
      
      // Find user in mock database
      const user = mockUsers.find(u => u.email.toLowerCase() === email.toLowerCase())
      
      // Record login attempt
      const attempt: AuthAttempt = {
        email,
        timestamp: now,
        success: false,
        ip: '127.0.0.1' // Mock IP
      }
      
      if (!user) {
        loginAttempts.push(attempt)
        return {
          success: false,
          error: {
            type: AuthError.INVALID_CREDENTIALS,
            message: 'Invalid email or password',
            details: { field: 'email' }
          }
        }
      }
      
      // Check if account is locked
      if (user.lockedUntil && new Date(user.lockedUntil) > new Date()) {
        loginAttempts.push(attempt)
        const unlockTime = new Date(user.lockedUntil)
        return {
          success: false,
          error: {
            type: AuthError.ACCOUNT_LOCKED,
            message: `Account is temporarily locked. Try again after ${unlockTime.toLocaleTimeString()}.`,
            details: { 
              unlockTime,
              reason: 'Multiple failed login attempts'
            }
          }
        }
      }
      
      // Check if account is active
      if (!user.isActive) {
        loginAttempts.push(attempt)
        return {
          success: false,
          error: {
            type: AuthError.ACCOUNT_INACTIVE,
            message: 'Your account has been deactivated. Please contact support.',
            details: { 
              contactEmail: 'support@lemonpie.com',
              userId: user.id
            }
          }
        }
      }
      
      // Verify password (in real app, this would be hashed comparison)
      if (user.password !== password) {
        loginAttempts.push(attempt)
        
        // Increment failed attempts
        user.loginAttempts += 1
        
        // Lock account after max attempts
        if (user.loginAttempts >= RATE_LIMIT_CONFIG.MAX_ATTEMPTS) {
          user.lockedUntil = new Date(now + RATE_LIMIT_CONFIG.LOCKOUT_DURATION).toISOString()
          return {
            success: false,
            error: {
              type: AuthError.ACCOUNT_LOCKED,
              message: `Account locked due to multiple failed attempts. Try again in ${RATE_LIMIT_CONFIG.LOCKOUT_DURATION / 60000} minutes.`,
              details: { 
                attempts: user.loginAttempts,
                lockoutDuration: RATE_LIMIT_CONFIG.LOCKOUT_DURATION
              }
            }
          }
        }
        
        return {
          success: false,
          error: {
            type: AuthError.INVALID_CREDENTIALS,
            message: 'Invalid email or password',
            details: { 
              field: 'password',
              attemptsRemaining: RATE_LIMIT_CONFIG.MAX_ATTEMPTS - user.loginAttempts
            }
          }
        }
      }
      
      // Successful login
      attempt.success = true
      loginAttempts.push(attempt)
      
      // Reset failed attempts
      user.loginAttempts = 0
      user.lockedUntil = undefined
      user.lastLogin = new Date().toISOString()
      
      // Set authentication state
      isAuthenticated.value = true
      currentUser.value = {
        id: user.id,
        name: user.name,
        email: user.email,
        bio: user.bio || '',
        location: user.location || '',
        joinDate: user.joinDate,
        avatar: user.avatar,
        role: user.role
      }
      
      // Generate mock JWT token
      const token = `mock_jwt_${user.id}_${Date.now()}`
      
      // Store token securely (in real app, use httpOnly cookies)
      localStorage.setItem('auth_token', token)
      localStorage.setItem('user_data', JSON.stringify(currentUser.value))
      
      // Load user data
      await loadUserData()
      
      return {
        success: true,
        user: user,
        token
      }
      
    } catch (error) {
      console.error('Login error:', error)
      return {
        success: false,
        error: {
          type: AuthError.SERVER_ERROR,
          message: 'An unexpected error occurred. Please try again.',
          details: { error: error instanceof Error ? error.message : 'Unknown error' }
        }
      }
    }
  }

  const register = async (userData: {
    name: string
    email: string
    password: string
    confirmPassword: string
  }) => {
    isLoading.value = true
    error.value = null

    try {
      // Validate passwords match
      if (userData.password !== userData.confirmPassword) {
        throw new Error('Passwords do not match')
      }

      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock successful registration
      const newUser: User = {
        id: Date.now().toString(),
        name: userData.name,
        email: userData.email,
        joinDate: new Date().toISOString().split('T')[0],
        role: 'user'
      }
      
      currentUser.value = newUser
      isAuthenticated.value = true
      
      return { success: true }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Registration failed'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const logout = () => {
    // Clear authentication state
    currentUser.value = null
    isAuthenticated.value = false
    
    // Clear stored tokens and data
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
    
    // Clear user-specific data
    watchlist.value = []
    favorites.value = []
    userReviews.value = []
    error.value = null
    
    console.log('User logged out successfully')
  }

  // Check if user is authenticated on app initialization
  const checkAuthStatus = async (): Promise<boolean> => {
    try {
      const token = localStorage.getItem('auth_token')
      const userData = localStorage.getItem('user_data')
      
      if (!token || !userData) {
        return false
      }
      
      // In a real app, you would validate the token with the server
      // For mock purposes, we'll check if it's a valid format and not expired
      const tokenParts = token.split('_')
      if (tokenParts.length !== 3 || tokenParts[0] !== 'mock' || tokenParts[1] !== 'jwt') {
        logout() // Invalid token format
        return false
      }
      
      const tokenTimestamp = parseInt(tokenParts[2])
      const tokenAge = Date.now() - tokenTimestamp
      const TOKEN_EXPIRY = 24 * 60 * 60 * 1000 // 24 hours
      
      if (tokenAge > TOKEN_EXPIRY) {
        logout() // Token expired
        return false
      }
      
      // Restore user data
      const user = JSON.parse(userData)
      currentUser.value = user
      isAuthenticated.value = true
      
      // Load user data
      await loadUserData()
      
      return true
    } catch (error) {
      console.error('Auth check failed:', error)
      logout()
      return false
    }
  }

  const loadUserData = async () => {
    if (!currentUser.value) return

    try {
      // Load user reviews
      userReviews.value = mockReviews.filter(review => review.userId === currentUser.value?.id)
      
      // Load watchlist and favorites (mock data)
      watchlist.value = ['1', '3', '5'] // Mock movie IDs
      favorites.value = ['2', '4'] // Mock movie IDs
    } catch (err) {
      console.error('Failed to load user data:', err)
    }
  }

  const updateProfile = async (updates: Partial<User>) => {
    if (!currentUser.value) return { success: false, error: 'Not authenticated' }

    isLoading.value = true
    error.value = null

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      currentUser.value = { ...currentUser.value, ...updates }
      return { success: true }
    } catch (err) {
      error.value = 'Failed to update profile'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const addToWatchlist = (movieId: string) => {
    if (!watchlist.value.includes(movieId)) {
      watchlist.value.push(movieId)
    }
  }

  const removeFromWatchlist = (movieId: string) => {
    const index = watchlist.value.indexOf(movieId)
    if (index > -1) {
      watchlist.value.splice(index, 1)
    }
  }

  const toggleWatchlist = (movieId: string) => {
    if (isInWatchlist.value(movieId)) {
      removeFromWatchlist(movieId)
    } else {
      addToWatchlist(movieId)
    }
  }

  const addToFavorites = (movieId: string) => {
    if (!favorites.value.includes(movieId)) {
      favorites.value.push(movieId)
    }
  }

  const removeFromFavorites = (movieId: string) => {
    const index = favorites.value.indexOf(movieId)
    if (index > -1) {
      favorites.value.splice(index, 1)
    }
  }

  const toggleFavorites = (movieId: string) => {
    if (isInFavorites.value(movieId)) {
      removeFromFavorites(movieId)
    } else {
      addToFavorites(movieId)
    }
  }

  const addUserReview = (review: Omit<Review, 'id' | 'date' | 'userId'>) => {
    if (!currentUser.value) return

    const newReview: Review = {
      ...review,
      id: Date.now().toString(),
      createdAt: new Date().toISOString().split('T')[0],
      userId: currentUser.value.id
    }

    userReviews.value.push(newReview)
  }

  const updateUserReview = (reviewId: string, updates: Partial<Review>) => {
    const index = userReviews.value.findIndex(r => r.id === reviewId)
    if (index !== -1) {
      userReviews.value[index] = { ...userReviews.value[index], ...updates }
    }
  }

  const deleteUserReview = (reviewId: string) => {
    const index = userReviews.value.findIndex(r => r.id === reviewId)
    if (index !== -1) {
      userReviews.value.splice(index, 1)
    }
  }

  // Initialize with mock authentication for demo
  const initializeMockAuth = () => {
    currentUser.value = mockUser
    isAuthenticated.value = true
    loadUserData()
  }

  // Role management functions
  const hasRole = (role: User['role']): boolean => {
    return currentUser.value?.role === role
  }

  const isCritic = (): boolean => {
    return hasRole('critic')
  }

  const isAdmin = (): boolean => {
    return hasRole('admin')
  }

  const isModerator = (): boolean => {
    return hasRole('moderator')
  }

  const canSubmitCritique = (): boolean => {
    return isCritic() || isAdmin()
  }

  const assignRole = async (userId: string, role: User['role']) => {
    if (!isAdmin()) {
      return { success: false, error: 'Insufficient permissions' }
    }

    isLoading.value = true
    error.value = null

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 500))
      
      // If updating current user's role
      if (currentUser.value?.id === userId) {
        currentUser.value.role = role
      }
      
      return { success: true }
    } catch (err) {
      error.value = 'Failed to assign role'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  return {
    // State
    currentUser,
    isAuthenticated,
    isLoading,
    error,
    watchlist,
    favorites,
    userReviews,
    
    // Getters
    userStats,
    watchlistMovies,
    favoriteMovies,
    isInWatchlist,
    isInFavorites,
    
    // Actions
    login,
    register,
    logout,
    checkAuthStatus,
    loadUserData,
    updateProfile,
    addToWatchlist,
    removeFromWatchlist,
    toggleWatchlist,
    addToFavorites,
    removeFromFavorites,
    toggleFavorites,
    addUserReview,
    updateUserReview,
    deleteUserReview,
    initializeMockAuth,
    
    // Role management
    hasRole,
    isCritic,
    isAdmin,
    isModerator,
    canSubmitCritique,
    assignRole
  }
})