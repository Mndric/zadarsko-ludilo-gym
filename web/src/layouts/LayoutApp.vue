<script setup lang="ts">
import Navigacija from '@/components/Navigacija.vue'
</script>
 
<template>
  <div class="layout-app">
    <Navigacija />
    <main class="sadrzaj">
      <slot />
    </main>
  </div>
</template>
 
<style scoped>
.layout-app {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr;
}
.sadrzaj {
  padding: 2rem;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}
</style>
