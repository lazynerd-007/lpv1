import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

// Lazy-loaded components for code splitting
const HomePage = () => import('@/pages/HomePage.vue')
const MovieDetailsPage = () => import('@/pages/MovieDetailsPage.vue')
const SeriesDetailsPage = () => import('@/pages/SeriesDetailsPage.vue')
const SearchPage = () => import('@/pages/SearchPage.vue')
const BrowseMoviesPage = () => import('@/pages/BrowseMoviesPage.vue')
const BrowseSeriesPage = () => import('@/pages/BrowseSeriesPage.vue')
const PeoplePage = () => import('@/pages/PeoplePage.vue')
const WriteReviewPage = () => import('@/pages/WriteReviewPage.vue')
const EditReviewPage = () => import('@/pages/EditReviewPage.vue')
const UserProfilePage = () => import('@/pages/UserProfilePage.vue')
const LoginPage = () => import('@/pages/LoginPage.vue')
const RegisterPage = () => import('@/pages/RegisterPage.vue')
const ForgotPasswordPage = () => import('@/pages/ForgotPasswordPage.vue')
const AboutPage = () => import('@/pages/AboutPage.vue')
const PersonDetailsPage = () => import('@/pages/PersonDetailsPage.vue')
const PrivacyPolicyPage = () => import('@/pages/PrivacyPolicyPage.vue')
const TermsOfServicePage = () => import('@/pages/TermsOfServicePage.vue')
const ContactUsPage = () => import('@/pages/ContactUsPage.vue')
const MovieCastAndCrewPage = () => import('@/pages/MovieCastAndCrewPage.vue')
const SeriesCastAndCrewPage = () => import('@/pages/SeriesCastAndCrewPage.vue')
// Admin components
const AdminPage = () => import('@/pages/AdminPage.vue')
const AdminDashboard = () => import('@/pages/admin/AdminDashboard.vue')
const AdminUsers = () => import('@/pages/admin/AdminUsers.vue')
const AdminModeration = () => import('@/pages/admin/AdminModeration.vue')
const AdminContent = () => import('@/pages/admin/AdminContent.vue')
const AdminAnalytics = () => import('@/pages/admin/AdminAnalytics.vue')
const AdminSettings = () => import('@/pages/admin/AdminSettings.vue')
const AdminCritics = () => import('@/pages/admin/AdminCritics.vue')
const AdminReports = () => import('@/pages/admin/AdminReports.vue')

