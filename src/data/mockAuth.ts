// Mock Authentication Database for Testing
// This file contains test credentials and authentication scenarios

export interface MockUser {
  id: string
  name: string
  email: string
  password: string // In real app, this would be hashed
  bio?: string
  location?: string
  joinDate: string
  avatar?: string
  isActive: boolean
  lastLogin?: string
  loginAttempts: number
  lockedUntil?: string
  role: 'user' | 'admin' | 'moderator'
}

export interface AuthAttempt {
  email: string
  timestamp: number
  success: boolean
  ip?: string
}

// Mock user database with various test scenarios
export const mockUsers: MockUser[] = [
  {
    id: '1',
    name: 'Adebayo Johnson',
    email: 'admin@admin.com',
    password: 'admin123', // Test admin account
    bio: 'Passionate Nollywood enthusiast and film critic',
    location: 'Lagos, Nigeria',
    joinDate: '2023-01-15',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20man%20profile%20picture%20professional%20headshot&image_size=square',
    isActive: true,
    loginAttempts: 0,
    role: 'admin'
  },
  {
    id: '2',
    name: 'Funmi Adebayo',
    email: 'user@test.com',
    password: 'password123',
    bio: 'Movie lover and weekend binge-watcher',
    location: 'Abuja, Nigeria',
    joinDate: '2023-03-20',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20woman%20profile%20picture%20professional%20headshot&image_size=square',
    isActive: true,
    loginAttempts: 0,
    role: 'user'
  },
  {
    id: '3',
    name: 'Kemi Okafor',
    email: 'moderator@test.com',
    password: 'mod123456',
    bio: 'Community moderator and film enthusiast',
    location: 'Port Harcourt, Nigeria',
    joinDate: '2023-02-10',
    avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20woman%20moderator%20profile%20picture&image_size=square',
    isActive: true,
    loginAttempts: 0,
    role: 'moderator'
  },
  {
    id: '4',
    name: 'Locked User',
    email: 'locked@test.com',
    password: 'locked123',
    bio: 'Account locked due to multiple failed attempts',
    location: 'Kano, Nigeria',
    joinDate: '2023-04-01',
    isActive: false,
    loginAttempts: 5,
    lockedUntil: new Date(Date.now() + 15 * 60 * 1000).toISOString(), // Locked for 15 minutes
    role: 'user'
  },
  {
    id: '5',
    name: 'Inactive User',
    email: 'inactive@test.com',
    password: 'inactive123',
    bio: 'Deactivated account for testing',
    location: 'Ibadan, Nigeria',
    joinDate: '2023-01-01',
    isActive: false,
    loginAttempts: 0,
    role: 'user'
  }
]

// Track login attempts for rate limiting
export const loginAttempts: AuthAttempt[] = []

// Authentication error types
export enum AuthError {
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  ACCOUNT_LOCKED = 'ACCOUNT_LOCKED',
  ACCOUNT_INACTIVE = 'ACCOUNT_INACTIVE',
  TOO_MANY_ATTEMPTS = 'TOO_MANY_ATTEMPTS',
  NETWORK_ERROR = 'NETWORK_ERROR',
  SERVER_ERROR = 'SERVER_ERROR',
  VALIDATION_ERROR = 'VALIDATION_ERROR'
}

// Authentication response interface
export interface AuthResponse {
  success: boolean
  user?: MockUser
  error?: {
    type: AuthError
    message: string
    details?: any
  }
  token?: string
}

// Rate limiting configuration
export const RATE_LIMIT_CONFIG = {
  MAX_ATTEMPTS: 5,
  LOCKOUT_DURATION: 15 * 60 * 1000, // 15 minutes
  ATTEMPT_WINDOW: 5 * 60 * 1000, // 5 minutes
  GLOBAL_RATE_LIMIT: 10 // Max attempts per IP per window
}

// Test scenarios for different authentication cases
export const TEST_SCENARIOS = {
  SUCCESS: {
    email: 'admin@admin.com',
    password: 'admin123',
    description: 'Successful login with admin credentials'
  },
  INVALID_EMAIL: {
    email: 'nonexistent@test.com',
    password: 'password123',
    description: 'Login with non-existent email'
  },
  INVALID_PASSWORD: {
    email: 'user@test.com',
    password: 'wrongpassword',
    description: 'Login with incorrect password'
  },
  LOCKED_ACCOUNT: {
    email: 'locked@test.com',
    password: 'locked123',
    description: 'Login with locked account'
  },
  INACTIVE_ACCOUNT: {
    email: 'inactive@test.com',
    password: 'inactive123',
    description: 'Login with inactive account'
  },
  EMPTY_CREDENTIALS: {
    email: '',
    password: '',
    description: 'Login with empty credentials'
  },
  INVALID_EMAIL_FORMAT: {
    email: 'invalid-email',
    password: 'password123',
    description: 'Login with invalid email format'
  }
}

// Helper functions for authentication testing
export const getTestCredentials = () => {
  return {
    validAdmin: { email: 'admin@admin.com', password: 'admin123' },
    validUser: { email: 'user@test.com', password: 'password123' },
    validModerator: { email: 'moderator@test.com', password: 'mod123456' },
    lockedAccount: { email: 'locked@test.com', password: 'locked123' },
    inactiveAccount: { email: 'inactive@test.com', password: 'inactive123' }
  }
}

export const getRandomTestUser = (): MockUser => {
  const activeUsers = mockUsers.filter(user => user.isActive && !user.lockedUntil)
  return activeUsers[Math.floor(Math.random() * activeUsers.length)]
}