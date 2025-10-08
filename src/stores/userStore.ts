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
import { useSeriesStore } from '@/stores/seriesStore'

interface User {
  id: string
  name: string
  email: string
  bio?: string
  location?: string
  joinDate: string
  avatar?: string
  role?: 'user' | 'admin' | 'moderator' | 'critic'
}

interface UserStats {
  totalReviews: number
  averageRating: number
  totalLikes: number
  moviesWatched: number
  followingCount: number
  followersCount: number
}

export interface UserActivity {
  id: string
  userId: string
  type: 'review' | 'rating' | 'follow' | 'watchlist_add' | 'favorite_add'
  targetId: string // Movie ID or User ID
  targetType: 'movie' | 'series' | 'user'
  content?: string // Review content or activity description
  rating?: number // For rating activities
  timestamp: string
  metadata?: Record<string, any>
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
  const following = ref<string[]>([]) // User IDs that current user follows
  const followers = ref<string[]>([]) // User IDs that follow current user
  const userActivities = ref<UserActivity[]>([]) // User activity feed

  // State for login and registration
  const loginError = ref<string | null>(null)
  const loginInProgress = ref(false)
  const registrationError = ref<string | null>(null)
  const registrationInProgress = ref(false)
  const profileUpdateSuccess = ref(false)
  const profileUpdateError = ref<string | null>(null)
  
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
    const followingCount = following.value.length
    const followersCount = followers.value.length

