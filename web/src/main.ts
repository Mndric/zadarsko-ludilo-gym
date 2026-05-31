import { createApp }   from 'vue'
import { createPinia }  from 'pinia'
import App    from './App.vue'
import router from './router'
import './styles/globalno.css'
import { useAuthStore }      from './stores/auth'
import { useObavijestiStore } from './stores/obavijesti'
 
const pinia     = createPinia()
const aplikacija = createApp(App)
aplikacija.use(pinia)
 
// Boot: provjeri token PRIJE routera
if (localStorage.getItem('access_token')) {
  try {
    await useAuthStore(pinia).dohvatiMene()
  } catch {
    localStorage.removeItem('access_token')
  }
}
 
aplikacija.use(router)
 
aplikacija.config.errorHandler = (err) => {
  const poruka = err instanceof Error ? err.message : 'Neočekivana greška.'
  useObavijestiStore(pinia).greska(poruka)
}
 
aplikacija.mount('#app')
