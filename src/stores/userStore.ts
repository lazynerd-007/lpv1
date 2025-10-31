import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useSeriesStore } from '@/stores/seriesStore'
import { useAuthStore } from '@/stores/authStore'

interface Review {
  id: string
  userId: string
  movieId: string
  userName: string
  userAvatar: string
  lemonPieRating: number
  reviewText: string
  reviewLanguage: string
  spoilerWarning: boolean
  culturalAuthenticityRating: number
  productionQualityRating: number
  storyRating: number
  actingRating: number
  cinematographyRating: number
  nollywoodTags: string[]
  helpfulnessScore: number
  helpfulVotes: number
  unhelpfulVotes: number
  userVotes: { [userId: string]: 'helpful' | 'unhelpful' }
  createdAt: string
  isVerifiedCritic: boolean
}

const API_BASE_URL = 'http://localhost:8000/api/v1'

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
  
  // Initialize authentication from authStore
  const initializeAuth = () => {
    const authStore = useAuthStore()
    authStore.initializeAuth()
    
    if (authStore.user) {
      currentUser.value = authStore.user
      isAuthenticated.value = true
      loadUserData()
    }
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
    // TODO: Implement API call to fetch user details for following list
    return following.value.map(userId => ({
      id: userId,
      name: `User ${userId}`,
      email: `user${userId}@example.com`,
      avatar: undefined,
      bio: undefined
    }))
  })

  const followerUsers = computed(() => {
    // TODO: Implement API call to fetch user details for followers list
    return followers.value.map(userId => ({
      id: userId,
      name: `User ${userId}`,
      email: `user${userId}@example.com`,
      avatar: undefined,
      bio: undefined
    }))
  })

  const recentActivities = computed(() => {
    return userActivities.value
      .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
      .slice(0, 20)
  })

  // Actions
  const login = async (email: string, password: string) => {
    const authStore = useAuthStore()
    await authStore.login(email, password)
    
    // Sync user data from authStore
    if (authStore.user) {
      currentUser.value = authStore.user
      isAuthenticated.value = true
      loadUserData()
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

  const loadUserWatchlist = async () => {
    if (!isAuthenticated.value) return

    try {
      const authStore = useAuthStore()
      const token = authStore.accessToken
      
      if (!token) {
        console.error('No authentication token available')
        return
      }

      const response = await fetch(`${API_BASE_URL}/users/watchlist`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (response.ok) {
        const data = await response.json()
        // Extract movie IDs from the response
        watchlist.value = data.movies?.map((movie: any) => movie.id.toString()) || []
      }
    } catch (error) {
      console.error('Error loading user watchlist:', error)
    }
  }

  const loadUserData = async () => {
    // Load user data from authStore
    const authStore = useAuthStore()
    if (authStore.user) {
      currentUser.value = authStore.user
      isAuthenticated.value = true
      
      // Load user's watchlist from backend
      await loadUserWatchlist()
      
      return true
    }
    return false
  }

  const updateProfile = async (updates: Partial<User>) => {
    if (!currentUser.value) return { success: false, error: 'Not authenticated' }

    isLoading.value = true
    error.value = null

    try {
      // Get auth token
      const authStore = useAuthStore()
      const token = authStore.accessToken
      
      if (!token) {
        throw new Error('No authentication token available')
      }

      // Make API call to update profile
      const response = await fetch(`${API_BASE_URL}/users/profile`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(updates)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      const updatedProfile = await response.json()
      
      // Update local state with the response from the server
      currentUser.value = { ...currentUser.value, ...updatedProfile }
      
      return { success: true }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update profile'
      error.value = errorMessage
      return { success: false, error: errorMessage }
    } finally {
      isLoading.value = false
    }
  }

  const addToWatchlist = async (movieId: string) => {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated to add to watchlist')
    }

    try {
      const authStore = useAuthStore()
      const token = authStore.accessToken
      
      if (!token) {
        throw new Error('No authentication token available')
      }

      const response = await fetch(`${API_BASE_URL}/users/watchlist/${movieId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to add to watchlist')
      }

      // Update local state only after successful API call
      if (!watchlist.value.includes(movieId)) {
        watchlist.value.push(movieId)
      }
    } catch (error) {
      console.error('Error adding to watchlist:', error)
      throw error
    }
  }

  const removeFromWatchlist = async (movieId: string) => {
    if (!isAuthenticated.value) {
      throw new Error('User must be authenticated to remove from watchlist')
    }

    try {
      const authStore = useAuthStore()
      const token = authStore.accessToken
      
      if (!token) {
        throw new Error('No authentication token available')
      }

      const response = await fetch(`${API_BASE_URL}/users/watchlist/${movieId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to remove from watchlist')
      }

      // Update local state only after successful API call
      const index = watchlist.value.indexOf(movieId)
      if (index > -1) {
        watchlist.value.splice(index, 1)
      }
    } catch (error) {
      console.error('Error removing from watchlist:', error)
      throw error
    }
  }

  const toggleWatchlist = async (movieId: string) => {
    if (isInWatchlist.value(movieId)) {
      await removeFromWatchlist(movieId)
    } else {
      await addToWatchlist(movieId)
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
      // This would be handled by the backend in a real app
      console.log(`User ${currentUser.value.name} followed user ${userId}`)
      
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
  const addToWatchlistWithActivity = async (movieId: string) => {
    await addToWatchlist(movieId)
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

  // Initialize authentication
  const initializeAuthState = () => {
    initializeAuth()
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
    // TODO: Implement API call to update user role
    console.log(`Assigning role ${role} to user ${userId}`)
    
    // Update current user role if it's the same user
    if (currentUser.value?.id === userId) {
      currentUser.value.role = role
    }
    
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
    initializeAuthState,
    checkAuthStatus,
    loadUserData,
    loadUserWatchlist,
    
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