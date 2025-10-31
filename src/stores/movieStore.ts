import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService, type Movie as ApiMovie, type MovieDetails } from '@/services/api'
import { 
  mockMovies, 
  getReviewsForMovie,
  type Movie,
  type Review
} from '@/data/mockMovies'

export const useMovieStore = defineStore('movie', () => {
  // State
  const movies = ref<Movie[]>([])
  const apiMovies = ref<ApiMovie[]>([])
  const featuredMovies = ref<ApiMovie[]>([])
  const trendingMoviesApi = ref<ApiMovie[]>([])
  const reviews = ref<Review[]>([])
  const currentMovie = ref<Movie | MovieDetails | null>(null)
  const currentMovieReviews = ref<Review[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const hasLoadedMovies = ref(false)

  // API Actions
  const loadMovies = async () => {
    if (hasLoadedMovies.value) return
    
    try {
      isLoading.value = true
      error.value = null
      
      const response = await apiService.getMovies()
      apiMovies.value = response.data?.movies || []
      
      // Convert API movies to local Movie format for compatibility
      movies.value = (response.data?.items || []).map(apiMovie => ({
        id: apiMovie.id.toString(),
        title: apiMovie.title,
        localTitle: apiMovie.local_title,
        releaseDate: apiMovie.release_date,
        runtime: 120, // Default runtime since not provided by API
        genre: apiMovie.genres || [],
        language: ['English'], // Default language
        director: apiMovie.director || 'Unknown',
        producer: 'Unknown', // Not provided by API
        cast: [], // Not provided in list endpoint
        type: apiMovie.type as 'movie' | 'series',
        plotSummary: 'Plot summary not available', // Not provided in list endpoint
        posterUrl: apiMovie.poster_url || '',
        trailerUrl: '', // Not provided in list endpoint
        productionCompany: 'Unknown', // Not provided by API
        filmingLocations: [], // Not provided by API
        productionState: 'Unknown', // Not provided by API
        boxOfficeNG: '', // Not provided by API
        streamingPlatforms: [], // Not provided by API
        awards: [], // Not provided by API
        lemonPieRating: apiMovie.stats?.average_rating || 0,
        userRating: 0, // Default
        criticRating: 0, // Default
        reviewCount: apiMovie.stats?.review_count || 0
      }))
      
      hasLoadedMovies.value = true
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to load movies'
      console.error('Failed to load movies:', err)
    } finally {
      isLoading.value = false
    }
  }

  const loadFeaturedMovies = async () => {
    try {
      const response = await apiService.getFeaturedMovies()
      featuredMovies.value = response.data?.movies || []
    } catch (err) {
      console.error('Failed to load featured movies:', err)
    }
  }

  const loadTrendingMovies = async () => {
    try {
      const response = await apiService.getTrendingMovies()
      trendingMoviesApi.value = response.data?.movies || []
    } catch (err) {
      console.error('Failed to load trending movies:', err)
    }
  }

  // Getters
  const featuredMovie = computed(() => featuredMovies.value[0] || null)
  const pieMovies = computed(() => movies.value.filter(movie => movie.lemonPieRating >= 7))
  const lemonMovies = computed(() => movies.value.filter(movie => movie.lemonPieRating < 5))
  const topRatedMovies = computed(() => movies.value.filter(movie => movie.lemonPieRating >= 8))
  const trendingMoviesComputed = computed(() => trendingMoviesApi.value.map(apiMovie => ({
    id: apiMovie.id.toString(),
    title: apiMovie.title,
    description: apiMovie.description,
    releaseDate: apiMovie.release_date,
    duration: apiMovie.duration || 120,
    genres: apiMovie.genres || [],
    director: apiMovie.director || 'Unknown',
    cast: apiMovie.cast || [],
    lemonPieRating: apiMovie.rating || 0,
    posterUrl: apiMovie.poster_url || '',
    trailerUrl: apiMovie.trailer_url || '',
    backdropUrl: apiMovie.backdrop_url || '',
    language: apiMovie.language || 'en',
    country: apiMovie.country || 'Unknown',
    budget: apiMovie.budget || 0,
    revenue: apiMovie.revenue || 0,
    status: apiMovie.status || 'Released',
    tagline: apiMovie.tagline || '',
    homepage: apiMovie.homepage || '',
    imdbId: apiMovie.imdb_id || '',
    tmdbId: apiMovie.tmdb_id || 0,
    popularity: apiMovie.popularity || 0,
    voteAverage: apiMovie.vote_average || 0,
    voteCount: apiMovie.vote_count || 0,
    adult: apiMovie.adult || false,
    video: apiMovie.video || false,
    originalTitle: apiMovie.original_title || apiMovie.title,
    originalLanguage: apiMovie.original_language || 'en'
  })))
  const recentlyAddedMovies = computed(() => {
    return movies.value
      .sort((a, b) => new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime())
      .slice(0, 10)
  })
  const moviesByGenre = computed(() => (genre: string) => {
    return movies.value.filter(movie => movie.genres.includes(genre))
  })
  const moviesByYear = computed(() => (year: number) => {
    return movies.value.filter(movie => new Date(movie.releaseDate).getFullYear() === year)
  })

  // Actions
  const fetchMovie = async (id: string) => {
    try {
      isLoading.value = true
      error.value = null
      
      // Try to get from API first
      try {
        const response = await apiService.getMovie(id)
        currentMovie.value = response.data
        currentMovieReviews.value = getReviewsForMovie(id)
        return
      } catch (apiError) {
        console.warn('Failed to fetch from API, falling back to local data:', apiError)
      }
      
      // Fallback to local data
      const movie = movies.value.find(m => m.id === id)
      if (movie) {
        currentMovie.value = movie
        currentMovieReviews.value = getReviewsForMovie(id)
      } else {
        error.value = 'Movie not found'
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to fetch movie'
    } finally {
      isLoading.value = false
    }
  }

  const getMovieById = (id: string): Movie | undefined => {
    return movies.value.find(movie => movie.id === id)
  }

  const searchMovies = async (query: string): Promise<Movie[]> => {
    if (!query.trim()) return []
    
    try {
      // Try API search first
      const response = await apiService.searchMovies({ query })
      // Backend returns array directly, not wrapped in data property
      const movies = response.data || response
      return movies.map(apiMovie => ({
        id: apiMovie.id.toString(),
        title: apiMovie.title,
        localTitle: apiMovie.local_title,
        releaseDate: apiMovie.release_date,
        runtime: 120, // Default runtime since not provided by API
        genre: apiMovie.genres || [],
        language: ['English'], // Default language
        director: apiMovie.director || 'Unknown',
        producer: 'Unknown', // Not provided by API
        cast: [], // Not provided in search endpoint
        type: apiMovie.type as 'movie' | 'series',
        plotSummary: 'Plot summary not available', // Not provided in search endpoint
        posterUrl: apiMovie.poster_url || '',
        trailerUrl: '', // Not provided in search endpoint
        productionCompany: 'Unknown', // Not provided by API
        filmingLocations: [], // Not provided by API
        productionState: 'Unknown', // Not provided by API
        boxOfficeNG: '', // Not provided by API
        streamingPlatforms: [], // Not provided by API
        awards: [], // Not provided by API
        lemonPieRating: apiMovie.stats?.average_rating || 0,
        userRating: 0, // Default
        criticRating: 0, // Default
        reviewCount: apiMovie.stats?.review_count || 0
      }))
    } catch (err) {
      console.warn('API search failed, falling back to local search:', err)
      
      // Fallback to local search
      const searchTerm = query.toLowerCase()
      return movies.value.filter(movie => 
        movie.title.toLowerCase().includes(searchTerm) ||
        movie.localTitle?.toLowerCase().includes(searchTerm) ||
        movie.director.toLowerCase().includes(searchTerm) ||
        movie.cast.some(actor => actor.toLowerCase().includes(searchTerm)) ||
        movie.genre.some(genre => genre.toLowerCase().includes(searchTerm))
      )
    }
  }

  const filterMovies = (filters: {
    genre?: string
    year?: string
    rating?: string
    language?: string
    productionState?: string
  }) => {
    let filtered = [...movies.value]
    
    if (filters.genre) {
      filtered = filtered.filter(movie => 
        movie.genre.some(g => g.toLowerCase().includes(filters.genre!.toLowerCase()))
      )
    }
    
    if (filters.year) {
      filtered = filtered.filter(movie => 
        movie.releaseDate.startsWith(filters.year!)
      )
    }
    
    if (filters.rating) {
      filtered = filtered.filter(movie => {
        const rating = movie.lemonPieRating
        switch (filters.rating) {
          case 'pie': return rating >= 7
          case 'neutral': return rating >= 4 && rating < 7
          case 'lemon': return rating < 4
          default: return true
        }
      })
    }
    
    if (filters.language) {
      filtered = filtered.filter(movie => 
        movie.language.some(l => l.toLowerCase().includes(filters.language!.toLowerCase()))
      )
    }
    
    if (filters.productionState) {
      filtered = filtered.filter(movie => 
        movie.productionState.toLowerCase().includes(filters.productionState!.toLowerCase())
      )
    }
    
    return filtered
  }

  const sortMovies = (movies: Movie[], sortBy: string, order: 'asc' | 'desc' = 'asc') => {
    const sorted = [...movies].sort((a, b) => {
      let comparison = 0
      
      switch (sortBy) {
        case 'title':
          comparison = a.title.localeCompare(b.title)
          break
        case 'year':
          comparison = new Date(a.releaseDate).getTime() - new Date(b.releaseDate).getTime()
          break
        case 'rating':
          comparison = a.lemonPieRating - b.lemonPieRating
          break
        case 'reviews':
          const aReviews = getReviewsForMovie(a.id).length
          const bReviews = getReviewsForMovie(b.id).length
          comparison = aReviews - bReviews
          break
        default:
          return 0
      }
      
      return order === 'desc' ? -comparison : comparison
    })
    
    return sorted
  }

  const addReview = (review: Omit<Review, 'id' | 'createdAt'>) => {
    const newReview: Review = {
      id: `review-${Date.now()}`,
      createdAt: new Date().toISOString(),
      helpfulVotes: 0,
      unhelpfulVotes: 0,
      ...review
    }
    
    reviews.value.push(newReview)
    
    // If this is a review for the current movie, update currentMovieReviews
    if (currentMovie.value && review.movieId === currentMovie.value.id) {
      currentMovieReviews.value.push(newReview)
    }
    
    return newReview
  }
  
  const updateReview = (updatedReview: Review) => {
    // Find the review index in the reviews array
    const reviewIndex = reviews.value.findIndex(r => r.id === updatedReview.id)
    
    if (reviewIndex !== -1) {
      // Update the review in the reviews array
      reviews.value[reviewIndex] = {
        ...reviews.value[reviewIndex],
        ...updatedReview
      }
      
      // If this is a review for the current movie, update currentMovieReviews
      if (currentMovie.value && updatedReview.movieId === currentMovie.value.id) {
        const currentReviewIndex = currentMovieReviews.value.findIndex(r => r.id === updatedReview.id)
        if (currentReviewIndex !== -1) {
          currentMovieReviews.value[currentReviewIndex] = {
            ...currentMovieReviews.value[currentReviewIndex],
            ...updatedReview
          }
        }
      }
      
      return true
    }
    
    return false
  }
  
  const getReviewById = (reviewId: string): Review | undefined => {
    return reviews.value.find(review => review.id === reviewId)
  }

  // This function is already defined above with a different signature

  const deleteReview = (reviewId: string) => {
    const index = reviews.value.findIndex(r => r.id === reviewId)
    if (index !== -1) {
      reviews.value.splice(index, 1)
      
      // Update current movie reviews if needed
      if (currentMovie.value) {
        currentMovieReviews.value = getReviewsForMovie(currentMovie.value.id)
      }
    }
  }

  const voteOnReview = (reviewId: string, userId: string, voteType: 'helpful' | 'unhelpful') => {
    const reviewIndex = reviews.value.findIndex(r => r.id === reviewId)
    if (reviewIndex === -1) return
    
    const review = reviews.value[reviewIndex]
    
    // Prevent users from voting on their own reviews
    if (review.userId === userId) return
    
    // Remove previous vote if exists
    const previousVote = review.userVotes[userId]
    if (previousVote) {
      if (previousVote === 'helpful') {
        review.helpfulVotes--
      } else {
        review.unhelpfulVotes--
      }
    }
    
    // Add new vote
    if (previousVote === voteType) {
      // If clicking the same vote, remove it
      delete review.userVotes[userId]
    } else {
      // Add new vote
      review.userVotes[userId] = voteType
      if (voteType === 'helpful') {
        review.helpfulVotes++
      } else {
        review.unhelpfulVotes++
      }
    }
    
    // Update helpfulness score (helpful votes - unhelpful votes)
    review.helpfulnessScore = review.helpfulVotes - review.unhelpfulVotes
    
    // Update current movie reviews if needed
    if (currentMovie.value) {
      currentMovieReviews.value = getReviewsForMovie(currentMovie.value.id)
    }
  }
  
  const getUserVoteOnReview = (reviewId: string, userId: string): 'helpful' | 'unhelpful' | null => {
    const review = reviews.value.find(r => r.id === reviewId)
    return review?.userVotes[userId] || null
  }

  const clearCurrentMovie = () => {
    currentMovie.value = null
    currentMovieReviews.value = []
    error.value = null
  }

  return {
    // State
    movies,
    apiMovies,
    featuredMovies,
    reviews,
    currentMovie,
    currentMovieReviews,
    isLoading,
    error,
    hasLoadedMovies,
    
    // Getters
    featuredMovie,
    pieMovies,
    lemonMovies,
    topRatedMovies,
    trendingMovies: trendingMoviesComputed,
    recentlyAddedMovies,
    moviesByGenre,
    moviesByYear,
    
    // API Actions
    loadMovies,
    loadFeaturedMovies,
    loadTrendingMovies,
    
    // Actions
    fetchMovie,
    searchMovies,
    filterMovies,
    sortMovies,
    addReview,
    updateReview,
    deleteReview,
    voteOnReview,
    getUserVoteOnReview,
    clearCurrentMovie,
    getMovieById
  }
})