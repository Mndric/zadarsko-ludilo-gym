<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useOpremaStore }     from '@/stores/oprema'
import { useObavijestiStore } from '@/stores/obavijesti'
import FormaPolje from '@/components/FormaPolje.vue'
import Gumb       from '@/components/Gumb.vue'
import Modal      from '@/components/Modal.vue'
 
const opremaStore = useOpremaStore()
const obavijesti  = useObavijestiStore()
 
const modalOtvoren = ref(false)
const naziv        = ref('')
const kolicina     = ref('')
const dodajemo     = ref(false)
const greske       = ref({ naziv: '', kolicina: '' })
 
onMounted(() => opremaStore.ucitaj())
 
function validiraj(): boolean {
  greske.value.naziv    = naziv.value.trim().length >= 2  ? '' : 'Min. 2 znaka.'
  greske.value.kolicina = Number(kolicina.value) > 0      ? '' : 'Mora biti > 0.'
  return !greske.value.naziv && !greske.value.kolicina
}
 
async function dodajOpremu(): Promise<void> {
  if (!validiraj()) return
  dodajemo.value = true
  try {
    await opremaStore.dodaj({ name: naziv.value.trim(), quantity: Number(kolicina.value) })
    obavijesti.uspjeh(`Oprema "${naziv.value}" dodana.`)
    naziv.value = ''
    kolicina.value = ''
    modalOtvoren.value = false
  } catch (e) {
    obavijesti.greska(e instanceof Error ? e.message : 'Greška pri dodavanju.')
  } finally {
    dodajemo.value = false
  }
}
</script>
 
<template>
  <div class="pogled">
    <div class="zaglavlje">
      <h1>Upravljanje opremom</h1>
      <Gumb @click="modalOtvoren = true">+ Dodaj opremu</Gumb>
    </div>
 
    <!-- Loading -->
    <div v-if="opremaStore.ucitava" class="stanje-ucitavanje">
      <div class="spinner"></div>
      <span class="muted">Učitavanje...</span>
    </div>
 
    <!-- Error -->
    <div v-else-if="opremaStore.greska" class="stanje-greska">
      ⚠ {{ opremaStore.greska }}
      <Gumb vrsta="sekundarni" velicina="mali" @click="opremaStore.ucitaj()">Pokušaj ponovo</Gumb>
    </div>
 
    <!-- Empty -->
    <div v-else-if="opremaStore.stavke.length === 0" class="stanje-prazno">
      <span>📦</span>
      <p>Nema opreme. Dodajte prvu spravu.</p>
    </div>
 
    <!-- Table -->
    <table v-else class="tablica">
      <thead>
        <tr>
          <th>ID</th>
          <th>Naziv</th>
          <th>Dostupno</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="o in opremaStore.stavke" :key="o.id">
          <td class="muted">#{{ o.id }}</td>
          <td class="naziv">{{ o.name }}</td>
          <td>{{ o.quantity }}</td>
          <td>
            <span :class="['status-badge', o.quantity > 0 ? 'status-badge--dostupno' : 'status-badge--zauzeto']">
              {{ o.quantity > 0 ? 'Dostupno' : 'Zauzeto' }}
            </span>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
 
  <Modal v-model="modalOtvoren" naslov="Dodaj novu opremu">
    <FormaPolje oznaka="Naziv opreme" v-model="naziv" :greska="greske.naziv" :obavezno="true" pomoc="npr. Bučice 10kg, Klupa za bench press" />
    <FormaPolje oznaka="Količina" v-model="kolicina" vrsta="number" :greska="greske.kolicina" :obavezno="true" />
    <template #akcije>
      <Gumb vrsta="sekundarni" @click="modalOtvoren = false">Odustani</Gumb>
      <Gumb :ucitava="dodajemo" @click="dodajOpremu">Dodaj opremu</Gumb>
    </template>
  </Modal>
</template>
 
<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; }
.zaglavlje { display: flex; align-items: center; justify-content: space-between; }
.stanje-ucitavanje { display: flex; align-items: center; gap: 1rem; padding: 2rem 0; }
.stanje-greska { display: flex; align-items: center; gap: 1rem; padding: 1rem; border: 1px solid var(--boja-greska); color: var(--boja-greska); }
.stanje-prazno { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem 0; color: var(--boja-tekst-mute); }
.stanje-prazno span { font-size: 3rem; }
.tablica { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.tablica th { text-align: left; padding: 0.625rem 1rem; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--boja-tekst-mute); border-bottom: 2px solid var(--boja-rub); }
.tablica td { padding: 0.75rem 1rem; border-bottom: 1px solid var(--boja-rub); }
.tablica tbody tr:hover td { background: var(--boja-povrsina); }
.naziv { font-weight: 600; }
.status-badge { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.1em; padding: 0.2rem 0.5rem; border: 1px solid currentColor; }
.status-badge--dostupno { color: var(--boja-uspjeh); }
.status-badge--zauzeto  { color: var(--boja-greska); }
.spinner { width: 24px; height: 24px; border: 3px solid var(--boja-rub); border-top-color: var(--boja-akcent); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
