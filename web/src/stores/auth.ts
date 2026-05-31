import { defineStore } from 'pinia'
import apiClient from '@/api/client'
import type { AuthState, TokenResponse } from '@/types/api'
import type { Korisnik } from '@/types/korisnik'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null,
    token: localStorage.getItem('access_token') || null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state): boolean => !!state.token,
    isAdmin: (state): boolean => state.user?.role === 'admin'
  },

  actions: {
    async login(username: string, password: string): Promise<boolean> {
      this.loading = true
      this.error = null
      try {
        // FastAPI OAuth2PasswordRequestForm zahtijeva Form-Data format umjesto JSON-a!
        const formData = new URLSearchParams()
        formData.append('username', username)
        formData.append('password', password)

        const response = await apiClient.post<TokenResponse>('/login', formData, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })

        this.token = response.data.access_token
        localStorage.setItem('access_token', this.token)

        // Nakon uspješne prijave, odmah dohvaćamo profil prijavljenog korisnika
        await this.fetchCurrentUser()
        return true
      } catch (err: any) {
        this.error = err.response?.data?.detail || 'Prijava nije uspjela. Provjerite podatke.'
        throw this.error
      } finally {
        this.loading = false
      }
    },

    async fetchCurrentUser(): Promise<void> {
      if (!this.token) return
      try {
        const response = await apiClient.get<Korisnik>('/users/me')
        this.user = response.data
        localStorage.setItem('user', JSON.stringify(response.data))
      } catch {
        this.logout()
      }
    },

    logout(): void {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
    }
  }
})