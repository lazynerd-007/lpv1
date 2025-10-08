import { computed } from 'vue'
import { useUserStore } from '@/stores/userStore'

export interface Permission {
  action: string
  resource: string
  conditions?: Record<string, any>
}

export interface RolePermissions {
  [key: string]: Permission[]
}

// Define role-based permissions
const ROLE_PERMISSIONS: RolePermissions = {
  admin: [
    { action: 'read', resource: 'admin_dashboard' },
    { action: 'write', resource: 'admin_dashboard' },
    { action: 'read', resource: 'user_management' },
    { action: 'write', resource: 'user_management' },
    { action: 'read', resource: 'content_moderation' },
    { action: 'write', resource: 'content_moderation' },
    { action: 'read', resource: 'analytics' },
    { action: 'write', resource: 'system_settings' },
    { action: 'read', resource: 'all_reviews' },
    { action: 'write', resource: 'all_reviews' },
    { action: 'delete', resource: 'all_reviews' },
    { action: 'read', resource: 'user_profiles' },
    { action: 'write', resource: 'user_profiles' },
    { action: 'assign', resource: 'user_roles' },
    { action: 'verify', resource: 'critic_status' }
  ],
  moderator: [
    { action: 'read', resource: 'content_moderation' },
    { action: 'write', resource: 'content_moderation' },
    { action: 'read', resource: 'all_reviews' },
    { action: 'write', resource: 'all_reviews' },
    { action: 'delete', resource: 'inappropriate_content' },
    { action: 'read', resource: 'user_reports' },
    { action: 'write', resource: 'user_reports' }
  ],
  critic: [
    { action: 'read', resource: 'critic_dashboard' },
    { action: 'write', resource: 'verified_reviews' },
    { action: 'read', resource: 'advanced_analytics' },
    { action: 'write', resource: 'critic_insights' }
  ],
  user: [
    { action: 'read', resource: 'public_content' },
    { action: 'write', resource: 'own_reviews' },
    { action: 'write', resource: 'own_profile' },
    { action: 'read', resource: 'own_profile' },
    { action: 'write', resource: 'watchlist' },
    { action: 'write', resource: 'favorites' }
  ]
}

export function useRoleBasedAccess() {
  const userStore = useUserStore()

  // Check if user has a specific role
  const hasRole = (role: 'user' | 'admin' | 'moderator' | 'critic') => {
    return userStore.hasRole(role)
  }

  // Check if user has any of the specified roles
  const hasAnyRole = (roles: ('user' | 'admin' | 'moderator' | 'critic')[]) => {
    return roles.some(role => userStore.hasRole(role))
  }

  // Check if user has permission for a specific action on a resource
  const hasPermission = (action: string, resource: string, conditions?: Record<string, any>) => {
    const user = userStore.currentUser
    if (!user || !user.role) return false

    const rolePermissions = ROLE_PERMISSIONS[user.role] || []
    
    return rolePermissions.some(permission => {
      const actionMatch = permission.action === action || permission.action === '*'
      const resourceMatch = permission.resource === resource || permission.resource === '*'
      
      // Check conditions if provided
      if (conditions && permission.conditions) {
        const conditionsMatch = Object.entries(permission.conditions).every(
          ([key, value]) => conditions[key] === value
        )
        return actionMatch && resourceMatch && conditionsMatch
      }
      
      return actionMatch && resourceMatch
    })
  }

  // Check if user can access admin features
  const canAccessAdmin = computed(() => {
    return hasRole('admin')
  })

  // Check if user can moderate content
  const canModerateContent = computed(() => {
    return hasAnyRole(['admin', 'moderator'])
  })

  // Check if user is a verified critic
  const isVerifiedCritic = computed(() => {
    const user = userStore.currentUser
    return user?.role === 'critic'
  })

  // Check if user can manage users
  const canManageUsers = computed(() => {
    return hasPermission('write', 'user_management')
  })

  // Check if user can view analytics
  const canViewAnalytics = computed(() => {
    return hasPermission('read', 'analytics')
  })

  // Check if user can assign roles
  const canAssignRoles = computed(() => {
    return hasPermission('assign', 'user_roles')
  })

  // Check if user can verify critics
  const canVerifyCritics = computed(() => {
    return hasPermission('verify', 'critic_status')
  })

  // Check if user can edit a specific review
  const canEditReview = (reviewUserId: string) => {
    const user = userStore.currentUser
    if (!user) return false
    
    // Users can edit their own reviews
    if (user.id === reviewUserId) return true
    
    // Admins and moderators can edit any review
    return hasAnyRole(['admin', 'moderator'])
  }

  // Check if user can delete a specific review
  const canDeleteReview = (reviewUserId: string) => {
    const user = userStore.currentUser
    if (!user) return false
    
    // Users can delete their own reviews
    if (user.id === reviewUserId) return true
    
    // Admins and moderators can delete any review
    return hasAnyRole(['admin', 'moderator'])
  }

  // Get user's role display name
  const getRoleDisplayName = (role?: string) => {
    const roleNames = {
      admin: 'Administrator',
      moderator: 'Moderator',
      critic: 'Verified Critic',
      user: 'User'
    }
    return roleNames[role as keyof typeof roleNames] || 'User'
  }

  // Get available actions for current user
  const getAvailableActions = () => {
    const user = userStore.currentUser
    if (!user || !user.role) return []
    
    return ROLE_PERMISSIONS[user.role] || []
  }

  return {
    // Role checks
    hasRole,
    hasAnyRole,
    hasPermission,
    
    // Computed permissions
    canAccessAdmin,
    canModerateContent,
    isVerifiedCritic,
    canManageUsers,
    canViewAnalytics,
    canAssignRoles,
    canVerifyCritics,
    
    // Dynamic permission checks
    canEditReview,
    canDeleteReview,
    
    // Utility functions
    getRoleDisplayName,
    getAvailableActions
  }
}

// Type definitions for route meta
declare module 'vue-router' {
  interface RouteMeta {
    requiresAuth?: boolean
    requiresAdmin?: boolean
    requiresModerator?: boolean
    requiresCritic?: boolean
    permissions?: Permission[]
  }
}