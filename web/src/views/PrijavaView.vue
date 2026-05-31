<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import FormaPolje from '@/components/FormaPolje.vue'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')

// Lokalne varijable za klijentske greške
const greskaKorisnickoIme = ref('')
const greskaLozinka = ref('')
const obavijestIsteka = ref(false)

// Provjeri je li korisnik preusmjeren zbog isteka tokena (iz interceptora)
onMounted(() => {
  if (route.query.expired === 'true') {
    obavijestIsteka.value = true
  }
})

// Klijentska validacija (Uvjet za 2. obranu)
function validirajFormu(): boolean {
  let ispravno = true
  greskaKorisnickoIme.value = ''
  greskaLozinka.value = ''

  if (!username.value.trim()) {
    greskaKorisnickoIme.value = 'Korisničko ime je obavezno.'
    ispravno = false
  }
  if (!password.value) {
    greskaLozinka.value = 'Lozinka je obavezna.'
    ispravno = false
  } else if (password.value.length < 4) {
    greskaLozinka.value = 'Lozinka mora imati barem 4 znaka.'
    ispravno = false
  }

  return ispravno
}

async function izvrsiPrijavu() {
  obavijestIsteka.value = false
  
  if (!validirajFormu()) return // Zaustavi slanje ako klijentska validacija padne[cite: 1]

  try {
    const uspjeh = await authStore.login(username.value, password.value)
    if (uspjeh) {
      router.push({ name: 'home' })
    }
  } catch (err) {
    // Greška se automatski sprema u authStore.error i prikazuje na ekranu
  }
}
</script>

<template>
  <div class="login-ekran">
    <div class="login-kartica">
      <h2>Prijava u Sustav</h2>
      
      <!-- Obavijest o isteku sesije iz interceptora -->
      <div v-if="obavijestIsteka" class="info-alert">
        Vaša sesija je istekla. Molimo prijavite se ponovno.
      </div>

      <!-- Globalna serverska greška (npr. krivi podaci bačeni s backenda) -->
      <div v-if="authStore.error" class="error-alert">
        {{ authStore.error }}
      </div>

      <form @submit.prevent="izvrsiPrijavu" novalidate>
        <FormaPolje
          oznaka="Korisničko ime"
          v-model="username"
          :greska="greskaKorisnickoIme"
          :obavezno="true"
          placeholder="Unesite korisničko ime"
        />

        <FormaPolje
          oznaka="Lozinka"
          v-model="password"
          vrsta="password"
          :greska="greskaLozinka"
          :obavezno="true"
          placeholder="Unesite lozinku"
        />

        <button type="submit" class="btn-prijava" :disabled="authStore.loading">
          {{ authStore.loading ? 'Prijava u tijeku...' : 'Prijavi se' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-ekran {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}
.login-kartica {
  background: white;
  padding: 2.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
}
h2 {
  margin-bottom: 1.5rem;
  color: #2c3e50;
  text-align: center;
}
.error-alert {
  background-color: #fde8e8;
  color: #e74c3c;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #f8b4b4;
  font-size: 0.9rem;
}
.info-alert {
  background-color: #e8f4fd;
  color: #3498db;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #b3e5fc;
  font-size: 0.9rem;
}
.btn-prijava {
  width: 100%;
  background-color: #3498db;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
}
.btn-prijava:hover {
  background-color: #2980b9;
}
.btn-prijava:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}
</style>