import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  mockMovies, 
  mockReviews, 
  getMovieById, 
  getReviewsForMovie,
  getFeaturedMovie,
  getPieMovies,
  getLemonMovies,
  getTrendingMovies,
  getTrendingTVShows,
  type Movie,
  type Review
} from '@/data/mockMovies'

export const useMovieStore = defineStore('movie', () => {
  // State
  const movies = ref<Movie[]>(mockMovies)
  const reviews = ref<Review[]>(mockReviews)
  const currentMovie = ref<Movie | null>(null)
  const currentMovieReviews = ref<Review[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const featuredMovie = computed(() => getFeaturedMovie())
  const pieMovies = computed(() => getPieMovies())
  const lemonMovies = computed(() => getLemonMovies())
  const trendingMovies = computed(() => getTrendingMovies())
  const trendingTVShows = computed(() => getTrendingTVShows())
  
  const topRatedMovies = computed(() => {
    return [...movies.value]
      .sort((a, b) => b.lemonPieRating - a.lemonPieRating)
      .slice(0, 8)
  })
  
  const recentlyAddedMovies = computed(() => {
    return [...movies.value]
      .sort((a, b) => new Date(b.releaseDate).getTime() - new Date(a.releaseDate).getTime())
      .slice(0, 8)
  })
  
  const moviesByGenre = computed(() => {
    const genres: Record<string, Movie[]> = {}
    movies.value.forEach(movie => {
      movie.genre.forEach(g => {
        if (!genres[g]) genres[g] = []
        genres[g].push(movie)
      })
    })
    return genres
  })

  const moviesByYear = computed(() => {
    const years: Record<string, Movie[]> = {}
    movies.value.forEach(movie => {
      const year = movie.releaseDate.split('-')[0]
      if (!years[year]) years[year] = []
      years[year].push(movie)
    })
    return years
  })

  // Actions
  const fetchMovie = async (id: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      const movie = getMovieById(id)
      if (movie) {
        currentMovie.value = movie
        currentMovieReviews.value = getReviewsForMovie(id)
      } else {
        error.value = 'Movie not found'
      }
    } catch (err) {
      error.value = 'Failed to fetch movie'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }

  const searchMovies = (query: string): Movie[] => {
    if (!query.trim()) return []
    
    const searchTerm = query.toLowerCase()
    return movies.value.filter(movie => 
      movie.title.toLowerCase().includes(searchTerm) ||
      movie.localTitle?.toLowerCase().includes(searchTerm) ||
      movie.director.toLowerCase().includes(searchTerm) ||
      movie.cast.some(actor => actor.toLowerCase().includes(searchTerm)) ||
      movie.genre.some(genre => genre.toLowerCase().includes(searchTerm))
    )
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

  const addReview = (review: Omit<Review, 'id' | 'date'>) => {
    const newReview: Review = {
      ...review,
      id: Date.now().toString(),
      createdAt: new Date().toISOString().split('T')[0]
    }
    
    reviews.value.push(newReview)
    
    // Update current movie reviews if viewing the same movie
    if (currentMovie.value?.id === review.movieId) {
      currentMovieReviews.value = getReviewsForMovie(review.movieId)
    }
  }

  const updateReview = (reviewId: string, updates: Partial<Review>) => {
    const index = reviews.value.findIndex(r => r.id === reviewId)
    if (index !== -1) {
      reviews.value[index] = { ...reviews.value[index], ...updates }
      
      // Update current movie reviews if needed
      if (currentMovie.value) {
        currentMovieReviews.value = getReviewsForMovie(currentMovie.value.id)
      }
    }
  }

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

  const clearCurrentMovie = () => {
    currentMovie.value = null
    currentMovieReviews.value = []
    error.value = null
  }

  return {
    // State
    movies,
    reviews,
    currentMovie,
    currentMovieReviews,
    isLoading,
    error,
    
    // Getters
    featuredMovie,
    pieMovies,
    lemonMovies,
    trendingMovies,
    trendingTVShows,
    topRatedMovies,
    recentlyAddedMovies,
    moviesByGenre,
    moviesByYear,
    
    // Actions
    fetchMovie,
    searchMovies,
    filterMovies,
    sortMovies,
    addReview,
    updateReview,
    deleteReview,
    clearCurrentMovie
  }
})