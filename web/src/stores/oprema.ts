import { defineStore } from 'pinia'
import { ref } from 'vue'
import { dohvatiOpremu, kreirajOpremu } from '@/services/gym'
import type { Oprema, OpremaCreate } from '@/types/oprema'
 
export const useOpremaStore = defineStore('oprema', () => {
  const stavke = ref<Oprema[]>([])
  const ucitava = ref(false)
  const greska = ref('')
 
  async function ucitaj(): Promise<void> {
    ucitava.value = true
    greska.value = ''
    try {
      stavke.value = await dohvatiOpremu()
    } catch (e) {
      greska.value = e instanceof Error ? e.message : 'Greška pri dohvatu opreme.'
    } finally {
      ucitava.value = false
    }
  }
 
  async function dodaj(tijelo: OpremaCreate): Promise<void> {
    const nova = await kreirajOpremu(tijelo)
    stavke.value.push(nova)
  }
 
  return { stavke, ucitava, greska, ucitaj, dodaj }
})
