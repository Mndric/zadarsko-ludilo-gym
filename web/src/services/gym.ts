import { api } from './api'
import type { Oprema, OpremaCreate } from '@/types/oprema'
import type { Rezervacija, RezervacijaCreate } from '@/types/rezervacija'
import type { Clanarina } from '@/types/clanarina'
 
// Oprema
export async function dohvatiOpremu(): Promise<Oprema[]> {
  const { data } = await api.get<Oprema[]>('/gym/equipment')
  return data
}
 
export async function kreirajOpremu(tijelo: OpremaCreate): Promise<Oprema> {
  const { data } = await api.post<Oprema>('/gym/equipment', tijelo)
  return data
}
 
// Rezervacije
export async function kreirajRezervaciju(tijelo: RezervacijaCreate): Promise<Rezervacija> {
  const { data } = await api.post<Rezervacija>('/gym/reserve', tijelo)
  return data
}
 
export async function dohvatiMojeRezervacije(): Promise<Rezervacija[]> {
  const { data } = await api.get<Rezervacija[]>('/gym/my-reservations')
  return data
}
 
export async function obrisiRezervaciju(id: number): Promise<void> {
  await api.delete(`/gym/reservations/${id}`)
}
 
// Clanarina
export async function aktivirajClanarinu(): Promise<Clanarina> {
  const { data } = await api.post<Clanarina>('/gym/membership/activate')
  return data
}