    return {
      totalReviews,
      averageRating,
      totalLikes,
      moviesWatched,
      followingCount,
      followersCount
    }
  })

  const watchlistMovies = computed(() => {
    // Initialize seriesStore
    const seriesStore = useSeriesStore()
    
    return watchlist.value.map(id => {
      // Try to get as movie first
      const movie = getMovieById(id)
      if (movie) {
        // Add type property to each movie object
        return { ...movie, type: 'movie' }
      }
      
      // If not found as movie, try to get as series
      const series = seriesStore.getSeriesById(id)
      if (series) {
        // Add type property to each series object
        return { ...series, type: 'series' }
      }
      
      return null
    }).filter(Boolean)
  })

  const favoriteMovies = computed(() => {
    // Initialize seriesStore
    const seriesStore = useSeriesStore()
    
    return favorites.value.map(id => {
      // Try to get as movie first
      const movie = getMovieById(id)
      if (movie) {
        // Add type property to each movie object
        return { ...movie, type: 'movie' }
      }
      
      // If not found as movie, try to get as series
      const series = seriesStore.getSeriesById(id)
      if (series) {
        // Add type property to each series object
        return { ...series, type: 'series' }
      }
      
      return null
    }).filter(Boolean)
  })

  const isInWatchlist = computed(() => (movieId: string) => {
    return watchlist.value.includes(movieId)
  })

  const isInFavorites = computed(() => (movieId: string) => {
    return favorites.value.includes(movieId)
  })

  const isFollowing = computed(() => (userId: string) => {
    return following.value.includes(userId)
  })

  const isFollowedBy = computed(() => (userId: string) => {
    return followers.value.includes(userId)
  })

  const followingUsers = computed(() => {
    return following.value.map(userId => {
      const user = mockUsers.find(u => u.id === userId)
      return user ? {
        id: user.id,
        name: user.name,
        email: user.email,
        avatar: user.avatar,
        bio: user.bio
      } : null
    }).filter(Boolean)
  })

  const followerUsers = computed(() => {
    return followers.value.map(userId => {
      const user = mockUsers.find(u => u.id === userId)
      return user ? {
        id: user.id,
        name: user.name,
        email: user.email,
        avatar: user.avatar,
        bio: user.bio
      } : null
    }).filter(Boolean)
  })

  const recentActivities = computed(() => {
    return userActivities.value
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, 20)
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
      
      // Note: loadUserData() removed as it was overwriting the correctly set currentUser
      
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
        joinDate: new Date().toISOString().split('T')[0]
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
    following.value = []
    followers.value = []
    userActivities.value = []
    error.value = null
    
    console.log('User logged out successfully')
  }

  // Check if user is authenticated on app initialization
  const checkAuthStatus = () => {
    // In a real app, this would check if the user's token is still valid
    // For this mock, we'll just return the current authentication state
    return isAuthenticated.value
  }

  const loadUserData = async () => {
    // In a real app, this would load user data from an API
    // For this mock, we'll just set the mock user data
    currentUser.value = mockUser as any
    isAuthenticated.value = true
    return true
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

  const addUserReview = (review: Omit<Review, 'id' | 'createdAt' | 'userId'>) => {
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

  // Following system actions
  const followUser = async (userId: string) => {
    if (!currentUser.value || userId === currentUser.value.id) return { success: false, error: 'Cannot follow yourself' }
    
    if (following.value.includes(userId)) {
      return { success: false, error: 'Already following this user' }
    }

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // Add to following list
      following.value.push(userId)
      
      // Add activity
      addActivity({
        type: 'follow',
        targetId: userId,
        targetType: 'user',
        content: `Started following user`
      })
      
      // In a real app, this would also update the target user's followers list
      // For mock purposes, we'll simulate this
      const targetUser = mockUsers.find(u => u.id === userId)
      if (targetUser) {
        // This would be handled by the backend in a real app
        console.log(`User ${currentUser.value.name} followed ${targetUser.name}`)
      }
      
      return { success: true }
    } catch (error) {
      return { success: false, error: 'Failed to follow user' }
    }
  }

  const unfollowUser = async (userId: string) => {
    if (!currentUser.value) return { success: false, error: 'Not authenticated' }
    
    const index = following.value.indexOf(userId)
    if (index === -1) {
      return { success: false, error: 'Not following this user' }
    }

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 300))
      
      // Remove from following list
      following.value.splice(index, 1)
      
      // Add activity
      addActivity({
        type: 'follow',
        targetId: userId,
        targetType: 'user',
        content: `Unfollowed user`
      })
      
      return { success: true }
    } catch (error) {
      return { success: false, error: 'Failed to unfollow user' }
    }
  }

  const toggleFollow = async (userId: string) => {
    if (isFollowing.value(userId)) {
      return await unfollowUser(userId)
    } else {
      return await followUser(userId)
    }
  }

  // Activity tracking
  const addActivity = (activity: Omit<UserActivity, 'id' | 'userId' | 'timestamp'>) => {
    if (!currentUser.value) return

    const newActivity: UserActivity = {
      ...activity,
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      userId: currentUser.value.id,
      timestamp: new Date().toISOString()
    }

    userActivities.value.unshift(newActivity)
    
    // Keep only last 100 activities to prevent memory issues
    if (userActivities.value.length > 100) {
      userActivities.value = userActivities.value.slice(0, 100)
    }
  }

  const getActivitiesByType = (type: UserActivity['type']) => {
    return userActivities.value.filter(activity => activity.type === type)
  }

  const getActivitiesForUser = (userId: string) => {
    return userActivities.value.filter(activity => activity.userId === userId)
  }

  // Enhanced watchlist and favorites with activity tracking
  const addToWatchlistWithActivity = (movieId: string) => {
    addToWatchlist(movieId)
    addActivity({
      type: 'watchlist_add',
      targetId: movieId,
      targetType: 'movie',
      content: 'Added movie to watchlist'
    })
  }

  const addToFavoritesWithActivity = (movieId: string) => {
    addToFavorites(movieId)
    addActivity({
      type: 'favorite_add',
      targetId: movieId,
      targetType: 'movie',
      content: 'Added movie to favorites'
    })
  }

  const addUserReviewWithActivity = (review: Omit<Review, 'id' | 'createdAt' | 'userId'>) => {
    addUserReview(review)
    addActivity({
      type: 'review',
      targetId: review.movieId,
      targetType: 'movie',
      content: review.reviewText,
      rating: review.lemonPieRating
    })
  }

  // Initialize with mock authentication for demo
  const initializeMockAuth = () => {
    currentUser.value = mockUser
    isAuthenticated.value = true
    loadUserData()
  }

  // Role check methods
  const isAdmin = () => {
    return currentUser.value?.role === 'admin'
  }
  
  const isModerator = () => {
    return currentUser.value?.role === 'moderator'
  }
  
  const isCritic = () => {
    return currentUser.value?.role === 'critic'
  }
  
  const hasRole = (role: 'user' | 'admin' | 'moderator' | 'critic') => {
    return currentUser.value?.role === role
  }
  
  const assignRole = (userId: string, role: 'user' | 'admin' | 'moderator' | 'critic') => {
    // Find user in mock database
    const userIndex = mockUsers.findIndex(user => user.id === userId)
    if (userIndex === -1) return false
    
    // Update role
    mockUsers[userIndex].role = role
    return true
  }
  
  // Return the store
  return {
    // State
    currentUser,
    isAuthenticated,
    isLoading,
    error,
    watchlist,
    favorites,
    userReviews,
    following,
    followers,
    userActivities,
    loginError,
    loginInProgress,
    registrationError,
    registrationInProgress,
    profileUpdateSuccess,
    profileUpdateError,
    
    // Getters
    userStats,
    watchlistMovies,
    favoriteMovies,
    isInWatchlist,
    isInFavorites,
    isFollowing,
    isFollowedBy,
    followingUsers,
    followerUsers,
    recentActivities,
    
    // Actions
    login,
    logout,
    register,
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
    checkAuthStatus,
    loadUserData,
    
    // Following system
    followUser,
    unfollowUser,
    toggleFollow,
    
    // Activity tracking
    addActivity,
    getActivitiesByType,
    getActivitiesForUser,
    addToWatchlistWithActivity,
    addToFavoritesWithActivity,
    addUserReviewWithActivity,
    
    // Role methods
    isAdmin,
    isModerator,
    isCritic,
    hasRole,
    assignRole
  }
})