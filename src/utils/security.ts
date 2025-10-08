// Security utilities for authentication and data validation

/**
 * Validate email format
 */
export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email) && email.length <= 254
}

/**
 * Validate password strength
 */
export function validatePassword(password: string): {
  isValid: boolean
  errors: string[]
} {
  const errors: string[] = []
  
  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long')
  }
  
  if (password.length > 128) {
    errors.push('Password must be less than 128 characters')
  }
  
  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter')
  }
  
  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter')
  }
  
  if (!/\d/.test(password)) {
    errors.push('Password must contain at least one number')
  }
  
  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    errors.push('Password must contain at least one special character')
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

/**
 * Sanitize user input to prevent XSS
 */
export function sanitizeInput(input: string): string {
  if (typeof input !== 'string') {
    return ''
  }
  
  return input
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;')
    .replace(/\//g, '&#x2F;')
    .trim()
}

/**
 * Validate movie review content
 */
export function validateReviewContent(content: string): {
  isValid: boolean
  errors: string[]
} {
  const errors: string[] = []
  const sanitized = sanitizeInput(content)
  
  if (!sanitized || sanitized.length < 10) {
    errors.push('Review must be at least 10 characters long')
  }
  
  if (sanitized.length > 2000) {
    errors.push('Review must be less than 2000 characters')
  }
  
  // Check for potential spam patterns
  const spamPatterns = [
    /http[s]?:\/\//gi, // URLs
    /www\./gi, // Web addresses
    /(.)\1{10,}/gi, // Repeated characters
    /[A-Z]{20,}/gi // Excessive caps
  ]
  
  for (const pattern of spamPatterns) {
    if (pattern.test(content)) {
      errors.push('Review content appears to contain spam or inappropriate content')
      break
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

/**
 * Validate rating value
 */
export function validateRating(rating: number): boolean {
  return Number.isInteger(rating) && rating >= 1 && rating <= 10
}

/**
 * Validate user profile data
 */
export function validateUserProfile(profile: {
  username?: string
  bio?: string
  favoriteGenres?: string[]
}): {
  isValid: boolean
  errors: string[]
} {
  const errors: string[] = []
  
  if (profile.username) {
    const sanitizedUsername = sanitizeInput(profile.username)
    if (sanitizedUsername.length < 3) {
      errors.push('Username must be at least 3 characters long')
    }
    if (sanitizedUsername.length > 30) {
      errors.push('Username must be less than 30 characters')
    }
    if (!/^[a-zA-Z0-9_-]+$/.test(sanitizedUsername)) {
      errors.push('Username can only contain letters, numbers, underscores, and hyphens')
    }
  }
  
  if (profile.bio) {
    const sanitizedBio = sanitizeInput(profile.bio)
    if (sanitizedBio.length > 500) {
      errors.push('Bio must be less than 500 characters')
    }
  }
  
  if (profile.favoriteGenres) {
    if (profile.favoriteGenres.length > 10) {
      errors.push('Cannot select more than 10 favorite genres')
    }
    
    const validGenres = [
      'Action', 'Comedy', 'Drama', 'Romance', 'Thriller', 'Horror',
      'Adventure', 'Crime', 'Fantasy', 'Sci-Fi', 'Documentary', 'Musical'
    ]
    
    for (const genre of profile.favoriteGenres) {
      if (!validGenres.includes(genre)) {
        errors.push(`Invalid genre: ${genre}`)
      }
    }
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

/**
 * Check for potential SQL injection patterns
 */
export function detectSQLInjection(input: string): boolean {
  const sqlPatterns = [
    /('|(\-\-)|(;)|(\||\|)|(\*|\*))/i,
    /(union|select|insert|delete|update|drop|create|alter|exec|execute)/i,
    /(script|javascript|vbscript|onload|onerror|onclick)/i
  ]
  
  return sqlPatterns.some(pattern => pattern.test(input))
}

/**
 * Rate limiting helper
 */
export class RateLimiter {
  private attempts: Map<string, { count: number; resetTime: number }> = new Map()
  
  constructor(
    private maxAttempts: number = 5,
    private windowMs: number = 15 * 60 * 1000 // 15 minutes
  ) {}
  
  isAllowed(identifier: string): boolean {
    const now = Date.now()
    const record = this.attempts.get(identifier)
    
    if (!record || now > record.resetTime) {
      this.attempts.set(identifier, {
        count: 1,
        resetTime: now + this.windowMs
      })
      return true
    }
    
    if (record.count >= this.maxAttempts) {
      return false
    }
    
    record.count++
    return true
  }
  
  getRemainingAttempts(identifier: string): number {
    const record = this.attempts.get(identifier)
    if (!record || Date.now() > record.resetTime) {
      return this.maxAttempts
    }
    return Math.max(0, this.maxAttempts - record.count)
  }
  
  reset(identifier: string): void {
    this.attempts.delete(identifier)
  }
}

/**
 * Content Security Policy helpers
 */
export const CSP_DIRECTIVES = {
  defaultSrc: ["'self'"],
  scriptSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
  styleSrc: ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
  imgSrc: ["'self'", "data:", "https:"],
  fontSrc: ["'self'", "https://fonts.gstatic.com"],
  connectSrc: ["'self'", "https://api.themoviedb.org"],
  mediaSrc: ["'self'"],
  objectSrc: ["'none'"],
  baseUri: ["'self'"],
  formAction: ["'self'"],
  frameAncestors: ["'none'"]
}

export function generateCSPHeader(): string {
  return Object.entries(CSP_DIRECTIVES)
    .map(([directive, sources]) => `${directive.replace(/([A-Z])/g, '-$1').toLowerCase()} ${sources.join(' ')}`)
    .join('; ')
}