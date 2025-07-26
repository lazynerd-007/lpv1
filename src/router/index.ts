import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import MovieDetailsPage from '@/pages/MovieDetailsPage.vue'
import SearchPage from '@/pages/SearchPage.vue'
import BrowseMoviesPage from '@/pages/BrowseMoviesPage.vue'
import WriteReviewPage from '@/pages/WriteReviewPage.vue'
import UserProfilePage from '@/pages/UserProfilePage.vue'
import LoginPage from '@/pages/LoginPage.vue'
import RegisterPage from '@/pages/RegisterPage.vue'
import AboutPage from '@/pages/AboutPage.vue'

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
      path: '/about',
      name: 'about',
      component: AboutPage,
      meta: {
        title: 'About - LemonNPie'
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
  const isAuthenticated = false; // TODO: Replace with actual auth check
  
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } });
  } else if (to.meta.hideForAuth && isAuthenticated) {
    next({ name: 'home' });
  } else {
    next();
  }
});

export default router
