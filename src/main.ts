import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import './focus-styles.css'
import App from './App.vue'
import router from './router'
import { useUserStore } from './stores/userStore'

// Create Vue app instance
const app = createApp(App)
const pinia = createPinia()

// Use plugins
app.use(pinia)
app.use(router)

// Initialize authentication status
const initializeAuth = async () => {
  const userStore = useUserStore()
  await userStore.checkAuthStatus()
}

// Mount app and initialize auth
initializeAuth().then(() => {
  app.mount('#app')
}).catch((error) => {
  console.error('Failed to initialize authentication:', error)
  app.mount('#app') // Mount anyway
})
