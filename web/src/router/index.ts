import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
 
// Stranice — lazy load za bolji performance
const PrijavaView       = () => import('@/views/PrijavaView.vue')
const RegistracijaView  = () => import('@/views/RegistracijaView.vue')
const NepoznatoView     = () => import('@/views/NepoznatoView.vue')
 
// Korisničke stranice
const DashboardView     = () => import('@/views/user/DashboardView.vue')
const OpremaView        = () => import('@/views/user/OpremaView.vue')
const RezervacijeView   = () => import('@/views/user/RezervacijeView.vue')
const ClanarinaView     = () => import('@/views/user/ClanarinaView.vue')
 
// Admin stranice
const AdminDashView     = () => import('@/views/admin/AdminDashView.vue')
const AdminOpremaView   = () => import('@/views/admin/AdminOpremaView.vue')
 
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: () => {
        const auth = useAuthStore()
        if (!auth.isAuthenticated) return '/prijava'
        return auth.isAdmin ? '/admin/pocetna' : '/pocetna'
      }
    },
    {
      path: '/prijava',
      component: PrijavaView,
      meta: { layout: 'gost', javno: true }
    },
    {
      path: '/registracija',
      component: RegistracijaView,
      meta: { layout: 'gost', javno: true }
    },
    // ── Korisničke rute ──────────────────────────────────────────
    {
      path: '/pocetna',
      component: DashboardView,
      meta: { layout: 'app' }
    },
    {
      path: '/oprema',
      component: OpremaView,
      meta: { layout: 'app' }
    },
    {
      path: '/rezervacije',
      component: RezervacijeView,
      meta: { layout: 'app' }
    },
    {
      path: '/clanarina',
      component: ClanarinaView,
      meta: { layout: 'app' }
    },
    // ── Admin rute (zaštićene) ────────────────────────────────────
    {
      path: '/admin',
      meta: { layout: 'app', uloga: 'admin' },
      children: [
        { path: 'pocetna',  component: AdminDashView },
        { path: 'oprema',   component: AdminOpremaView },
      ]
    },
    // 404
    {
      path: '/:catchAll(.*)*',
      component: NepoznatoView,
      meta: { layout: 'gost', javno: true }
    }
  ]
})
 
// ── Navigation Guard ─────────────────────────────────────────────────────
router.beforeEach((to) => {
  const auth = useAuthStore()
 
  // Javna stranica
  if (to.meta.javno) {
    if (auth.isAuthenticated)
      return auth.isAdmin ? '/admin/pocetna' : '/pocetna'
    return true
  }
 
  // Nije prijavljen → login
  if (!auth.isAuthenticated) return '/prijava'
 
  // Admin stranica dostupna samo adminu
  if (to.meta.uloga === 'admin' && !auth.isAdmin) return '/pocetna'
 
  return true
})
 
export default router
