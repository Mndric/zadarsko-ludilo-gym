<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <div class="page-container mali-kontejner">
    <h1>Korisnički Profil</h1>
    <p class="podnaslov">Pregled vaših osobnih podataka spremljenih u bazi.</p>

    <div class="profil-kartica">
      <div class="profil-avatar">👤</div>
      
      <div class="profil-detalji">
        <div class="detalj-red">
          <span class="oznaka">Korisničko ime:</span>
          <span class="vrijednost">{{ authStore.user?.username }}</span>
        </div>
        
        <div class="detalj-red">
          <span class="oznaka">E-mail adresa:</span>
          <span class="vrijednost">{{ authStore.user?.email || 'Nije unesena' }}</span>
        </div>

        <div class="detalj-red">
          <span class="oznaka">Sustavna uloga:</span>
          <span class="vrijednost uloga-znacka" :class="authStore.user?.role">
            {{ authStore.user?.role }}
          </span>
        </div>

        <div class="detalj-red">
          <span class="oznaka">ID korisnika:</span>
          <span class="vrijednost monospaced">#{{ authStore.user?.id }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.mali-kontejner {
  max-width: 600px;
  margin: 0 auto;
}
h1 {
  color: #2c3e50;
  margin-bottom: 0.25rem;
}
.podnaslov {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
}
.profil-kartica {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}
.profil-avatar {
  font-size: 4rem;
  background: #f5f6fa;
  width: 90px;
  height: 90px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 50%;
}
.profil-detalji {
  width: 100%;
}
.detalj-red {
  display: flex;
  justify-content: space-between;
  padding: 0.85rem 0;
  border-bottom: 1px solid #f1f2f6;
}
.detalj-red:last-child {
  border-bottom: none;
}
.oznaka {
  color: #7f8c8d;
  font-weight: 500;
}
.vrijednost {
  color: #2c3e50;
  font-weight: 600;
}
.uloga-znacka {
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  text-transform: uppercase;
}
.uloga-znacka.admin {
  background-color: #fde8e8;
  color: #e74c3c;
}
.uloga-znacka.user {
  background-color: #e8f4fd;
  color: #3498db;
}
.monospaced {
  font-family: monospace;
  color: #95a5a6;
}
</style>