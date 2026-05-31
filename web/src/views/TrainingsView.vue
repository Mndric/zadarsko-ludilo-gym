<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTreningStore } from '@/stores/treningi'
import { useAuthStore } from '@/stores/auth'
import UniverzalnaTablica, { type Stupac } from '@/components/UniverzalnaTablica.vue'
import FormaPolje from '@/components/FormaPolje.vue'

const treningStore = useTreningStore()
const authStore = useAuthStore()

// Reaktivne varijable za formu novog treninga
const noviNaslov = ref('')
const noviOpis = ref('')
const novaVrsta = ref('')
const noviKapacitet = ref(10)

// Lokalne varijable za klijentske greške u formi
const greskaNaslov = ref('')
const greskaOpis = ref('')
const greskaVrsta = ref('')
const greskaKapacitet = ref('')
const serverskaGreska = ref('')

// Definicija stupaca za našu reupotrebljivu tablicu
const stupci: Stupac[] = [
  { kljuc: 'title', oznaka: 'Naziv treninga' },
  { kljuc: 'description', oznaka: 'Opis' },
  { kljuc: 'type', oznaka: 'Vrsta' },
  { kljuc: 'capacity', oznaka: 'Kapacitet (broj ljudi)' }
]

// Dohvaćanje podataka pri učitavanju stranice (Uvjet iz projekta)
onMounted(() => {
  dohvatiPodatke()
})

function dohvatiPodatke() {
  treningStore.fetchTrainings()
}

// 1. Klijentska validacija (Uvjet za 2. obranu)
function validirajFormu(): boolean {
  let ispravno = true
  greskaNaslov.value = ''
  greskaOpis.value = ''
  greskaVrsta.value = ''
  greskaKapacitet.value = ''
  serverskaGreska.value = ''

  if (!noviNaslov.value.trim()) {
    greskaNaslov.value = 'Naziv treninga je obavezan.'
    ispravno = false
  }
  if (!noviOpis.value.trim()) {
    greskaOpis.value = 'Opis treninga je obavezan.'
    ispravno = false
  }
  if (!novaVrsta.value.trim()) {
    greskaVrsta.value = 'Morate unijeti vrstu treninga (npr. Crossfit, Pilates).'
    ispravno = false
  }
  if (noviKapacitet.value <= 0) {
    greskaKapacitet.value = 'Kapacitet mora biti broj veći od nule.'
    ispravno = false
  }

  return ispravno
}

// Slanje obrasca na backend
async function dodajNoviTrening() {
  if (!validirajFormu()) return // Zaustavi ako klijentska validacija padne

  try {
    await treningStore.dodajTrening({
      title: noviNaslov.value,
      description: noviOpis.value,
      type: novaVrsta.value,
      capacity: Number(noviKapacitet.value)
    })
    
    // Čišćenje forme nakon uspješnog dodavanja
    noviNaslov.value = ''
    noviOpis.value = ''
    novaVrsta.value = ''
    noviKapacitet.value = 10
  } catch (err: any) {
    // 2. Serverska validacija (Prikaz serverske greške korisniku)
    serverskaGreska.value = err
  }
}

function obrisi(id: number) {
  if (confirm('Jeste li sigurni da želite obrisati ovaj trening?')) {
    treningStore.obrisiTrening(id)
  }
}
</script>

<template>
  <div class="page-container">
    <div class="naslov-sekcija">
      <h1>Upravljanje Treninga</h1>
      <p>Pregled i kreiranje rasporeda treninga u dvorani.</p>
    </div>

    <div class="mreza-sadrzaja">
      <div class="tablica-sekcija">
        <h2>Popis Treninga</h2>
        <UniverzalnaTablica
          :stupci="stupci"
          :redovi="treningStore.items"
          :stanje="treningStore.stanje"
          :porukaGreske="treningStore.porukaGreske"
          @ponovno="dohvatiPodatke"
        >
          <template #akcije="{ red }">
            <button 
              v-if="authStore.isAdmin" 
              @click="obrisi(red.id)" 
              class="btn-brisi"
            >
              Obriši
            </button>
            <span v-else class="User-tekst">Nema akcija</span>
          </template>
        </UniverzalnaTablica>
      </div>

      <div class="forma-sekcija">
        <h2>Dodaj Novi Trening</h2>
        
        <div v-if="serverskaGreska" class="alert-greska">
          {{ serverskaGreska }}
        </div>

        <form @submit.prevent="dodajNoviTrening" novalidate class="forma-kartica">
          <FormaPolje
            oznaka="Naziv treninga"
            v-model="noviNaslov"
            :greska="greskaNaslov"
            :obavezno="true"
            placeholder="Npr. Jutarnji Cardio"
          />

          <FormaPolje
            oznaka="Opis treninga"
            v-model="noviOpis"
            :greska="greskaOpis"
            :obavezno="true"
            placeholder="Npr. Trening visokog intenziteta"
          />

          <FormaPolje
            oznaka="Vrsta"
            v-model="novaVrsta"
            :greska="greskaVrsta"
            :obavezno="true"
            placeholder="Npr. HIIT, Snaga"
          />

          <FormaPolje
            oznaka="Kapacitet"
            v-model="noviKapacitet"
            vrsta="number"
            :greska="greskaKapacitet"
            :obavezno="true"
          />

          <button type="submit" class="btn-potvrdi">
            Kreiraj Trening
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.naslov-sekcija {
  margin-bottom: 2rem;
}
.naslov-sekcija h1 {
  color: #2c3e50;
}
.mreza-sadrzaja {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
}
@media (max-width: 900px) {
  .mreza-sadrzaja {
    grid-template-columns: 1fr;
  }
}
h2 {
  font-size: 1.25rem;
  color: #34495e;
  margin-bottom: 1rem;
}
.forma-kartica {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.btn-potvrdi {
  width: 100%;
  background-color: #2ecc71;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 0.5rem;
}
.btn-potvrdi:hover {
  background-color: #27ae60;
}
.btn-brisi {
  background-color: #e74c3c;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}
.btn-brisi:hover {
  background-color: #c0392b;
}
.alert-greska {
  background-color: #fde8e8;
  color: #e74c3c;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  border: 1px solid #f8b4b4;
  font-size: 0.9rem;
}
.user-tekst {
  font-size: 0.85rem;
  color: #95a5a6;
  font-style: italic;
}
</style>