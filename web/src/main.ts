import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

import './styles/globalno.css'

async function bootApp(): Promise<void> {
  const app = createApp(App)
  const pinia = createPinia()
  
  app.use(pinia)

  // BOOT: Obnovi stanje korisnika iz tokena prije učitavanja routera
  if (localStorage.getItem('access_token')) {
    const authStore = useAuthStore(pinia)
    try {
      await authStore.fetchCurrentUser()
    } catch {
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
    }
  }

  app.use(router)
  app.mount('#app')
}

bootApp()