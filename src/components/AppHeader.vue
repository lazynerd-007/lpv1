<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { Search, Menu, X, Bell, ChevronDown, User, Heart, Settings, Sun, Moon, Shield } from 'lucide-vue-next';
import { useUserStore } from '@/stores/userStore';
import { useTheme } from '@/composables/useTheme';
import NotificationDropdown from '@/components/ui/NotificationDropdown.vue';

const router = useRouter();
const userStore = useUserStore();
const { theme, isDark, toggleTheme } = useTheme();

// State
const isMenuOpen = ref(false);
const searchQuery = ref('');
const isSearchFocused = ref(false);
const isUserDropdownOpen = ref(false);

// Navigation items
const navItems = [
  { name: 'Movies', path: '/movies' },
  { name: 'Series', path: '/series' },
  { name: 'People', path: '/people' },
  { name: 'Contact Us', path: '/contact' }
];

// User menu items (for when user is logged in)
const userMenuItems = computed(() => {
  const baseItems = [
    { name: 'Watchlist', path: '/watchlist', icon: Heart },
    { name: 'Profile', path: '/profile', icon: User },
    { name: 'Settings', path: '/settings', icon: Settings }
  ];
  
  // Add admin panel for admin users
  if (userStore.isAdmin()) {
    baseItems.splice(2, 0, { name: 'Admin Panel', path: '/admin', icon: Shield });
  }
  
  return baseItems;
});

// Computed properties for user data
const isLoggedIn = computed(() => userStore.isAuthenticated);
const currentUser = computed(() => userStore.currentUser);
const userLastName = computed(() => {
  if (!currentUser.value?.name) return '';
  const nameParts = currentUser.value.name.split(' ');
  return nameParts[nameParts.length - 1];
});

// No longer need isCurrentRoute function since we removed active route styling

// Methods
const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value;
};

const toggleUserDropdown = () => {
  isUserDropdownOpen.value = !isUserDropdownOpen.value;
};

const closeUserDropdown = () => {
  isUserDropdownOpen.value = false;
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
  closeUserDropdown();
};

const handleLogin = () => {
  router.push('/login');
};

const handleLogout = () => {
  userStore.logout();
  closeUserDropdown();
  router.push('/');
};

const handleThemeToggle = () => {
  toggleTheme();
  // Don't close dropdown immediately to show the theme change
};

// Click outside handler
const handleClickOutside = (event: Event) => {
  const target = event.target as Element;
  if (!target.closest('.user-dropdown')) {
    closeUserDropdown();
  }
};

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
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
          <!-- Authenticated User Section -->
          <div v-if="isLoggedIn" class="flex items-center gap-3">
            <!-- Notification Dropdown -->
            <NotificationDropdown />
            
            <!-- User Profile Dropdown -->
             <div class="relative user-dropdown">
              <button 
                @click="toggleUserDropdown"
                @keydown.escape="closeUserDropdown"
                class="flex items-center gap-2 p-2 hover:bg-gray-800 rounded-lg transition-colors"
                aria-haspopup="true"
                :aria-expanded="isUserDropdownOpen"
                aria-label="User menu"
              >
                <img 
                  :src="currentUser?.avatar || 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=default%20user%20avatar&image_size=square'" 
                  :alt="currentUser?.name || 'User'"
                  class="w-8 h-8 rounded-full border-2 border-gray-600" 
                />
                <span class="hidden sm:block text-white font-medium">{{ userLastName }}</span>
                <ChevronDown 
                  :class="{ 'transform rotate-180': isUserDropdownOpen }"
                  class="w-4 h-4 text-gray-400 transition-transform"
                />
              </button>
              
              <!-- Dropdown Menu -->
              <div 
                v-if="isUserDropdownOpen"
                @click.stop
                class="absolute right-0 mt-2 w-48 bg-gray-800 rounded-lg shadow-xl border border-gray-700 py-2 z-50"
                role="menu"
                aria-orientation="vertical"
              >
                <div class="px-4 py-2 border-b border-gray-700">
                  <p class="text-sm font-medium text-white">{{ currentUser?.name }}</p>
                  <p class="text-xs text-gray-400">{{ currentUser?.email }}</p>
                </div>
                
                <div class="py-1">
                  <button
                    v-for="item in userMenuItems"
                    :key="item.name"
                    @click="navigateTo(item.path)"
                    class="w-full text-left px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-gray-700 transition-colors flex items-center gap-3"
                    role="menuitem"
                  >
                    <component :is="item.icon" class="w-4 h-4" />
                    {{ item.name }}
                  </button>
                  
                  <!-- Theme Toggle -->
                  <button
                    @click="handleThemeToggle"
                    class="w-full text-left px-4 py-2 text-sm text-gray-300 hover:text-white hover:bg-gray-700 transition-colors flex items-center gap-3"
                    role="menuitem"
                  >
                    <Sun v-if="isDark" class="w-4 h-4" />
                    <Moon v-else class="w-4 h-4" />
                    {{ isDark ? 'Light Mode' : 'Dark Mode' }}
                  </button>
                </div>
                
                <div class="border-t border-gray-700 py-1">
                  <button
                    @click="handleLogout"
                    class="w-full text-left px-4 py-2 text-sm text-red-400 hover:text-red-300 hover:bg-gray-700 transition-colors"
                    role="menuitem"
                  >
                    Logout
                  </button>
                </div>
              </div>
            </div>
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
        <div class="border-t border-gray-700 pt-4">
          <!-- Authenticated User (Mobile) -->
          <div v-if="isLoggedIn" class="space-y-3">
            <div class="flex items-center justify-between pb-3 border-b border-gray-700">
              <div class="flex items-center gap-3">
                <img 
                  :src="currentUser?.avatar || 'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=default%20user%20avatar&image_size=square'" 
                  :alt="currentUser?.name || 'User'"
                  class="w-10 h-10 rounded-full border-2 border-gray-600" 
                />
                <div>
                  <p class="text-white font-medium">{{ currentUser?.name }}</p>
                  <p class="text-xs text-gray-400">{{ currentUser?.email }}</p>
                </div>
              </div>
              <!-- Mobile Notification Dropdown -->
              <NotificationDropdown />
            </div>
            
            <div class="space-y-2">
              <button
                v-for="item in userMenuItems"
                :key="item.name"
                @click="navigateTo(item.path)"
                class="w-full text-left px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors flex items-center gap-3"
              >
                <component :is="item.icon" class="w-4 h-4" />
                {{ item.name }}
              </button>
              
              <!-- Theme Toggle (Mobile) -->
              <button
                @click="handleThemeToggle"
                class="w-full text-left px-4 py-3 text-gray-300 hover:text-white hover:bg-gray-800 rounded-lg transition-colors flex items-center gap-3"
              >
                <Sun v-if="isDark" class="w-4 h-4" />
                <Moon v-else class="w-4 h-4" />
                {{ isDark ? 'Light Mode' : 'Dark Mode' }}
              </button>
              
              <button
                @click="handleLogout"
                class="w-full text-left px-4 py-3 text-red-400 hover:text-red-300 hover:bg-gray-800 rounded-lg transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
          
          <!-- Guest User (Mobile) -->
          <div v-else class="space-y-3">
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
    </div>
  </header>
</template>

<style scoped>
/* Custom styles for the dark header */
</style>