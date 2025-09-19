import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import './focus-styles.css'
import App from './App.vue'
import router from './router'

// Create Vue app instance
const app = createApp(App)
const pinia = createPinia()

// Use plugins
app.use(pinia)
app.use(router)

// Mount app
app.mount('#app')
