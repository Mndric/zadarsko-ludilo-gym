<script setup lang="ts">
import { ref } from 'vue'
import { useObavijestiStore } from '@/stores/obavijesti'
import { aktivirajClanarinu } from '@/services/gym'
import { ApiGreska } from '@/services/api'
import Gumb from '@/components/Gumb.vue'
import type { Clanarina } from '@/types/clanarina'
 
const obavijesti  = useObavijestiStore()
const clanarina   = ref<Clanarina | null>(null)
const aktiviramo  = ref(false)
 
async function aktiviraj(): Promise<void> {
  aktiviramo.value = true
  try {
    clanarina.value = await aktivirajClanarinu()
    obavijesti.uspjeh('Standard članarina uspješno aktivirana!')
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.poruka : 'Greška pri aktivaciji.')
  } finally {
    aktiviramo.value = false
  }
}
 
function formatirajDatum(d: string): string {
  return new Date(d).toLocaleDateString('hr-HR')
}
</script>
 
<template>
  <div class="pogled">
    <h1>Moja članarina</h1>
 
    <div v-if="clanarina" class="kartica-aktivna">
      <div class="aktivna-zaglavlje">✓ ČLANARINA AKTIVNA</div>
      <div class="detalji">
        <div class="detalj">
          <span class="detalj-oznaka">Tip</span>
          <span class="detalj-vrijednost">{{ clanarina.type }}</span>
        </div>
        <div class="detalj">
          <span class="detalj-oznaka">Aktivirana</span>
          <span class="detalj-vrijednost">{{ formatirajDatum(clanarina.start_date) }}</span>
        </div>
      </div>
    </div>
 
    <div v-else class="kartica-kupnja">
      <h2>Standard Članarina</h2>
      <p class="muted">Aktivirajte članarinu kako biste mogli rezervirati opremu u teretani.</p>
      <ul class="benefiti">
        <li>✓ Pristup svoj opremi</li>
        <li>✓ Neograničene rezervacije</li>
        <li>✓ Prioritetni termini</li>
      </ul>
      <Gumb :ucitava="aktiviramo" @click="aktiviraj">
        Aktiviraj Standard članarinu
      </Gumb>
    </div>
  </div>
</template>
 
<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; max-width: 600px; }
.kartica-aktivna {
  background: var(--boja-povrsina); border: 1px solid var(--boja-uspjeh);
  padding: 2rem; display: flex; flex-direction: column; gap: 1.5rem;
}
.aktivna-zaglavlje {
  font-family: var(--font-display); font-weight: 700; font-size: 1.1rem;
  text-transform: uppercase; letter-spacing: 0.1em; color: var(--boja-uspjeh);
}
.detalji { display: flex; flex-direction: column; gap: 0.75rem; }
.detalj { display: flex; justify-content: space-between; font-size: 0.875rem; padding-bottom: 0.75rem; border-bottom: 1px solid var(--boja-rub); }
.detalj-oznaka { color: var(--boja-tekst-mute); text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.08em; }
.detalj-vrijednost { font-weight: 600; }
.kartica-kupnja {
  background: var(--boja-povrsina); border: 1px solid var(--boja-rub);
  border-top: 3px solid var(--boja-akcent); padding: 2rem;
  display: flex; flex-direction: column; gap: 1.25rem;
}
.kartica-kupnja h2 { font-size: 1.5rem; color: var(--boja-akcent); }
.benefiti { display: flex; flex-direction: column; gap: 0.5rem; color: var(--boja-tekst-mute); font-size: 0.875rem; }
.benefiti li { padding: 0.25rem 0; }
</style>
