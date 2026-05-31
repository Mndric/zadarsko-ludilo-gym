<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { register } from '@/services/auth'
import { ApiGreska } from '@/services/api'
import FormaPolje from '@/components/FormaPolje.vue'
import Gumb from '@/components/Gumb.vue'
 
const router     = useRouter()
const auth       = useAuthStore()
const obavijesti = useObavijestiStore()
 
const email        = ref('')
const lozinka      = ref('')
const lozinkaPotvr = ref('')
const ucitava      = ref(false)
const greske       = ref({ email: '', lozinka: '', lozinkaPotvr: '' })
 
function validiraj(): boolean {
  greske.value.email        = email.value.includes('@') ? '' : 'Unesite valjanu email adresu.'
  greske.value.lozinka      = lozinka.value.length >= 8  ? '' : 'Min. 8 znakova.'
  greske.value.lozinkaPotvr = lozinka.value === lozinkaPotvr.value ? '' : 'Lozinke se ne podudaraju.'
  return !Object.values(greske.value).some(Boolean)
}
 
async function registracija(): Promise<void> {
  if (!validiraj()) return
  ucitava.value = true
  try {
    await register(email.value, lozinka.value)
    obavijesti.uspjeh('Registracija uspješna! Molimo se prijavite.')
    await router.push('/prijava')
  } catch (e) {
    obavijesti.greska(e instanceof ApiGreska ? e.poruka : 'Greška pri registraciji.')
  } finally {
    ucitava.value = false
  }
}
</script>
 
<template>
  <div class="stranica">
    <div class="hero">
      <h1 class="logo">⚡ ZADARSKO<span class="logo-zuta"> LUDILO</span></h1>
      <p class="subtitle">REGISTRACIJA NOVOG KORISNIKA</p>
    </div>
    <form class="forma" @submit.prevent="registracija">
      <FormaPolje oznaka="Email" v-model="email" vrsta="email" :greska="greske.email" :obavezno="true" />
      <FormaPolje oznaka="Lozinka" v-model="lozinka" vrsta="password" :greska="greske.lozinka" :obavezno="true" pomoc="Minimalno 8 znakova" />
      <FormaPolje oznaka="Potvrda lozinke" v-model="lozinkaPotvr" vrsta="password" :greska="greske.lozinkaPotvr" :obavezno="true" />
      <Gumb tip="submit" :ucitava="ucitava" style="width:100%;justify-content:center;">
        Registriraj se
      </Gumb>
    </form>
    <p class="prijava-link">
      Već imate račun?
      <RouterLink to="/prijava" class="link">Prijavite se</RouterLink>
    </p>
  </div>
</template>
 
<style scoped>
.stranica { width: 100%; max-width: 420px; display: flex; flex-direction: column; gap: 2rem; }
.hero { text-align: center; }
.logo {
  font-family: var(--font-display); font-weight: 900;
  font-size: 3rem; letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--boja-tekst); line-height: 1;
}
.logo-zuta { color: var(--boja-akcent); }
.subtitle { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.2em; color: var(--boja-tekst-mute); margin-top: 0.5rem; }
.forma {
  display: flex; flex-direction: column; gap: 1.25rem; padding: 2rem;
  background: var(--boja-povrsina); border: 1px solid var(--boja-rub);
  border-top: 3px solid var(--boja-akcent);
}
.prijava-link { text-align: center; font-size: 0.8rem; color: var(--boja-tekst-mute); }
.link { color: var(--boja-akcent); }
</style>

