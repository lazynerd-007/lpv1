<script setup lang="ts">
import { Facebook, Twitter, Instagram, Youtube, Mail, MapPin, Phone } from 'lucide-vue-next';

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Footer sections data
const footerSections = {
  discover: {
    title: 'Discover',
    links: [
      { name: 'Latest Pies', href: '/movies?rating=pie' },
      { name: 'Fresh Lemons', href: '/movies?rating=lemon' },
      { name: 'Trending Reviews', href: '/reviews/trending' },
      { name: 'Top Critics', href: '/critics' },
      { name: 'Nollywood News', href: '/news' }
    ]
  },
  genres: {
    title: 'Nollywood Genres',
    links: [
      { name: 'Comedy', href: '/movies?genre=comedy' },
      { name: 'Drama', href: '/movies?genre=drama' },
      { name: 'Action', href: '/movies?genre=action' },
      { name: 'Romance', href: '/movies?genre=romance' },
      { name: 'Thriller', href: '/movies?genre=thriller' }
    ]
  },
  regions: {
    title: 'Regional Cinema',
    links: [
      { name: 'Lagos Productions', href: '/movies?state=lagos' },
      { name: 'Enugu Films', href: '/movies?state=enugu' },
      { name: 'Kano Cinema', href: '/movies?state=kano' },
      { name: 'Abuja Movies', href: '/movies?state=abuja' },
      { name: 'All Regions', href: '/movies' }
    ]
  },
  company: {
    title: 'Company',
    links: [
      { name: 'About Us', href: '/about' },
      { name: 'Contact', href: '/contact' },
      { name: 'Privacy Policy', href: '/privacy' },
      { name: 'Terms of Service', href: '/terms' },
      { name: 'Advertise', href: '/advertise' }
    ]
  }
};

const socialLinks = [
  { name: 'Facebook', icon: Facebook, href: 'https://facebook.com/lemonnpie', color: 'hover:text-blue-600' },
  { name: 'Twitter', icon: Twitter, href: 'https://twitter.com/lemonnpie', color: 'hover:text-blue-400' },
  { name: 'Instagram', icon: Instagram, href: 'https://instagram.com/lemonnpie', color: 'hover:text-pink-600' },
  { name: 'YouTube', icon: Youtube, href: 'https://youtube.com/lemonnpie', color: 'hover:text-red-600' }
];

const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="bg-deep-navy text-cream-white">
    <!-- Main Footer Content -->
    <div class="container mx-auto px-4 py-12">
      <div class="flex justify-center">
        <!-- Brand Section -->
        <div class="max-w-md text-center">
          <div class="mb-6">
            <h3 class="text-2xl font-bold mb-2">
              <span class="text-lemon-yellow">🍋</span>
              LemonNPie
              <span class="text-nollywood-gold">🥧</span>
            </h3>
            <p class="text-cream-white/80 text-sm leading-relaxed">
              Celebrating the best and exposing the worst of Nollywood cinema. 
              Your trusted guide to Nigerian film excellence.
            </p>
          </div>
          
          <!-- Contact Info -->
          <div class="space-y-2 text-sm">
            <div class="flex items-center justify-center gap-2">
              <MapPin class="w-4 h-4 text-nollywood-gold" />
              <span>Lagos, Nigeria</span>
            </div>
            <div class="flex items-center justify-center gap-2">
              <Mail class="w-4 h-4 text-nollywood-gold" />
              <a href="mailto:hello@lemonnpie.com" class="hover:text-nollywood-gold transition-colors">
                hello@lemonnpie.com
              </a>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Newsletter Signup -->
      <div class="mt-12 pt-8 border-t border-cream-white/20">
        <div class="max-w-md mx-auto text-center">
          <h4 class="font-semibold text-nollywood-gold mb-2">Stay Updated</h4>
          <p class="text-cream-white/80 text-sm mb-4">
            Get the latest Nollywood reviews and news delivered to your inbox
          </p>
          <div class="flex gap-2">
            <input 
              type="email" 
              placeholder="Enter your email"
              class="input input-bordered input-sm flex-1 bg-cream-white/10 border-cream-white/30 text-cream-white placeholder-cream-white/60"
            />
            <button class="btn btn-primary btn-sm">
              Subscribe
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Bottom Footer -->
    <div class="bg-deep-navy/80 border-t border-cream-white/20">
      <div class="container mx-auto px-4 py-6">
        <div class="flex flex-col md:flex-row items-center justify-between gap-4">
          <!-- Copyright -->
          <div class="text-center md:text-left">
            <p class="text-cream-white/80 text-sm">
              © {{ currentYear }} LemonNPie. All rights reserved.
            </p>
            <p class="text-cream-white/60 text-xs mt-1">
              Proudly celebrating Nigerian cinema since 2024
            </p>
          </div>
          
          <!-- Social Links -->
          <div class="flex items-center gap-4">
            <span class="text-cream-white/80 text-sm hidden md:block">Follow us:</span>
            <div class="flex gap-3">
              <a 
                v-for="social in socialLinks" 
                :key="social.name"
                :href="social.href"
                target="_blank"
                rel="noopener noreferrer"
                :class="[
                  'p-2 rounded-full bg-cream-white/10 transition-all duration-300',
                  social.color
                ]"
                :aria-label="social.name"
              >
                <component :is="social.icon" class="w-4 h-4" />
              </a>
            </div>
          </div>
          
          <!-- Language Selector -->
          <div class="dropdown dropdown-top dropdown-end">
            <div tabindex="0" role="button" class="btn btn-ghost btn-sm text-cream-white/80">
              🇳🇬 English
            </div>
            <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-40 mb-2">
              <li><a>🇳🇬 English</a></li>
              <li><a>🇳🇬 Yoruba</a></li>
              <li><a>🇳🇬 Igbo</a></li>
              <li><a>🇳🇬 Hausa</a></li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Floating Back to Top Button -->
    <button 
      class="fixed bottom-6 right-6 btn btn-circle btn-primary shadow-lg hover:shadow-xl transition-all duration-300 z-40"
      @click="scrollToTop"
      aria-label="Back to top"
    >
      ↑
    </button>
  </footer>
</template>

<style scoped>
.dropdown:hover .dropdown-content {
  @apply block;
}

.input:focus {
  @apply border-nollywood-gold;
}

/* Custom scrollbar for better UX */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #FFD700;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #FFC107;
}
</style>