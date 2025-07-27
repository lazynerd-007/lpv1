import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { 
  mockTVShows, 
  getTrendingTVShows,
  type TVShow,
  type Review
} from '@/data/mockMovies'

export const useSeriesStore = defineStore('series', () => {
  // State
  const series = ref<TVShow[]>(mockTVShows)
  const currentSeries = ref<TVShow | null>(null)
  const currentSeriesReviews = ref<Review[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const trendingSeries = computed(() => getTrendingTVShows())
  const pieSeries = computed(() => series.value.filter(show => show.lemonPieRating >= 7))
  const lemonSeries = computed(() => series.value.filter(show => show.lemonPieRating <= 4))
  const ongoingSeries = computed(() => series.value.filter(show => show.status === 'ongoing'))
  const completedSeries = computed(() => series.value.filter(show => show.status === 'completed'))

  // Actions
  const fetchSeries = async (id: string) => {
    isLoading.value = true
    error.value = null
    
    try {
      const show = getSeriesById(id)
      if (show) {
        currentSeries.value = show
        // currentSeriesReviews.value = getReviewsForSeries(id)
      } else {
        error.value = 'Series not found'
      }
    } catch (err) {
      error.value = 'Failed to fetch series'
      console.error('Error fetching series:', err)
    } finally {
      isLoading.value = false
    }
  }

  const searchSeries = (query: string) => {
    if (!query.trim()) return series.value
    
    const searchTerm = query.toLowerCase()
    return series.value.filter(show => 
      show.title.toLowerCase().includes(searchTerm) ||
      show.plotSummary.toLowerCase().includes(searchTerm) ||
      show.genre.some(g => g.toLowerCase().includes(searchTerm)) ||
      show.cast.some(actor => actor.toLowerCase().includes(searchTerm))
    )
  }

  const filterSeries = (filters: {
    genre?: string
    year?: string
    rating?: string
    language?: string
    productionState?: string
    status?: string
  }) => {
    let filtered = [...series.value]

    if (filters.genre && filters.genre !== '') {
      filtered = filtered.filter(show => 
        show.genre.some(g => g.toLowerCase().includes(filters.genre!.toLowerCase()))
      )
    }

    if (filters.year && filters.year !== '') {
      const year = parseInt(filters.year)
      filtered = filtered.filter(show => {
        const showYear = new Date(show.releaseDate).getFullYear()
        return showYear === year
      })
    }

    if (filters.rating && filters.rating !== '') {
      if (filters.rating === 'pie') {
        filtered = filtered.filter(show => show.lemonPieRating >= 7)
      } else if (filters.rating === 'lemon') {
        filtered = filtered.filter(show => show.lemonPieRating <= 4)
      }
    }

    if (filters.language && filters.language !== '') {
      filtered = filtered.filter(show => 
        show.language.some(lang => lang.toLowerCase().includes(filters.language!.toLowerCase()))
      )
    }

    if (filters.productionState && filters.productionState !== '') {
      filtered = filtered.filter(show => 
        show.productionState.toLowerCase().includes(filters.productionState!.toLowerCase())
      )
    }

    if (filters.status && filters.status !== '') {
      filtered = filtered.filter(show => show.status === filters.status)
    }

    return filtered
  }

  const sortSeries = (series: TVShow[], sortBy: string, order: 'asc' | 'desc' = 'asc') => {
    const sorted = [...series].sort((a, b) => {
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
        case 'popularity':
          comparison = a.reviewCount - b.reviewCount
          break
        case 'seasons':
          comparison = a.seasons - b.seasons
          break
        case 'episodes':
          comparison = a.episodes - b.episodes
          break
        default:
          comparison = 0
      }
      
      return order === 'desc' ? -comparison : comparison
    })
    
    return sorted
  }

  const getSeriesById = (id: string) => {
    return series.value.find(show => show.id === id)
  }

  const clearCurrentSeries = () => {
    currentSeries.value = null
    currentSeriesReviews.value = []
    error.value = null
  }

  return {
    // State
    series,
    currentSeries,
    currentSeriesReviews,
    isLoading,
    error,
    
    // Getters
    trendingSeries,
    pieSeries,
    lemonSeries,
    ongoingSeries,
    completedSeries,
    
    // Actions
    fetchSeries,
    searchSeries,
    filterSeries,
    sortSeries,
    getSeriesById,
    clearCurrentSeries
  }
})