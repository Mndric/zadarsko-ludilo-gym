<template>
  <div class="nepoznato">
    <div class="broj">404</div>
    <h1>Stranica nije pronađena</h1>
    <p class="muted">Tražena stranica ne postoji ili je premještena.</p>
    <RouterLink to="/" class="veza">← Povratak na početnu</RouterLink>
  </div>
</template>
 
<style scoped>
.nepoznato { text-align: center; display: flex; flex-direction: column; gap: 1rem; align-items: center; }
.broj { font-family: var(--font-display); font-size: 8rem; font-weight: 900; color: var(--boja-akcent); line-height: 1; }
h1 { font-size: 1.5rem; }
.veza { margin-top: 1rem; color: var(--boja-tekst-mute); font-size: 0.875rem; border-bottom: 1px solid var(--boja-rub); padding-bottom: 0.2rem; }
.veza:hover { color: var(--boja-akcent); border-color: var(--boja-akcent); }
</style>
