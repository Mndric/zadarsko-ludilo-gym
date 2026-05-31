import axios, { type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import router from '@/router'

const apiClient = axios.create({
  baseURL: (import.meta.env.VITE_API_URL as string) || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request Interceptor: Automatsko lijepljenje Bearer tokena
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response Interceptor: Hvatanje 401 grešaka i preusmjeravanje (Auth Flow uvjet)
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Čišćenje lokalnog stanja
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      
      // Preusmjeri na login s query parametrom kako bismo obavijestili korisnika
      router.push({ name: 'login', query: { expired: 'true' } })
    }
    return Promise.reject(error)
  }
)

export default apiClient