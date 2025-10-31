import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useMovieStore } from './movieStore'
import type { Movie } from '@/data/mockMovies'

interface SearchFilters {
  genre: string
  year: string
  rating: string
  language: string
  productionState: string
}

interface SearchState {
  query: string
  results: Movie[]
  isLoading: boolean
  hasSearched: boolean
}

export const useSearchStore = defineStore('search', () => {
  // State
  const searchState = ref<SearchState>({
    query: '',
    results: [],
    isLoading: false,
    hasSearched: false
  })

  const filters = ref<SearchFilters>({
    genre: '',
    year: '',
    rating: '',
    language: '',
    productionState: ''
  })

  const sortBy = ref('title')
  const sortOrder = ref<'asc' | 'desc'>('asc')
  const currentPage = ref(1)
  const itemsPerPage = ref(12)

  // Filter options
  const filterOptions = {
    genres: ['Comedy', 'Drama', 'Action', 'Romance', 'Thriller', 'Crime', 'Horror', 'Adventure'],
    years: ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015'],
    ratings: [
      { label: 'All Ratings', value: '' },
      { label: 'Pies (7-10)', value: 'pie' },
      { label: 'Neutral (4-6)', value: 'neutral' },
      { label: 'Lemons (1-3)', value: 'lemon' }
    ],
    languages: ['English', 'Yoruba', 'Igbo', 'Hausa', 'Pidgin'],
    states: ['Lagos', 'Enugu', 'Kano', 'Abuja', 'Rivers', 'Oyo', 'Delta', 'Anambra']
  }

  // Getters
  const hasActiveFilters = computed(() => {
    return Object.values(filters.value).some(value => value !== '')
  })

  const filteredResults = computed(() => {
    const movieStore = useMovieStore()
    let results = searchState.value.results

    // Apply filters
    if (hasActiveFilters.value) {
      results = movieStore.filterMovies(filters.value)
    }

    // Apply sorting
    if (sortBy.value) {
      results = movieStore.sortMovies(results, sortBy.value, sortOrder.value)
    }

    return results
  })

  const paginatedResults = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    return filteredResults.value.slice(start, end)
  })

  const totalPages = computed(() => {
    return Math.ceil(filteredResults.value.length / itemsPerPage.value)
  })

  const searchSummary = computed(() => {
    const total = filteredResults.value.length
    const showing = paginatedResults.value.length
    const start = (currentPage.value - 1) * itemsPerPage.value + 1
    const end = start + showing - 1

    return {
      total,
      showing,
      start,
      end,
      hasResults: total > 0,
      hasQuery: searchState.value.query.trim() !== ''
    }
  })

  // Actions
  const performSearch = async (query: string) => {
    searchState.value.isLoading = true
    searchState.value.query = query
    currentPage.value = 1

    try {
      const movieStore = useMovieStore()
      searchState.value.results = await movieStore.searchMovies(query)
      searchState.value.hasSearched = true
    } catch (error) {
      console.error('Search failed:', error)
      searchState.value.results = []
    } finally {
      searchState.value.isLoading = false
    }
  }

  const updateFilter = (filterKey: keyof SearchFilters, value: string) => {
    filters.value[filterKey] = value
    currentPage.value = 1 // Reset to first page when filters change
  }

  const clearFilters = () => {
    filters.value = {
      genre: '',
      year: '',
      rating: '',
      language: '',
      productionState: ''
    }
    currentPage.value = 1
  }

  const clearSearch = () => {
    searchState.value = {
      query: '',
      results: [],
      isLoading: false,
      hasSearched: false
    }
    clearFilters()
    currentPage.value = 1
  }

  const updateSort = (newSortBy: string, newSortOrder?: 'asc' | 'desc') => {
    // If same sort field, toggle order
    if (sortBy.value === newSortBy && !newSortOrder) {
      sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
    } else {
      sortBy.value = newSortBy
      sortOrder.value = newSortOrder || 'asc'
    }
    currentPage.value = 1
  }

  const setPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++
    }
  }

  const previousPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--
    }
  }

  const setItemsPerPage = (items: number) => {
    itemsPerPage.value = items
    currentPage.value = 1
  }

  // Quick search presets
  const searchPresets = {
    popularPies: () => {
      clearSearch()
      updateFilter('rating', 'pie')
      updateSort('rating', 'desc')
    },
    recentReleases: () => {
      clearSearch()
      updateFilter('year', '2024')
      updateSort('year', 'desc')
    },
    comedies: () => {
      clearSearch()
      updateFilter('genre', 'Comedy')
      updateSort('rating', 'desc')
    },
    lagosMovies: () => {
      clearSearch()
      updateFilter('productionState', 'Lagos')
      updateSort('year', 'desc')
    }
  }

  const applyPreset = (presetName: keyof typeof searchPresets) => {
    searchPresets[presetName]()
  }

  const loadFromURL = (query: any) => {
    // Load search query from URL
    if (query.q) {
      performSearch(query.q as string)
    }
    
    // Load filters from URL
    if (query.genre) updateFilter('genre', query.genre as string)
    if (query.year) updateFilter('year', query.year as string)
    if (query.rating) updateFilter('rating', query.rating as string)
    if (query.language) updateFilter('language', query.language as string)
    if (query.state) updateFilter('productionState', query.state as string)
    
    // Load pagination from URL
    if (query.page) {
      const page = parseInt(query.page as string)
      if (!isNaN(page)) setPage(page)
    }
  }

  return {
    // State
    searchState,
    filters,
    sortBy,
    sortOrder,
    currentPage,
    itemsPerPage,
    filterOptions,
    
    // Getters
    hasActiveFilters,
    filteredResults,
    paginatedResults,
    totalPages,
    searchSummary,
    
    // Actions
    performSearch,
    updateFilter,
    clearFilters,
    clearSearch,
    updateSort,
    setPage,
    nextPage,
    previousPage,
    setItemsPerPage,
    applyPreset,
    loadFromURL
  }
})