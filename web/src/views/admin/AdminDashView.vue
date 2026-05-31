<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
const auth = useAuthStore()
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
</style>
