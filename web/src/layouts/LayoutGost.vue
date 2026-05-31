<template>
  <div class="layout-gost">
    <slot />
  </div>
</template>
 
<style scoped>
.layout-gost {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background: var(--boja-pozadina);
  /* Suptilni grid pattern */
  background-image: linear-gradient(
    rgba(255, 214, 0, 0.03) 1px, transparent 1px
  ), linear-gradient(
    90deg, rgba(255, 214, 0, 0.03) 1px, transparent 1px
  );
  background-size: 40px 40px;
}
</style>
