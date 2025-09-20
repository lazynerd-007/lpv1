import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import HomePage from '@/pages/HomePage.vue'
import MovieDetailsPage from '@/pages/MovieDetailsPage.vue'
import SeriesDetailsPage from '@/pages/SeriesDetailsPage.vue'
import SearchPage from '@/pages/SearchPage.vue'
import BrowseMoviesPage from '@/pages/BrowseMoviesPage.vue'
import BrowseSeriesPage from '@/pages/BrowseSeriesPage.vue'
import PeoplePage from '@/pages/PeoplePage.vue'
import WriteReviewPage from '@/pages/WriteReviewPage.vue'
import UserProfilePage from '@/pages/UserProfilePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import ForgotPasswordPage from '@/pages/ForgotPasswordPage.vue'
import AboutPage from '@/pages/AboutPage.vue'
import PersonDetailsPage from '@/pages/PersonDetailsPage.vue'
import PrivacyPolicyPage from '@/pages/PrivacyPolicyPage.vue'
import TermsOfServicePage from '@/pages/TermsOfServicePage.vue'
import ContactUsPage from '@/pages/ContactUsPage.vue'
import MovieCastAndCrewPage from '@/pages/MovieCastAndCrewPage.vue'
import SeriesCastAndCrewPage from '@/pages/SeriesCastAndCrewPage.vue'
import WatchlistPage from '@/pages/WatchlistPage.vue'

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
      path: '/profile/:userId?',
      name: 'profile',
      component: UserProfilePage,
      props: true,
      meta: {
        title: 'User Profile - LemonNPie'
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
      return savedPosition;
    } else if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      };
    } else {
      return { top: 0 };
    }
  }
})

// Navigation guards
router.beforeEach((to, from, next) => {
  // Update document title
  if (to.meta.title) {
    document.title = to.meta.title as string;
  }
  
  // Check authentication requirements
  const userStore = useUserStore();
  const isAuthenticated = userStore.isAuthenticated;
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if (to.meta.hideForAuth && isAuthenticated) {
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router
