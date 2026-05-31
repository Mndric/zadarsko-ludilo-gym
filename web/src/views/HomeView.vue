<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useTreningStore } from '@/stores/treningi'
import { onMounted, computed } from 'vue'

const authStore = useAuthStore()
const treningStore = useTreningStore()

onMounted(() => {
  // Dohvaćamo treninge kako bismo na početnoj prikazali točan broj
  treningStore.fetchTrainings()
})

const brojTreninga = computed(() => treningStore.items.length)
</script>

<template>
  <div class="page-container">
    <div class="dobrodoslica-sekcija">
      <h1>Pozdrav, {{ authStore.user?.username }}! 👋</h1>
      <p>Dobrodošli natrag u sustav **Zadarsko Ludilo Gym**.</p>
    </div>

    <div class="nadzorna-ploca-mreza">
      <div class="stat-kartica">
        <div class="stat-ikona">🏋️‍♂️</div>
        <div class="stat-podaci">
          <h3>Dostupni Treninzi</h3>
          <p class="stat-broj">{{ brojTreninga }}</p>
        </div>
      </div>

      <div class="stat-kartica">
        <div class="stat-ikona">🔐</div>
        <div class="stat-podaci">
          <h3>Razina Pristupa</h3>
          <p class="stat-broj uloga-tekst">{{ authStore.user?.role }}</p>
        </div>
      </div>

      <div class="stat-kartica">
        <div class="stat-ikona">🟢</div>
        <div class="stat-podaci">
          <h3>Status Veze</h3>
          <p class="stat-broj status-tekst">Aktivna</p>
        </div>
      </div>
    </div>

    <div class="brze-akcije">
      <h2>Brzi prečaci</h2>
      <div class="gumbi-prečaci">
        <RouterLink to="/trainings" class="link-gumb">Upravljanje Treninga</RouterLink>
        <RouterLink to="/profile" class="link-gumb sekundarni">Pregled Profila</RouterLink>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dobrodoslica-sekcija {
  margin-bottom: 2.5rem;
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.dobrodoslica-sekcija h1 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}
.nadzorna-ploca-mreza {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}
.stat-kartica {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.stat-ikona {
  font-size: 2.5rem;
}
.stat-podaci h3 {
  margin-bottom: 0.25rem;
  color: #7f8c8d;
  font-size: 0.95rem;
}
.stat-broj {
  font-size: 1.75rem;
  font-weight: bold;
  color: #2c3e50;
}
.uloga-tekst {
  text-transform: uppercase;
  color: #3498db;
  font-size: 1.4rem;
}
.status-tekst {
  color: #2ecc71;
  font-size: 1.4rem;
}
.brze-akcije {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}
.brze-akcije h2 {
  color: #34495e;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}
.gumbi-prečaci {
  display: flex;
  gap: 1rem;
}
.link-gumb {
  background-color: #3498db;
  color: white;
  text-decoration: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  font-weight: bold;
  transition: background 0.2s;
}
.link-gumb:hover {
  background-color: #2980b9;
}
.link-gumb.sekundarni {
  background-color: #95a5a6;
}
.link-gumb.sekundarni:hover {
  background-color: #7f8c8d;
}
</style>