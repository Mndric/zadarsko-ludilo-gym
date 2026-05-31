import { defineStore } from 'pinia'
import { ref } from 'vue'
 
export type VrstaObavijesti = 'uspjeh' | 'greska' | 'info'
 
export interface Obavijest {
  id: number
  poruka: string
  vrsta: VrstaObavijesti
}
 
let sljedeci = 0
 
export const useObavijestiStore = defineStore('obavijesti', () => {
  const stavke = ref<Obavijest[]>([])
 
  function dodaj(poruka: string, vrsta: VrstaObavijesti = 'info'): void {
    const id = ++sljedeci
    stavke.value.push({ id, poruka, vrsta })
    setTimeout(() => ukloni(id), 4000)
  }
 
  function ukloni(id: number): void {
    stavke.value = stavke.value.filter((o) => o.id !== id)
  }
 
  return {
    stavke, ukloni,
    dodaj,
    uspjeh: (p: string) => dodaj(p, 'uspjeh'),
    greska: (p: string) => dodaj(p, 'greska'),
    info:   (p: string) => dodaj(p, 'info'),
  }
})
