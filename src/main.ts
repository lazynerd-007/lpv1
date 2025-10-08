import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/userStore'
import { useTheme } from './composables/useTheme'
import { measurePerformance, preloadCriticalImages } from './utils/performance'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize theme
const { initTheme } = useTheme()
initTheme()

// Check authentication status
const userStore = useUserStore()
userStore.checkAuthStatus()

// Performance optimizations
measurePerformance()

// Preload critical images (featured movie posters)
const criticalImages = [
  'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nollywood%20movie%20poster%20dramatic%20african%20cinema&image_size=portrait_4_3',
  'https://trae-api-sg.mchost.guru/api/ide/v1/text_to_image?prompt=nollywood%20action%20movie%20poster%20nigerian%20film&image_size=portrait_4_3'
]
preloadCriticalImages(criticalImages)

app.mount('#app')
