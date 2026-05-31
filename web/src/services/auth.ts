import { api } from './api'
import type { TokenOdgovor } from '@/types/auth'
import type { KorisnikPodaci } from '@/types/korisnik'
 
export async function login(email: string, password: string): Promise<TokenOdgovor> {
  const form = new URLSearchParams()
  form.append('username', email)
  form.append('password', password)
  const { data } = await api.post<TokenOdgovor>('/auth/login', form, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
  return data
}
 
export async function getMe(): Promise<KorisnikPodaci> {
  const { data } = await api.get<KorisnikPodaci>('/auth/me')
  return data
}
 
export async function register(email: string, password: string): Promise<KorisnikPodaci> {
  const { data } = await api.post<KorisnikPodaci>('/auth/register', { email, password })
  return data
}
