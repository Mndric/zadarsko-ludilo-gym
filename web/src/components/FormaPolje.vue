<script setup lang="ts">
// defineModel automatski upravlja dvosmjernom vezom (v-model)
const model = defineModel<string | number>()

defineProps<{
  oznaka: string
  vrsta?: string
  greska?: string
  obavezno?: boolean
  placeholder?: string
}>()
</script>

<template>
  <div class="polje-grupa" :class="{ 'ima-gresku': greska }">
    <label class="polje-label">
      {{ oznaka }} <span v-if="obavezno" class="obavezno-zvjezdica">*</span>
    </label>
    
    <input
      :type="vrsta || 'text'"
      v-model="model"
      :placeholder="placeholder"
      class="polje-input"
    />
    
    <!-- Prikaz greške ispod polja -->
    <span v-if="greska" class="greska-tekst" data-testid="field-error">
      {{ greska }}
    </span>
  </div>
</template>

<style scoped>
.polje-grupa {
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
}
.polje-label {
  font-weight: 600;
  margin-bottom: 0.25rem;
  color: #2c3e50;
}
.obavezno-zvjezdica {
  color: #e74c3c;
}
.polje-input {
  padding: 0.6rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
  transition: border-color 0.2s;
}
.polje-input:focus {
  outline: none;
  border-color: #3498db;
}
.ima-gresku .polje-input {
  border-color: #e74c3c;
}
.greska-tekst {
  color: #e74c3c;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}
</style>