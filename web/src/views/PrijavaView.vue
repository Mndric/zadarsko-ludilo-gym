<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useObavijestiStore } from '@/stores/obavijesti'
import { ApiGreska } from '@/services/api'
import FormaPolje from '@/components/FormaPolje.vue'
import Gumb from '@/components/Gumb.vue'
 
const router     = useRouter()
const auth       = useAuthStore()
const obavijesti = useObavijestiStore()
 
const email    = ref('')
const lozinka  = ref('')
const ucitava  = ref(false)
const greske   = ref({ email: '', lozinka: '' })
 
function validiraj(): boolean {
  greske.value.email   = email.value.includes('@') ? '' : 'Unesite valjanu email adresu.'
  greske.value.lozinka = lozinka.value.length >= 8  ? '' : 'Lozinka mora imati min. 8 znakova.'
  return !greske.value.email && !greske.value.lozinka
}
 
async function prijava(): Promise<void> {
  if (!validiraj()) return
  ucitava.value = true
  try {
    await auth.login(email.value, lozinka.value)
    await router.push(auth.isAdmin ? '/admin/pocetna' : '/pocetna')
  } catch (e) {
    const msg = e instanceof ApiGreska ? e.poruka : 'Greška pri prijavi.'
    obavijesti.greska(msg)
    if (msg.includes('lozink') || msg.includes('401')) greske.value.lozinka = 'Neispravan email ili lozinka.'
  } finally {
    ucitava.value = false
  }
}
</script>
 
<template>
  <div class="prijava">
    <div class="hero">
      <h1 class="logo">⚡ ZADARSKO<span class="logo-zuta"> LUDILO</span></h1>
      <p class="subtitle">GYM MANAGEMENT SYSTEM</p>
    </div>
 
    <form class="forma" @submit.prevent="prijava">
      <FormaPolje
        oznaka="Email"
        v-model="email"
        vrsta="email"
        :greska="greske.email"
        :obavezno="true"
      />
      <FormaPolje
        oznaka="Lozinka"
        v-model="lozinka"
        vrsta="password"
        :greska="greske.lozinka"
        :obavezno="true"
      />
      <Gumb tip="submit" :ucitava="ucitava" style="width:100%;justify-content:center;">
        Prijava
      </Gumb>
    </form>
 
    <p class="registracija-link">
      Nemate račun?
      <RouterLink to="/registracija" class="link">Registrirajte se</RouterLink>
    </p>
  </div>
</template>
 
<style scoped>
.prijava {
  width: 100%;
  max-width: 420px;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}
.hero { text-align: center; }
.logo {
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 3rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--boja-tekst);
  line-height: 1;
}
.logo-zuta { color: var(--boja-akcent); }
.subtitle {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: var(--boja-tekst-mute);
  margin-top: 0.5rem;
}
.forma {
  display: flex; flex-direction: column; gap: 1.25rem;
  padding: 2rem;
  background: var(--boja-povrsina);
  border: 1px solid var(--boja-rub);
  border-top: 3px solid var(--boja-akcent);
}
.registracija-link {
  text-align: center;
  font-size: 0.8rem;
  color: var(--boja-tekst-mute);
}
.link { color: var(--boja-akcent); transition: opacity var(--tranzicija); }
.link:hover { opacity: 0.75; }
</style>
