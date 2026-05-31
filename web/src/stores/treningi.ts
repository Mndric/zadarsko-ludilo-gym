import { defineStore } from 'pinia'
import { TreningService } from '@/services/treningi'
import type { Trening } from '@/types/trening'

export const useTreningStore = defineStore('treningi', {
  state: () => ({
    items: [] as Trening[],
    stanje: 'prazno' as 'ucitavanje' | 'greska' | 'prazno' | 'spremno',
    porukaGreske: '' as string
  }),

  actions: {
    async fetchTrainings(): Promise<void> {
      this.stanje = 'ucitavanje'
      this.porukaGreske = ''
      
      try {
        const podaci = await TreningService.getAll()
        this.items = podaci
        
        if (podaci.length === 0) {
          this.stanje = 'prazno'
        } else {
          this.stanje = 'spremno'
        }
      } catch (err: any) {
        this.stanje = 'greska'
        this.porukaGreske = err.response?.data?.detail || 'Neuspješno povezivanje sa serverom.'
      }
    },

    async dodajTrening(noviTrening: Omit<Trening, 'id'>): Promise<void> {
      try {
        const kreirano = await TreningService.create(noviTrening)
        this.items.push(kreirano)
        this.stanje = 'spremno'
      } catch (err: any) {
        throw err.response?.data?.detail || 'Greška pri spremanju treninga.'
      }
    },

    async obrisiTrening(id: number): Promise<void> {
      try {
        await TreningService.delete(id)
        this.items = this.items.filter(t => t.id !== id)
        if (this.items.length === 0) this.stanje = 'prazno'
      } catch (err: any) {
        alert('Nije moguće obrisati trening. Možda postoje aktivne rezervacije.')
      }
    }
  }
})