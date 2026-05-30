import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// Definiramo naše stranice (minimalno 5 kako traži profesor)
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guest: true } // Samo za neprijavljene
    },
    {
      path: '/',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
      meta: { requiresAuth: true } // Treba login
    },
    {
      path: '/trainings',
      name: 'trainings',
      component: () => import('../views/TrainingsView.vue'),
      meta: { requiresAuth: true } // Treba login
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/ProfileView.vue'),
      meta: { requiresAuth: true } // Treba login
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/AdminView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true } // Treba login I admin rola!
    }
  ]
})

// KLJUČNI DIO: Route Guard (Provjera prije svakog prelaska na stranicu)
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 1. Ako stranica zahtijeva login, a korisnik nije prijavljen -> šalji na login
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' })
  } 
  // 2. Ako je stranica samo za admine, a korisnik nije admin -> šalji na home
  else if (to.meta.requiresAdmin && !authStore.isAdmin) {
    next({ name: 'home' })
  }
  // 3. Ako je korisnik već prijavljen, a pokuša otići na login -> šalji na home
  else if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'home' })
  }
  else {
    next() // Pusti ga dalje
  }
})

export default router