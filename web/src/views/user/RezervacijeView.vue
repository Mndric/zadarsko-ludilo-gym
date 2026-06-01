<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useObavijestiStore }              from '@/stores/obavijesti'
import { dohvatiMojeRezervacije, obrisiRezervaciju } from '@/services/gym'
import { ApiGreska } from '@/services/api'
import Gumb from '@/components/Gumb.vue'
import type { Rezervacija } from '@/types/rezervacija'
 
type Stanje = 'ucitavanje' | 'greska' | 'prazno' | 'spremno'
 
const obavijesti  = useObavijestiStore()
const rezervacije = ref<any[]>([]) // Privremeno stavljeno na any[] ako tip 'Rezervacija' još nema 'equipment' definiran
const stanje      = ref<Stanje>('ucitavanje')
const porukaGreske = ref('')
const brisemoId   = ref<number | null>(null)
 
async function ucitaj(): Promise<void> {
  stanje.value = 'ucitavanje'
  try {
    const podaci = await dohvatiMojeRezervacije()
    rezervacije.value = podaci
    stanje.value = podaci.length === 0 ? 'prazno' : 'spremno'
  } catch (e) {
    stanje.value = 'greska'
    porukaGreske.value = e instanceof Error ? e.message : 'Greška pri dohvatu rezervacija.'
  }
}
 
async function otkazi(id: number): Promise<void> {
  if (!confirm('Otkazati rezervaciju?')) return
  brisemoId.value = id
  try {
    await obrisiRezervaciju(id)
    obavijesti.uspjeh('Rezervacija otkazana.')
    await ucitaj()
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.poruka : 'Greška pri otkazivanju.')
  } finally {
    brisemoId.value = null
  }
}
 
// POPRAVLJENO FORMATIRANJE VREMENA
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
 
onMounted(ucitaj)
</script>
 
<template>
  <div class="pogled">
    <h1>Moje rezervacije</h1>
 
    <div v-if="stanje === 'ucitavanje'" class="stanje-ucitavanje">
      <div class="spinner"></div>
      <span class="muted">Učitavanje rezervacija...</span>
    </div>
 
    <div v-else-if="stanje === 'greska'" class="stanje-greska">
      ⚠ {{ porukaGreske }}
    </div>
 
    <div v-else-if="stanje === 'prazno'" class="stanje-prazno">
      <span>📅</span>
      <p>Nemate aktivnih rezervacija.</p>
      <RouterLink to="/oprema">
        <Gumb>Rezerviraj opremu</Gumb>
      </RouterLink>
    </div>
 
    <table v-else class="tablica">
      <thead>
        <tr>
          <th>#</th>
          <th>Oprema</th>
          <th>Datum rezervacije</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in rezervacije" :key="r.id">
          <td class="muted">{{ r.id }}</td>
          <td>{{ r.equipment?.name ?? `Oprema #${r.equipment_id}` }}</td>
          <td>{{ formatirajDatum(r.reservation_date) }}</td>
          <td>
            <Gumb
              vrsta="opasnost"
              velicina="mali"
              :ucitava="brisemoId === r.id"
              @click="otkazi(r.id)"
            >
              Otkaži
            </Gumb>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
 
<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; }
.stanje-ucitavanje { display: flex; align-items: center; gap: 1rem; padding: 2rem 0; }
.stanje-greska { padding: 1rem; border: 1px solid var(--boja-greska); color: var(--boja-greska); font-size: 0.875rem; }
.stanje-prazno { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem 0; color: var(--boja-tekst-mute); }
.stanje-prazno span { font-size: 3rem; }
.tablica { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.tablica th {
  text-align: left; padding: 0.625rem 1rem;
  font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em;
  color: var(--boja-tekst-mute); border-bottom: 2px solid var(--boja-rub);
}
.tablica td { padding: 0.75rem 1rem; border-bottom: 1px solid var(--boja-rub); }
.tablica tbody tr:hover td { background: var(--boja-povrsina); }
.spinner { width: 24px; height: 24px; border: 3px solid var(--boja-rub); border-top-color: var(--boja-akcent); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>