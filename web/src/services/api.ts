import axios from 'axios'
 
export class ApiGreska extends Error {
  constructor(
    public readonly poruka: string,
    public readonly status: number
  ) {
    super(poruka)
    this.name = 'ApiGreska'
  }
}
 
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? 'http://localhost:8000',
})
 
// Request interceptor — dodaj Bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.set('Authorization', `Bearer ${token}`)
  return config
})
 
// Response interceptor — 401 → logout → /prijava
api.interceptors.response.use(
  (response) => response,
  async (error: unknown) => {
    if (!axios.isAxiosError(error) || !error.response) throw error
 
    const status = error.response.status
    const data = error.response.data as { detail?: string }
 
    if (status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/prijava'
      throw new ApiGreska('Sesija je istekla. Molimo prijavite se.', 401)
    }
 
    throw new ApiGreska(
      data.detail ?? error.message ?? 'Nepoznata greška',
      status
    )
  }
)
