import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { mockReviews, getMovieById, type Review } from '@/data/mockMovies'

interface User {
  id: string
  name: string
  email: string
  bio?: string
  location?: string
  joinDate: string
  avatar?: string
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
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20man%20profile%20picture%20professional%20headshot&image_size=square'
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
  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock successful login
      currentUser.value = mockUser
      isAuthenticated.value = true
      
      // Load user data
      await loadUserData()
      
      return { success: true }
    } catch (err) {
      error.value = 'Login failed. Please check your credentials.'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
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
    currentUser.value = null
    isAuthenticated.value = false
    watchlist.value = []
    favorites.value = []
    userReviews.value = []
    error.value = null
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
    initializeMockAuth
  }
})