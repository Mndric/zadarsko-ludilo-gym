<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import axios from 'axios' // Ili koristi svoj @/services/gym ako imaš predefiniran klijent

const auth = useAuthStore()

interface Rezervacija {
  id: int
  user_id: int
  equipment_id: int
  reservation_date: string
}

const sveRezervacije = ref<Rezervacija[]>([])
const ucitava = ref(true)
const greska = ref('')

onMounted(async () => {
  try {
    // Šaljemo zahtjev na novu admin rutu (provjeri koristiš li bazu na portu 8000)
    const token = localStorage.getItem('token') // dohvaćamo token za check_admin autorizaciju
    const response = await axios.get('http://localhost:8000/gym/admin/all-reservations', {
      headers: { Authorization: `Bearer ${token}` }
    })
    sveRezervacije.value = response.data
    ucitava.value = false
  } catch (e) {
    greska.value = 'Greška pri dohvatu popisa rezervacija.'
    ucitava.value = false
  }
})

function formatirajDatum(d: string): string {
  if (!d) return ''
  const utcString = d.endsWith('Z') ? d : d + 'Z'
  return new Date(utcString).toLocaleString('hr-HR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<template>
  <div class="pogled">
    <div class="zaglavlje">
      <h1>Admin dashboard</h1>
      <span class="badge-admin">ADMINISTRATOR</span>
    </div>
    <p class="muted">Prijavljeni kao: {{ auth.user?.email }}</p>

    <div class="kartice">
      <RouterLink to="/admin/oprema" class="kartica-link">
        <div class="kartica">
          <div class="kartica-ikona">🏋️</div>
          <div class="kartica-naslov">Upravljanje opremom</div>
          <p class="kartica-opis muted">Dodajte novu opremu, upravljajte zalihama i pregledajte svu dostupnu opremu.</p>
        </div>
      </RouterLink>
    </div>

    <div class="sekcija-rezervacije">
      <h2>Sve aktivne rezervacije u teretani</h2>
      
      <div v-if="ucitava" class="spinner"></div>
      <div v-else-if="greska" class="stanje-greska">{{ greska }}</div>
      <div v-else-if="sveRezervacije.length === 0" class="stanje-prazno">
        Trenutno nema niti jedne aktivne rezervacije korisnika.
      </div>
      
      <div v-else class="tablica-kontejner">
        <table class="admin-tablica">
          <thead>
            <tr>
              <th>ID Rezervacije</th>
              <th>ID Korisnika</th>
              <th>ID Opreme</th>
              <th>Datum i Vrijeme</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in sveRezervacije" :key="r.id">
              <td>#{{ r.id }}</td>
              <td><span class="user-badge">Korisnik #{{ r.user_id }}</span></td>
              <td>Oprema #{{ r.equipment_id }}</td>
              <td class="datum-tekst">{{ formatirajDatum(r.reservation_date) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; }
.zaglavlje { display: flex; align-items: center; gap: 1rem; }
.badge-admin {
  font-family: var(--font-display); font-size: 0.65rem; font-weight: 700;
  letter-spacing: 0.1em; padding: 0.2rem 0.6rem;
  background: var(--boja-akcent); color: #0a0a0a;
}
.kartice { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
.kartica-link { text-decoration: none; }
.kartica {
  background: var(--boja-povrsina); border: 1px solid var(--boja-rub);
  padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem;
  transition: border-color var(--tranzicija), transform 150ms ease;
  cursor: pointer;
}
.kartica:hover { border-color: var(--boja-akcent); transform: translateY(-2px); }
.kartica-ikona { font-size: 2.5rem; }
.kartica-naslov { font-family: var(--font-display); font-weight: 700; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.05em; }
.kartica-opis { font-size: 0.8rem; line-height: 1.5; }

/* Stilovi za novu tablicu rezervacija */
.sekcija-rezervacije {
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.sekcija-rezervacije h2 {
  font-size: 1.25rem;
  font-family: var(--font-display);
}
.tablica-kontejner { overflow-x: auto; }
.admin-tablica {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.9rem;
}
.admin-tablica th, .admin-tablica td {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--boja-rub);
}
.admin-tablica th {
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  color: var(--boja-akcent);
}
.user-badge {
  background: rgba(255,255,255,0.05);
  padding: 0.2rem 0.4rem;
  border-radius: 4px;
  font-weight: 600;
}
.datum-tekst { color: var(--boja-tekst-mute); }
.spinner { width: 24px; height: 24px; border: 3px solid var(--boja-rub); border-top-color: var(--boja-akcent); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.stanje-prazno { color: var(--boja-tekst-mute); font-size: 0.9rem; }
.stanje-greska { color: var(--boja-greska); font-size: 0.9rem; }
</style>