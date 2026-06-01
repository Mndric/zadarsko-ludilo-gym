<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useOpremaStore }      from '@/stores/oprema'
import { useObavijestiStore } from '@/stores/obavijesti'
import { useAuthStore }        from '@/stores/auth' // <-- 1. UVOZIMO AUTH STORE
import { kreirajRezervaciju } from '@/services/gym'
import { ApiGreska } from '@/services/api'
import Modal from '@/components/Modal.vue'
import Gumb  from '@/components/Gumb.vue'
 
const opremaStore = useOpremaStore()
const obavijesti  = useObavijestiStore()
const auth        = useAuthStore() // <-- 2. INICIJALIZIRAMO AUTH STORE
 
const modalOtvoren     = ref(false)
const odabranaOpremaId = ref<number | null>(null)
const datumRezervacije  = ref('')
const rezerviramo      = ref(false)
 
onMounted(() => opremaStore.ucitaj())
 
function otvoriModal(id: number): void {
  odabranaOpremaId.value = id
  datumRezervacije.value = ''
  modalOtvoren.value = true
}
 
async function potvrdiRezervaciju(): Promise<void> {
  if (!odabranaOpremaId.value || !datumRezervacije.value) {
    obavijesti.greska('Odaberite datum rezervacije.')
    return
  }
  rezerviramo.value = true
  try {
    await kreirajRezervaciju({
      equipment_id: odabranaOpremaId.value,
      reservation_date: new Date(datumRezervacije.value).toISOString()
    })
    obavijesti.uspjeh('Rezervacija uspješno kreirana!')
    modalOtvoren.value = false
    await opremaStore.ucitaj()
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.poruka : 'Greška pri rezervaciji.')
  } finally {
    rezerviramo.value = false
  }
}
</script>
 
<template>
  <div class="pogled">
    <h1>Dostupna oprema</h1>
 
    <div v-if="opremaStore.ucitava" class="stanje-ucitavanje">
      <div class="spinner"></div>
      <span class="muted">Učitavanje opreme...</span>
    </div>
 
    <div v-else-if="opremaStore.greska" class="stanje-greska">
      {{ opremaStore.greska }}
      <Gumb vrsta="sekundarni" velicina="mali" @click="opremaStore.ucitaj()">Pokušaj ponovo</Gumb>
    </div>
 
    <div v-else-if="opremaStore.stavke.length === 0" class="stanje-prazno">
      <span>🏋️</span>
      <p>Nema dostupne opreme u teretani.</p>
    </div>
 
    <div v-else class="mreza-opreme">
      <div
        v-for="o in opremaStore.stavke"
        :key="o.id"
        class="kartica-opreme"
        :class="{ 'kartica-opreme--zauzeta': o.quantity === 0 }"
      >
        <div class="oprema-naziv">{{ o.name }}</div>
        <div class="oprema-kolicina">
          <span :class="o.quantity > 0 ? 'dostupno' : 'zauzeto'">
            {{ o.quantity > 0 ? `${o.quantity} dostupno` : 'Zauzeto' }}
          </span>
        </div>

        <Gumb
          v-if="!auth.user?.is_admin"
          velicina="mali"
          :onemoguceno="o.quantity === 0"
          @click="otvoriModal(o.id)"
        >
          {{ o.quantity > 0 ? 'Rezerviraj' : 'Nedostupno' }}
        </Gumb>

        <div v-else class="admin-pregled-tekst">
          <span>Pregled (Admin)</span>
        </div>
      </div>
    </div>
  </div>
 
  <Modal v-model="modalOtvoren" naslov="Nova rezervacija">
    <div class="modal-polje">
      <label>Datum i vrijeme rezervacije</label>
      <input
        v-model="datumRezervacije"
        type="datetime-local"
        class="modal-input"
        :min="new Date().toISOString().slice(0, 16)"
      />
    </div>
    <template #akcije>
      <Gumb vrsta="sekundarni" @click="modalOtvoren = false">Odustani</Gumb>
      <Gumb :ucitava="rezerviramo" @click="potvrdiRezervaciju">Potvrdi rezervaciju</Gumb>
    </template>
  </Modal>
</template>
 
<style scoped>
.pogled { display: flex; flex-direction: column; gap: 2rem; }
.stanje-ucitavanje { display: flex; align-items: center; gap: 1rem; padding: 2rem 0; color: var(--boja-tekst-mute); }
.stanje-greska { display: flex; align-items: center; gap: 1rem; padding: 1rem; border: 1px solid var(--boja-greska); color: var(--boja-greska); font-size: 0.875rem; }
.stanje-prazno { display: flex; flex-direction: column; align-items: center; gap: 1rem; padding: 4rem 0; color: var(--boja-tekst-mute); font-size: 0.875rem; }
.stanje-prazno span { font-size: 3rem; }
.mreza-opreme { display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 1rem; }
.kartica-opreme {
  background: var(--boja-povrsina); border: 1px solid var(--boja-rub);
  padding: 1.5rem; display: flex; flex-direction: column; gap: 1rem;
  transition: border-color var(--tranzicija);
}
.kartica-opreme:hover { border-color: var(--boja-akcent); }
.kartica-opreme--zauzeta { opacity: 0.5; }
.oprema-naziv { font-family: var(--font-display); font-weight: 700; font-size: 1.1rem; text-transform: uppercase; letter-spacing: 0.05em; }
.dostupno { color: var(--boja-uspjeh); font-size: 0.8rem; font-weight: 600; }
.zauzeto  { color: var(--boja-greska);  font-size: 0.8rem; }
.modal-polje { display: flex; flex-direction: column; gap: 0.5rem; }
.modal-polje label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; color: var(--boja-tekst-mute); }
.modal-input { background: var(--boja-pozadina); border: 1px solid var(--boja-rub); color: var(--boja-tekst); padding: 0.625rem 0.875rem; width: 100%; }
.modal-input:focus { outline: none; border-color: var(--boja-akcent); }
.spinner { width: 24px; height: 24px; border: 3px solid var(--boja-rub); border-top-color: var(--boja-akcent); border-radius: 50%; animation: spin 0.7s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Stil za natpis kad je admin u pregledu */
.admin-pregled-tekst {
  font-size: 0.75rem;
  color: var(--boja-tekst-mute);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border: 1px dashed var(--boja-rub);
  padding: 0.4rem;
  text-align: center;
}
</style>