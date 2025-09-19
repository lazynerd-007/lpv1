<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { Search, Menu, X, User, Heart, Star, Film } from 'lucide-vue-next';

const router = useRouter();

// State
const isMenuOpen = ref(false);
const searchQuery = ref('');
const isSearchFocused = ref(false);

// Navigation items
const navItems = [
  { name: 'Movies', path: '/movies' },
  { name: 'Series', path: '/series' },
  { name: 'People', path: '/people' }
];

// User menu items (for when user is logged in)
const userMenuItems = [
  { name: 'My Profile', path: '/profile' },
  { name: 'My Reviews', path: '/my-reviews' },
  { name: 'Watchlist', path: '/watchlist' },
  { name: 'Settings', path: '/settings' }
];

// Mock user state (in real app, this would come from auth store)
const isLoggedIn = ref(false);
const user = ref({
  name: 'Adunni Lagos',
  avatar: 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=Nigerian%20woman%20profile%20picture%20professional%20headshot&image_size=square',
  isVerifiedCritic: false
});

// No longer need isCurrentRoute function since we removed active route styling

// Methods
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value } });
    searchQuery.value = '';
    isSearchFocused.value = false;
  }
};

const navigateTo = (path: string) => {
  router.push(path);
  isMenuOpen.value = false;
};

const handleLogin = () => {
  // In real app, this would open login modal or navigate to login page
  router.push('/login');
};

const handleLogout = () => {
  // In real app, this would clear auth state
  isLoggedIn.value = false;
};
</script>

<template>
  <header class="bg-gray-900 text-white sticky top-0 z-50 shadow-xl">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <router-link 
          to="/" 
          class="flex items-center gap-2 text-xl font-bold hover:text-orange-400 transition-colors"
        >
          <span class="text-yellow-400">🍋</span>
          <span class="text-white">LemonNPie</span>
          <span class="text-orange-400">🥧</span>
        </router-link>
        
        <div class="hidden md:flex flex-1 items-center">
          <!-- Search Bar (Desktop) -->
          <div class="relative">
            <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search for movies, TV shows and people..."
              class="w-[23.04rem] bg-gray-800 text-white placeholder-gray-400 pl-10 pr-4 py-2 rounded-lg border border-gray-700 focus:border-orange-400 focus:outline-none focus:ring-1 focus:ring-orange-400 transition-all"
              @keyup.enter="handleSearch"
            />
          </div>
          
          <!-- Desktop Navigation -->
          <nav class="hidden lg:flex items-center gap-6 ml-4">
            <router-link 
              v-for="item in navItems" 
              :key="item.name"
              :to="item.path"
              class="text-gray-300 hover:text-white transition-colors font-medium"
            >
              {{ item.name }}
            </router-link>
          </nav>
        </div>
        
        <!-- User Actions -->
        <div class="flex items-center gap-4">
          <!-- User Menu -->
          <div v-if="isLoggedIn" class="relative">
            <button class="flex items-center gap-2 hover:text-orange-400 transition-colors">
              <img :src="user.avatar" :alt="user.name" class="w-8 h-8 rounded-full" />
              <span class="hidden sm:block">{{ user.name }}</span>
            </button>
          </div>
          
          <!-- Login/Register Buttons (Desktop only) -->
          <div v-else class="hidden md:flex items-center gap-3">
            <button 
              class="text-gray-300 hover:text-white transition-colors font-medium"
              @click="handleLogin"
            >
              Login
            </button>
            <button 
              class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg font-medium transition-colors"
              @click="navigateTo('/register')"
            >
              Register
            </button>
          </div>
        </div>
        
        <!-- Mobile Menu Button -->
        <div class="lg:hidden ml-4 pl-4 border-l border-gray-700">
          <button 
            class="text-gray-300 hover:text-white transition-colors"
            @click="toggleMenu"
          >
            <Menu v-if="!isMenuOpen" class="w-6 h-6" />
            <X v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>
    
    <!-- Mobile Menu Overlay -->
    <div 
      v-if="isMenuOpen" 
      class="lg:hidden absolute top-full left-0 w-full bg-gray-900 border-t border-gray-700 shadow-xl"
    >
      <div class="p-4">
        <!-- Mobile Search -->
        <div class="mb-6">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Search movies..."
              class="w-full bg-gray-800 text-white placeholder-gray-400 pl-10 pr-4 py-3 rounded-lg border border-gray-700 focus:border-orange-400 focus:outline-none"
              @keyup.enter="handleSearch"
            />
          </div>
        </div>
        
        <!-- Mobile Navigation -->
        <nav class="space-y-2 mb-6">
          <router-link 
            v-for="item in navItems" 
            :key="item.name"
            :to="item.path"
            class="block px-4 py-3 rounded-lg text-gray-300 hover:text-white hover:bg-gray-800 transition-colors"
            @click="isMenuOpen = false"
          >
            {{ item.name }}
          </router-link>
        </nav>
        
        <!-- Mobile User Actions -->
        <div v-if="!isLoggedIn" class="space-y-3">
          <button 
            class="w-full text-left px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
            @click="handleLogin"
          >
            Login
          </button>
          <button 
            class="w-full bg-orange-500 hover:bg-orange-600 text-white px-4 py-3 rounded-lg font-medium transition-colors"
            @click="navigateTo('/register')"
          >
            Register
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
/* Custom styles for the dark header */
</style>