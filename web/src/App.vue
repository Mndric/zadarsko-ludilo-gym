<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

function odjava() {
  authStore.logout()
  router.push({ name: 'login' })
}
</script>

<template>
  <div class="aplikacija-kontejner">
    <!-- Navigacijska traka: Prikazuje se samo ako je korisnik autentificiran -->
    <nav v-if="authStore.isAuthenticated" class="glavna-navigacija">
      <div class="nav-brand">Sustav Treninga</div>
      <div class="nav-linkovi">
        <RouterLink to="/" class="nav-link">Početna</RouterLink>
        <RouterLink to="/trainings" class="nav-link">Treninzi</RouterLink>
        <RouterLink to="/profile" class="nav-link">Profil</RouterLink>
        <!-- Admin link vidljiv samo korisnicima s rolo 'admin' -->
        <RouterLink v-if="authStore.isAdmin" to="/admin" class="nav-link admin-link">
          Admin Panel
        </RouterLink>
      </div>
      <div class="nav-korisnik">
        <span class="korisnik-ime">{{ authStore.user?.username }} ({{ authStore.user?.role }})</span>
        <button @click="odjava" class="btn-odjava">Odjavi se</button>
      </div>
    </nav>

    <!-- Glavni sadržaj gdje router ubacuje komponente (Views) -->
    <main class="glavni-sadrzaj">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.aplikacija-kontejner {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: sans-serif;
}
.glavna-navigacija {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #2c3e50;
  color: white;
  padding: 1rem 2rem;
}
.nav-brand {
  font-size: 1.25rem;
  font-weight: bold;
}
.nav-linkovi {
  display: flex;
  gap: 1.5rem;
}
.nav-link {
  color: #ecf0f1;
  text-decoration: none;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
}
.nav-link:hover, .router-link-active {
  background-color: #34495e;
  color: #3498db;
}
.admin-link {
  border: 1px dashed #e74c3c;
  color: #e74c3c;
}
.admin-link:hover, .router-link-active.admin-link {
  background-color: #e74c3c;
  color: white;
}
.nav-korisnik {
  display: flex;
  align-items: center;
  gap: 1rem;
}
.korisnik-ime {
  font-size: 0.9rem;
  color: #bdc3c7;
}
.btn-odjava {
  background-color: #c0392b;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
}
.btn-odjava:hover {
  background-color: #e74c3c;
}
.glavni-sadrzaj {
  flex: 1;
  padding: 2rem;
  background-color: #f5f6fa;
}
</style>