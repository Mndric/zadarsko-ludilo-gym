import axios from 'axios'
import router from '@/router'

// 1. Kreiramo Axios instancu prema tvom FastAPI backendu
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 2. PRESRETAČ ZA ZAHTJEVE (Request Interceptor)
// Prije nego što bilo koji zahtjev ode na backend, provjeravamo imamo li token i lijepimo ga
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 3. PRESRETAČ ZA ODGOVORE (Response Interceptor)
// Ako backend vrati grešku 401 (što znači da je token istekao ili ne valja), brišemo sve i preusmjeravamo na login
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Token više ne vrijedi -> brišemo ga iz memorije
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      
      // Automatski preusmjeri korisnika na Login stranicu s porukom da je sesija istekla
      router.push({ name: 'login', query: { expired: 'true' } })
    }
    return Promise.reject(error)
  }
)

export default apiClient