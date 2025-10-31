/**
 * API service for communicating with the LemonNPie backend
 */

const API_BASE_URL = 'http://localhost:8000/api/v1'

export interface ApiResponse<T> {
  data?: T
  error?: string
  message?: string
}

export interface PaginatedResponse<T> {
  movies: T[]
  total: number
  page: number
  limit: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

export interface Movie {
  id: string
  title: string
  local_title?: string
  release_date: string
  director: string
  poster_url?: string
  type: 'movie' | 'series'
  genres: string[]
  stats?: {
    average_rating: number
    total_reviews: number
    total_votes: number
  }
  created_at: string
}

export interface MovieDetails extends Movie {
  description?: string
  duration?: number
  language?: string
  country?: string
  budget?: number
  box_office?: number
  trailer_url?: string
  backdrop_url?: string
  cast?: Array<{
    actor_name: string
    character_name: string
    role_type: string
  }>
  reviews?: Array<{
    id: string
    user_id: string
    rating: number
    content: string
    created_at: string
  }>
}

class ApiService {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${API_BASE_URL}${endpoint}`
      
      // Get auth token from localStorage
      const token = localStorage.getItem('access-token')
      const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...options.headers as Record<string, string>,
      }
      
      // Add authorization header if token exists
      if (token) {
        headers['Authorization'] = `Bearer ${token}`
      }
      
      const response = await fetch(url, {
        headers,
        ...options,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return { data }
    } catch (error) {
      console.error('API request failed:', error)
      return { 
        error: error instanceof Error ? error.message : 'Unknown error occurred' 
      }
    }
  }

  // Movie endpoints
  async getMovies(params: {
    page?: number
    per_page?: number
    genre?: string
    year?: number
    director?: string
  } = {}): Promise<ApiResponse<PaginatedResponse<Movie>>> {
    const searchParams = new URLSearchParams()
    
    if (params.page) searchParams.append('page', params.page.toString())
    if (params.per_page) searchParams.append('per_page', params.per_page.toString())
    if (params.genre) searchParams.append('genre', params.genre)
    if (params.year) searchParams.append('year', params.year.toString())
    if (params.director) searchParams.append('director', params.director)

    const queryString = searchParams.toString()
    const endpoint = `/movies/${queryString ? `?${queryString}` : ''}`
    
    return this.request<PaginatedResponse<Movie>>(endpoint)
  }

  async getMovie(id: string): Promise<ApiResponse<MovieDetails>> {
    return this.request<MovieDetails>(`/movies/${id}`)
  }

  async getTrendingMovies(limit: number = 10): Promise<ApiResponse<Movie[]>> {
    return this.request<Movie[]>(`/movies/trending?limit=${limit}`)
  }

  async getFeaturedMovies(limit: number = 10): Promise<ApiResponse<Movie[]>> {
    return this.request<Movie[]>(`/movies/featured?limit=${limit}`)
  }

  async searchMovies(params: {
    query?: string
    genre?: string
    year?: number
    director?: string
    page?: number
    per_page?: number
  }): Promise<ApiResponse<PaginatedResponse<Movie>>> {
    const searchParams = new URLSearchParams()
    
    if (params.query) searchParams.append('q', params.query)
    if (params.genre) searchParams.append('genre', params.genre)
    if (params.year) searchParams.append('year', params.year.toString())
    if (params.director) searchParams.append('director', params.director)
    if (params.page) searchParams.append('page', params.page.toString())
    if (params.per_page) searchParams.append('per_page', params.per_page.toString())

    const queryString = searchParams.toString()
    const endpoint = `/movies/search${queryString ? `?${queryString}` : ''}`
    
    return this.request<PaginatedResponse<Movie>>(endpoint)
  }

  // Auth endpoints
  async login(email: string, password: string): Promise<ApiResponse<{ access_token: string; user: any }>> {
    return this.request('/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
  }

  async register(userData: {
    email: string
    password: string
    username: string
    full_name: string
  }): Promise<ApiResponse<{ access_token: string; user: any }>> {
    return this.request('/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    })
  }

  async logout(): Promise<ApiResponse<{ message: string }>> {
    return this.request('/logout', {
      method: 'POST',
    })
  }

  async getCurrentUser(): Promise<ApiResponse<any>> {
    return this.request('/me')
  }
}

export const apiService = new ApiService()
export default apiService