// User components
const SettingsPage = () => import('@/pages/SettingsPage.vue')
const UserSettings = () => import('@/pages/UserSettings.vue')
const WatchlistPage = () => import('@/pages/WatchlistPage.vue')
const UserDashboard = () => import('@/pages/UserDashboard.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage,
      meta: {
        title: 'LemonNPie - Nollywood Movie Reviews'
      }
    },
    {
      path: '/movie/:id',
      name: 'movie-details',
      component: MovieDetailsPage,
      props: true,
      meta: {
        title: 'Movie Details - LemonNPie'
      }
    },
    {
      path: '/search',
      name: 'search',
      component: SearchPage,
      meta: {
        title: 'Search Movies - LemonNPie'
      }
    },
    {
      path: '/movies',
      name: 'movies',
      component: BrowseMoviesPage,
      meta: {
        title: 'Browse Movies - LemonNPie'
      }
    },
    {
      path: '/series',
      name: 'series',
      component: BrowseSeriesPage,
      meta: {
        title: 'Browse Series - LemonNPie'
      }
    },
    {
      path: '/people',
      name: 'people',
      component: PeoplePage,
      meta: {
        title: 'Trending Actors - LemonNPie'
      }
    },
    {
      path: '/person/:id',
      name: 'person-details',
      component: PersonDetailsPage,
      props: true,
      meta: {
        title: 'Person Details - LemonNPie'
      }
    },
    {
      path: '/movie/:id/cast-crew',
      name: 'movie-cast-crew',
      component: MovieCastAndCrewPage,
      props: true,
      meta: {
        title: 'Cast & Crew - LemonNPie'
      }
    },
    {
      path: '/series/:id/cast-crew',
      name: 'series-cast-crew',
      component: SeriesCastAndCrewPage,
      props: true,
      meta: {
        title: 'Series Cast & Crew - LemonNPie'
      }
     },
     {
      path: '/browse',
      redirect: '/movies'
    },
    {
      path: '/write-review/:movieId?',
      name: 'write-review',
      component: WriteReviewPage,
      props: true,
      meta: {
        title: 'Write Review - LemonNPie',
        requiresAuth: true
      }
    },
    {
      path: '/edit-review/:reviewId',
      name: 'edit-review',
      component: EditReviewPage,
      props: true,
      meta: {
        title: 'Edit Review - LemonNPie',
        requiresAuth: true
      }
    },
    {
      path: '/profile/:userId?',
      name: 'profile',
      component: UserProfilePage,
      props: true,
      meta: {
        title: 'User Profile - LemonNPie'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginPage,
      meta: {
        title: 'Login - LemonNPie',
        hideForAuth: true
      }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterPage,
      meta: {
        title: 'Register - LemonNPie',
        hideForAuth: true
      }
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: ForgotPasswordPage,
      meta: {
        title: 'Forgot Password - LemonNPie',
        hideForAuth: true
      }
    },
    {
      path: '/about',
      name: 'about',
      component: AboutPage,
      meta: {
        title: 'About - LemonNPie'
      }
    },
    {
      path: '/privacy-policy',
      name: 'privacy-policy',
      component: PrivacyPolicyPage,
      meta: {
        title: 'Privacy Policy - LemonNPie'
      }
    },
    {      path: '/terms-of-service',
      name: 'terms-of-service',
      component: TermsOfServicePage,
      meta: {
        title: 'Terms of Service - LemonNPie'
      }
    },
    {
      path: '/contact',
      name: 'contact',
      component: ContactUsPage,
      meta: {
        title: 'Contact Us - LemonNPie'
      }
    },
    {
      path: '/admin',
      name: 'admin',
      component: AdminDashboard,
      meta: {
        title: 'Admin Dashboard - LemonNPie',
        requiresAuth: true,
        requiresAdmin: true
      }
    },
    {
      path: '/admin/users',
      name: 'admin-users',
      component: AdminUsers,
      meta: {
        title: 'User Management - LemonNPie',
        requiresAuth: true,
        requiresAdmin: true
      }
    },

    {
      path: '/admin/moderation',
      name: 'admin-moderation',
      component: AdminModeration,
      meta: {
        title: 'Content Moderation - LemonNPie',
        requiresAuth: true,
        requiresModerator: true
      }
    },

    {
      path: '/admin/content',
      name: 'admin-content',
      component: AdminContent,
      meta: {
        title: 'Content Management - LemonNPie',
        requiresAuth: true,
        requiresAdmin: true
      }
    },

    {
      path: '/admin/analytics',
      name: 'admin-analytics',
      component: AdminAnalytics,
      meta: {
        title: 'Analytics Dashboard - LemonNPie',
        requiresAuth: true,
        requiresAdmin: true
      }
    },

    {
      path: '/admin/settings',
      name: 'admin-settings',
      component: AdminSettings,
      meta: {
        title: 'System Settings - LemonNPie',
        requiresAuth: true,
        requiresAdmin: true
      }
    },

    {
      path: '/admin/critics',
      name: 'admin-critics',
      component: AdminCritics,
      meta: {
        title: 'Critic Management - LemonNPie',
        requiresAuth: true,
        requiresAdmin: true
      }
    },

    {
      path: '/admin/reports',
      name: 'admin-reports',
      component: AdminReports,
      meta: {
        title: 'Reports Management - LemonNPie',
        requiresAuth: true,
        requiresModerator: true
      }
    },

    {
      path: '/settings',
      name: 'settings',
      component: SettingsPage,
      meta: {
        title: 'Settings - LemonNPie',
        requiresAuth: true
      }
    },
    {
      path: '/user-settings',
      name: 'user-settings',
      component: UserSettings,
      meta: {
        title: 'User Settings - LemonNPie',
        requiresAuth: true
      }
    },
    {
      path: '/watchlist',
      name: 'watchlist',
      component: WatchlistPage,
      meta: {
        title: 'My Watchlist - LemonNPie',
        requiresAuth: true
      }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: UserDashboard,
      meta: {
        title: 'Dashboard - LemonNPie',
        requiresAuth: true
      }
    },
    {
      path: '/series/:id',
      name: 'series-details',
      component: SeriesDetailsPage,
      props: true,
      meta: {
        title: 'Series Details - LemonNPie'
      }
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('@/pages/NotFoundPage.vue'),
      meta: {
        title: 'Page Not Found - LemonNPie'
      }
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return {
        top: 0,
        behavior: 'smooth'
      }
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  // Update document title
  if (to.meta.title) {
    document.title = to.meta.title as string;
  }
  
  const userStore = useUserStore();
  const isAuthenticated = userStore.isAuthenticated;
  const user = userStore.currentUser;
  
  // Check authentication requirements
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
    return;
  }
  
  // Check admin requirements
  if (to.meta.requiresAdmin && (!isAuthenticated || !userStore.hasRole('admin'))) {
    next({ name: 'home' });
    return;
  }
  
  // Check critic requirements (for future critic-only routes)
  if (to.meta.requiresCritic && (!isAuthenticated || !userStore.hasRole('critic'))) {
    next({ name: 'home' });
    return;
  }
  
  // Check moderator requirements (for future moderator-only routes)
  if (to.meta.requiresModerator && (!isAuthenticated || !userStore.hasRole('moderator'))) {
    next({ name: 'home' });
    return;
  }
  
  // Redirect authenticated users away from auth pages
  if (to.meta.hideForAuth && isAuthenticated) {
    next({ name: 'home' });
    return;
  }
  
  next();
});

export default router
