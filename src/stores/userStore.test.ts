import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useUserStore } from './userStore'
import type { User, Review } from '@/data/mockMovies'

describe('userStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('initializes with correct default state', () => {
    const store = useUserStore()
    
    expect(store.currentUser).toBeNull()
    expect(store.isAuthenticated).toBe(false)
    expect(store.userActivities).toEqual([])
    expect(store.watchlist).toEqual([])
    expect(store.favorites).toEqual([])
  })

  it('sets current user correctly', () => {
    const store = useUserStore()
    const mockUser = {
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      bio: '',
      location: '',
      joinDate: '2023-01-01',
      role: 'user' as const
    }

    store.currentUser = mockUser
    store.isAuthenticated = true

    expect(store.currentUser).toEqual(mockUser)
    expect(store.isAuthenticated).toBe(true)
  })

  it('should set and logout user correctly', () => {
    const store = useUserStore()
    const mockUser = {
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      bio: 'Test bio',
      location: 'Test location',
      joinDate: '2023-01-01',
      role: 'user' as const
    }

    // Directly set the user state
    store.currentUser = mockUser
    store.isAuthenticated = true
    expect(store.currentUser).toEqual(mockUser)
    expect(store.isAuthenticated).toBe(true)

    store.logout()
    expect(store.currentUser).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('checks user roles correctly', () => {
    const store = useUserStore()
    
    // Test admin role
    const adminUser: User = {
      id: '1',
      name: 'admin',
      email: 'admin@example.com',
      role: 'admin',
      avatar: '',
      bio: '',
      joinDate: '2024-01-01'
    }
    
    store.currentUser = adminUser
    store.isAuthenticated = true
    
    expect(store.hasRole('admin')).toBe(true)
    expect(store.hasRole('user')).toBe(false)
    expect(store.isAdmin()).toBe(true)
    expect(store.isModerator()).toBe(false)
    expect(store.isCritic()).toBe(false)
  })

  it('manages watchlist correctly', () => {
    const userStore = useUserStore()
    const movieId = 'movie-1'

    expect(userStore.isInWatchlist(movieId)).toBe(false)

    userStore.addToWatchlist(movieId)
    expect(userStore.isInWatchlist(movieId)).toBe(true)
    expect(userStore.watchlist).toContain(movieId)

    userStore.removeFromWatchlist(movieId)
    expect(userStore.isInWatchlist(movieId)).toBe(false)
    expect(userStore.watchlist).not.toContain(movieId)
  })

  it('removes movie from watchlist correctly', () => {
    const store = useUserStore()
    
    // Add movie to watchlist first
    store.addToWatchlist('movie1')
    expect(store.watchlist).toContain('movie1')
    
    // Remove movie from watchlist
    store.removeFromWatchlist('movie1')
    expect(store.watchlist).not.toContain('movie1')
  })

  it('manages favorites correctly', () => {
    const userStore = useUserStore()
    const movieId = 'movie-2'

    expect(userStore.isInFavorites(movieId)).toBe(false)

    userStore.addToFavorites(movieId)
    expect(userStore.isInFavorites(movieId)).toBe(true)
    expect(userStore.favorites).toContain(movieId)

    userStore.removeFromFavorites(movieId)
    expect(userStore.isInFavorites(movieId)).toBe(false)
    expect(userStore.favorites).not.toContain(movieId)
  })

  it('manages user following correctly', async () => {
    const userStore = useUserStore()
    const userId = 'user-2'

    // Set up authenticated user
    userStore.currentUser = {
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      bio: '',
      location: '',
      joinDate: '2023-01-01',
      role: 'user'
    }
    userStore.isAuthenticated = true

    expect(userStore.isFollowing(userId)).toBe(false)

    await userStore.followUser(userId)
    expect(userStore.isFollowing(userId)).toBe(true)
    expect(userStore.following).toContain(userId)

    await userStore.unfollowUser(userId)
    expect(userStore.isFollowing(userId)).toBe(false)
    expect(userStore.following).not.toContain(userId)
  })

  it('adds user review correctly', () => {
    const store = useUserStore()
    const mockUser = {
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      bio: '',
      location: '',
      joinDate: '2023-01-01',
      role: 'user' as const
    }
    
    store.currentUser = mockUser
    store.isAuthenticated = true
    
    const reviewData = {
      movieId: 'movie1',
      userName: 'Test User',
      userAvatar: 'https://example.com/avatar.jpg',
      reviewText: 'Great movie!',
      lemonPieRating: 8,
      reviewLanguage: 'English',
      spoilerWarning: false,
      culturalAuthenticityRating: 8,
      productionQualityRating: 8,
      storyRating: 8,
      actingRating: 8,
      cinematographyRating: 8,
      nollywoodTags: ['drama'],
      helpfulnessScore: 0,
      helpfulVotes: 0,
      unhelpfulVotes: 0,
      userVotes: {},
      isVerifiedCritic: false
    }
    
    store.addUserReview(reviewData)
    expect(store.userReviews.length).toBe(1)
    expect(store.userReviews[0].movieId).toBe('movie1')
    expect(store.userReviews[0].reviewText).toBe('Great movie!')
    expect(store.userReviews[0].lemonPieRating).toBe(8)
  })
})