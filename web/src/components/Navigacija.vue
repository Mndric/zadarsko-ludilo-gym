<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
 
const auth = useAuthStore()
const router = useRouter()
 
async function odjava(): Promise<void> {
  auth.logout()
  await router.push('/prijava')
}
</script>
 
<template>
  <nav class="nav">
    <RouterLink to="/" class="brand">
      ⚡ ZADARSKO<span class="brand-akcent">LUDILO</span>
    </RouterLink>
 
    <!-- Admin linkovi -->
    <div v-if="auth.isAdmin" class="linkovi">
      <RouterLink to="/admin/pocetna" class="link">Dashboard</RouterLink>
      <RouterLink to="/admin/oprema"  class="link">Oprema</RouterLink>
      <RouterLink to="/oprema"        class="link">Pregled opreme</RouterLink>
    </div>
 
    <!-- Korisnik linkovi -->
    <div v-else-if="auth.isAuthenticated" class="linkovi">
      <RouterLink to="/pocetna"     class="link">Dashboard</RouterLink>
      <RouterLink to="/oprema"      class="link">Oprema</RouterLink>
      <RouterLink to="/rezervacije" class="link">Rezervacije</RouterLink>
      <RouterLink to="/clanarina"   class="link">Članarina</RouterLink>
    </div>
 
    <div v-if="auth.isAuthenticated" class="desno">
      <span class="email">{{ auth.user?.email }}</span>
      <span v-if="auth.isAdmin" class="badge-admin">ADMIN</span>
      <button class="gumb-odjava" @click="odjava">Odjava</button>
    </div>
  </nav>
</template>
 
<style scoped>
.nav {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 0 2rem;
  height: 60px;
  background: var(--boja-povrsina);
  border-bottom: 2px solid var(--boja-akcent);
  position: sticky;
  top: 0;
  z-index: 50;
}
.brand {
  font-family: var(--font-display);
  font-weight: 900;
  font-size: 1.3rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--boja-tekst);
  white-space: nowrap;
}
.brand-akcent { color: var(--boja-akcent); margin-left: 0.3rem; }
.linkovi { display: flex; align-items: center; gap: 0.25rem; flex: 1; }
.link {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  padding: 0.375rem 0.75rem;
  transition: color var(--tranzicija);
  border-bottom: 2px solid transparent;
  padding-bottom: calc(0.375rem + 2px);
}
.link:hover, .link.router-link-active { color: var(--boja-tekst); }
.link.router-link-active { border-bottom-color: var(--boja-akcent); }
.desno { margin-left: auto; display: flex; align-items: center; gap: 1rem; }
.email {
  font-size: 0.75rem;
  color: var(--boja-tekst-mute);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.badge-admin {
  font-size: 0.6rem;
  font-family: var(--font-display);
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 0.15rem 0.5rem;
  background: var(--boja-akcent);
  color: #0a0a0a;
}
.gumb-odjava {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--boja-tekst-mute);
  padding: 0.25rem 0.75rem;
  border: 1px solid var(--boja-rub);
  transition: color var(--tranzicija), border-color var(--tranzicija);
}
.gumb-odjava:hover { color: var(--boja-akcent); border-color: var(--boja-akcent); }
</style>
