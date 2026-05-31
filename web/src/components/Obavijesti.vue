<script setup lang="ts">
import { useObavijestiStore } from '@/stores/obavijesti'
const store = useObavijestiStore()
</script>
 
<template>
  <Teleport to="body">
    <div class="kontejner">
      <TransitionGroup name="obavijest">
        <div
          v-for="o in store.stavke"
          :key="o.id"
          :class="['obavijest', `obavijest--${o.vrsta}`]"
          @click="store.ukloni(o.id)"
        >
          <span>{{ o.poruka }}</span>
          <button class="zatvori">×</button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>
 
<style scoped>
.kontejner {
  position: fixed; bottom: 1.5rem; right: 1.5rem;
  display: flex; flex-direction: column; gap: 0.5rem; z-index: 1000;
}
.obavijest {
  display: flex; align-items: center; justify-content: space-between; gap: 1rem;
  padding: 0.75rem 1rem;
  border: 1px solid var(--boja-rub);
  background: var(--boja-povrsina);
  cursor: pointer; min-width: 280px; max-width: 420px;
  font-size: 0.8rem;
}
.obavijest--uspjeh { border-left: 3px solid var(--boja-uspjeh); color: var(--boja-uspjeh); }
.obavijest--greska { border-left: 3px solid var(--boja-greska); color: var(--boja-greska); }
.obavijest--info   { border-left: 3px solid var(--boja-akcent); color: var(--boja-tekst); }
.zatvori { font-size: 1.25rem; opacity: 0.6; flex-shrink: 0; }
.obavijest-enter-active, .obavijest-leave-active { transition: all 200ms ease; }
.obavijest-enter-from, .obavijest-leave-to { opacity: 0; transform: translateX(1rem); }
</style>
