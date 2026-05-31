<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<template>
  <div class="page-container">
    <div class="admin-zaglavlje">
      <h1>Sigurnosna Admin Konzola</h1>
      <span class="sigurnosna-znacka">ZAKLJUČANO / ZAŠTIĆENO</span>
    </div>
    
    <p class="opis">Ovoj stranici možete pristupiti isključivo jer imate strogu **admin** ulogu dodijeljenu na backendu.</p>

    <div class="admin-panel">
      <div class="upozorenje-kutija">
        <h3>🛡️ Provjera Route Guarda Uspješna</h3>
        <p>Sustav je provjerio vaše JWT potpisane podatke u memoriji (`authStore.isAdmin`) i dopustio pristup ruti.</p>
      </div>

      <div class="admin-metrike">
        <div class="metrika-red">
          <strong>Identitet administratora:</strong>
          <span>{{ authStore.user?.username }}</span>
        </div>
        <div class="metrika-red">
          <strong>Backend Endpoint zaštita:</strong>
          <span>Aktivna (`/users/*` i destruktivni API pozivi)</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-zaglavlje {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 2px solid #e74c3c;
  padding-bottom: 1rem;
}
h1 {
  color: #c0392b;
}
.sigurnosna-znacka {
  background-color: #e74c3c;
  color: white;
  padding: 0.3rem 0.75rem;
  font-size: 0.8rem;
  font-weight: bold;
  border-radius: 4px;
}
.opis {
  color: #7f8c8d;
  margin-bottom: 2rem;
}
.admin-panel {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.upozorenje-kutija {
  background-color: #e8f8f5;
  border-left: 5px solid #2ecc71;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}
.upozorenje-kutija h3 {
  color: #27ae60;
  margin-bottom: 0.25rem;
}
.admin-metrike {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
}
.metrika-red {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #dee2e6;
}
.metrika-red:last-child {
  border-bottom: none;
}
</style>