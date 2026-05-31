<script setup lang="ts">
defineProps<{
  vrsta?: 'primarni' | 'sekundarni' | 'opasnost'
  velicina?: 'mali' | 'normalni'
  ucitava?: boolean
  onemoguceno?: boolean
  tip?: 'button' | 'submit' | 'reset'
}>()
</script>
 
<template>
  <button
    :type="tip ?? 'button'"
    :disabled="onemoguceno || ucitava"
    :class="['gumb', `gumb--${vrsta ?? 'primarni'}`, `gumb--${velicina ?? 'normalni'}`]"
  >
    <span v-if="ucitava" class="spinner-mali"></span>
    <slot>{{ ucitava ? 'Učitavanje...' : '' }}</slot>
  </button>
</template>
 
<style scoped>
.gumb {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-display);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  cursor: pointer;
  border: none;
  transition: background var(--tranzicija), color var(--tranzicija);
}
.gumb:disabled { opacity: 0.4; cursor: not-allowed; }
.gumb--normalni { padding: 0.625rem 1.5rem; font-size: 0.9rem; }
.gumb--mali     { padding: 0.375rem 0.875rem; font-size: 0.75rem; }
.gumb--primarni { background: var(--boja-akcent); color: #0a0a0a; }
.gumb--primarni:hover:not(:disabled) { background: var(--boja-akcent-hover); }
.gumb--sekundarni { background: transparent; color: var(--boja-tekst-mute); border: 1px solid var(--boja-rub); }
.gumb--sekundarni:hover:not(:disabled) { color: var(--boja-tekst); border-color: var(--boja-tekst-mute); }
.gumb--opasnost { background: transparent; color: var(--boja-greska); border: 1px solid var(--boja-greska); }
.gumb--opasnost:hover:not(:disabled) { background: var(--boja-greska); color: white; }
 
.spinner-mali {
  width: 14px; height: 14px;
  border: 2px solid rgba(0,0,0,0.3);
  border-top-color: #0a0a0a;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
</style>
