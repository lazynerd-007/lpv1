import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { setActivePinia, createPinia } from 'pinia'
import LoginPage from '@/pages/LoginPage.vue'
import { useUserStore } from '@/stores/userStore'
import type { User } from '@/data/mockMovies'

// Mock router for testing
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'home', component: { template: '<div>Home</div>' } },
    { path: '/login', name: 'login', component: LoginPage },
    { path: '/profile', name: 'profile', component: { template: '<div>Profile</div>' } }
  ]
})

describe('Authentication Integration Tests', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should handle complete login flow', async () => {
    const wrapper = mount(LoginPage, {
      global: {
        plugins: [router]
      }
    })

    const userStore = useUserStore()
    
    // Initially user should not be authenticated
    expect(userStore.isAuthenticated).toBe(false)
    expect(userStore.currentUser).toBeNull()

    // Find login form elements
    const emailInput = wrapper.find('input[type="email"]')
    const passwordInput = wrapper.find('input[type="password"]')
    const loginButton = wrapper.find('button[type="submit"]')

    expect(emailInput.exists()).toBe(true)
    expect(passwordInput.exists()).toBe(true)
    expect(loginButton.exists()).toBe(true)

    // Fill in login credentials
    await emailInput.setValue('test@example.com')
    await passwordInput.setValue('password123')

    // Mock successful login
    const mockUser: User = {
      id: '1',
      name: 'testuser',
      email: 'test@example.com',
      role: 'user',
      avatar: '',
      bio: '',
      joinDate: '2024-01-01'
    }

    // Simulate successful login
    userStore.currentUser = mockUser
    userStore.isAuthenticated = true

    // Verify user is now authenticated
    expect(userStore.isAuthenticated).toBe(true)
    expect(userStore.currentUser).toEqual(mockUser)
    expect(userStore.currentUser?.email).toBe('test@example.com')
  })

  it('should handle logout flow', async () => {
    const userStore = useUserStore()
    
    // Set up authenticated user
    const mockUser: User = {
      id: '1',
      name: 'Test User',
      email: 'test@example.com',
      role: 'user',
      avatar: '',
      bio: '',
      joinDate: '2024-01-01'
    }

    userStore.currentUser = mockUser
    userStore.isAuthenticated = true
    expect(userStore.isAuthenticated).toBe(true)

    // Perform logout
    userStore.logout()

    // Verify user is logged out
    expect(userStore.isAuthenticated).toBe(false)
    expect(userStore.currentUser).toBeNull()
  })

  it('should handle role-based access control', () => {
    const userStore = useUserStore()
    
    // Test admin user
    const adminUser: User = {
      id: '1',
      name: 'admin',
      email: 'admin@example.com',
      role: 'admin',
      avatar: '',
      bio: '',
      joinDate: '2024-01-01'
    }

    userStore.currentUser = adminUser
    userStore.isAuthenticated = true
    
    expect(userStore.hasRole('admin')).toBe(true)
    expect(userStore.isAdmin()).toBe(true)
    expect(userStore.hasRole('user')).toBe(false)
    expect(userStore.hasRole('moderator')).toBe(false)
    expect(userStore.isModerator()).toBe(false)
    expect(userStore.isCritic()).toBe(false)

    // Test regular user
    const regularUser: User = {
      id: '2',
      name: 'user',
      email: 'user@example.com',
      role: 'user',
      avatar: '',
      bio: '',
      joinDate: '2024-01-01'
    }

    userStore.currentUser = regularUser
    userStore.isAuthenticated = true
    
    expect(userStore.hasRole('user')).toBe(true)
    expect(userStore.isAdmin()).toBe(false)
    expect(userStore.hasRole('admin')).toBe(false)
    expect(userStore.hasRole('moderator')).toBe(false)
  })

  it('should handle user data persistence', async () => {
    const userStore = useUserStore()
    
    const mockUser: User = {
      id: '1',
      name: 'testuser',
      email: 'test@example.com',
      role: 'user',
      avatar: '',
      bio: '',
      joinDate: '2024-01-01'
    }

    userStore.currentUser = mockUser
    userStore.isAuthenticated = true

    // Test watchlist operations
    userStore.addToWatchlist('movie1')
    userStore.addToFavorites('movie2')
    userStore.addUserReview({
      movieId: 'movie3',
      userName: 'Test User',
      userAvatar: 'https://example.com/avatar.jpg',
      lemonPieRating: 8,
      reviewText: 'Great movie!',
      reviewLanguage: 'English',
      spoilerWarning: false,
      culturalAuthenticityRating: 9,
      productionQualityRating: 8,
      storyRating: 8,
      actingRating: 9,
      cinematographyRating: 7,
      nollywoodTags: ['comedy', 'romance'],
      helpfulnessScore: 0,
      helpfulVotes: 0,
      unhelpfulVotes: 0,
      userVotes: {},
      isVerifiedCritic: false
    })
    
    expect(userStore.watchlist).toContain('movie1')
    expect(userStore.favorites).toContain('movie2')
    expect(userStore.userReviews.some(r => r.movieId === 'movie3' && r.lemonPieRating === 4)).toBe(true)
    
    userStore.addToWatchlist('movie4')
    expect(userStore.watchlist).toContain('movie4')

    // Test favorites operations
    userStore.addToFavorites('movie5')
    expect(userStore.favorites).toContain('movie5')

    // Test ratings operations
    userStore.addUserReview({
      movieId: 'movie6',
      userName: 'Test User',
      userAvatar: 'https://example.com/avatar.jpg',
      lemonPieRating: 7,
      reviewText: 'Another great movie!',
      reviewLanguage: 'English',
      spoilerWarning: false,
      culturalAuthenticityRating: 8,
      productionQualityRating: 7,
      storyRating: 7,
      actingRating: 8,
      cinematographyRating: 6,
      nollywoodTags: ['drama', 'thriller'],
      helpfulnessScore: 0,
      helpfulVotes: 0,
      unhelpfulVotes: 0,
      userVotes: {},
      isVerifiedCritic: false
    })
    expect(userStore.userReviews.some(r => r.movieId === 'movie6' && r.lemonPieRating === 5)).toBe(true)
  })

  it('should handle user following/unfollowing', async () => {
    const userStore = useUserStore()
    
    const mockUser: User = {
      id: '1',
      name: 'testuser',
      email: 'test@example.com',
      role: 'user',
      avatar: '',
      bio: '',
      joinDate: '2024-01-01'
    }

    userStore.currentUser = mockUser
    userStore.isAuthenticated = true

    // Test following a user
    await userStore.followUser('user2')
    expect(userStore.following).toContain('user2')
    
    // Test unfollowing a user
    await userStore.unfollowUser('user2')
    expect(userStore.following).not.toContain('user2')
    
    // Test following multiple users
    await userStore.followUser('user3')
    await userStore.followUser('user4')
    expect(userStore.following).toContain('user3')
    expect(userStore.following).toContain('user4')
    expect(userStore.following).toHaveLength(2)
  })
})