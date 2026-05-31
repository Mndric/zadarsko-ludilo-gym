import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, getMe } from '@/services/auth'
import type { KorisnikPodaci } from '@/types/korisnik'
 
export const useAuthStore = defineStore('auth', () => {
  const korisnik = ref<KorisnikPodaci | null>(null)
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
 
  const isAuthenticated = computed(() => !!accessToken.value && !!korisnik.value)
  const isAdmin = computed(() => !!korisnik.value?.is_admin)
  const user = computed(() => korisnik.value)
 
  async function login(email: string, password: string): Promise<void> {
    const tokenData = await apiLogin(email, password)
    accessToken.value = tokenData.access_token
    localStorage.setItem('access_token', tokenData.access_token)
    await dohvatiMene()
  }
 
  async function dohvatiMene(): Promise<void> {
    const podaci = await getMe()
    korisnik.value = podaci
  }
 
  function logout(): void {
    korisnik.value = null
    accessToken.value = null
    localStorage.removeItem('access_token')
  }
 
  return {
    korisnik, accessToken, isAuthenticated, isAdmin, user,
    login, logout, dohvatiMene
  }
})
