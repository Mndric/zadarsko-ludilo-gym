<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore }      from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { dohvatiMojeRezervacije, aktivirajClanarinu } from '@/services/gym'
import { ApiGreska } from '@/services/api'
import Gumb from '@/components/Gumb.vue'
import type { Rezervacija } from '@/types/rezervacija'
 
const auth       = useAuthStore()
const obavijesti = useObavijestiStore()
 
const rezervacije = ref<Rezervacija[]>([])
const ucitava     = ref(true)
const greska      = ref('')
const aktiviraClanarinu = ref(false)
 
onMounted(async () => {
  try {
    rezervacije.value = await dohvatiMojeRezervacije()
    ucitava.value = false
  } catch (e) {
    greska.value = e instanceof Error ? e.message : 'Greška pri dohvatu.'
    ucitava.value = false
  }
})
 
async function kupiClanarinu(): Promise<void> {
  aktiviraClanarinu.value = true
  try {
    await aktivirajClanarinu()
    obavijesti.uspjeh('Članarina aktivirana! Sada možete rezervirati opremu.')
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.poruka : 'Greška pri aktivaciji.')
  } finally {
    aktiviraClanarinu.value = false
  }
}
 
function formatirajDatum(d: string): string {
  return new Date(d).toLocaleString('hr-HR')
}
</script>
 
<template>
  <div class="pogled">
    <div class="pozdrav">
      <h1>Dobrodošli, <span class="akcent">{{ auth.user?.email?.split('@')[0] }}</span>!</h1>
      <p class="muted">Zadarsko Ludilo Gym — upravljajte rezervacijama i članarinom</p>
    </div>
 
    <div class="kartice">
      <div class="kartica">
        <div class="kartica-zaglavlje">Moje rezervacije</div>
        <div v-if="ucitava" class="spinner"></div>
        <div v-else-if="greska" class="stanje-greska">{{ greska }}</div>
        <div v-else-if="rezervacije.length === 0" class="stanje-prazno">
          Nema aktivnih rezervacija.
        </div>
        <div v-else class="rezervacije-lista">
          <div v-for="r in rezervacije.slice(0, 5)" :key="r.id" class="rezervacija-red">
            <span class="oprema-id">Oprema #{{ r.equipment_id }}</span>
            <span class="datum muted">{{ formatirajDatum(r.reservation_date) }}</span>
          </div>
        </div>
        <RouterLink to="/rezervacije" class="vidi-sve">Vidi sve rezervacije →</RouterLink>
      </div>
 
      <div class="kartica kartica-clanarina">
        <div class="kartica-zaglavlje">Članarina</div>
        <p class="muted" style="margin-bottom:1rem">Aktivirajte članarinu kako biste mogli rezervirati opremu.</p>
        <Gumb :ucitava="aktiviraClanarinu" @click="kupiClanarinu">
          Aktiviraj Standard članarinu
        </Gumb>
      </div>
    </div>
  </div>
</template>
 
<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; }
.pozdrav { border-left: 4px solid var(--boja-akcent); padding-left: 1rem; }
.pozdrav h1 { font-size: 2rem; }
.kartice { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 1.5rem; }
.kartica {
  background: var(--boja-povrsina); border: 1px solid var(--boja-rub);
  padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem;
}
.kartica-zaglavlje {
  font-family: var(--font-display); font-weight: 700; font-size: 0.85rem;
  text-transform: uppercase; letter-spacing: 0.1em; color: var(--boja-akcent);
  border-bottom: 1px solid var(--boja-rub); padding-bottom: 0.75rem;
}
.kartica-clanarina { border-top: 3px solid var(--boja-akcent); }
.rezervacija-red {
  display: flex; justify-content: space-between; align-items: center;
  padding: 0.5rem 0; border-bottom: 1px solid var(--boja-rub); font-size: 0.875rem;
}
.oprema-id { font-weight: 600; }
.datum { font-size: 0.75rem; }
.vidi-sve { font-size: 0.75rem; color: var(--boja-akcent); text-transform: uppercase; letter-spacing: 0.08em; margin-top: auto; }
.stanje-prazno { color: var(--boja-tekst-mute); font-size: 0.875rem; padding: 0.5rem 0; }
.stanje-greska { color: var(--boja-greska); font-size: 0.875rem; }
.spinner { width: 24px; height: 24px; border: 3px solid var(--boja-rub); border-top-color: var(--boja-akcent); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
</style>
