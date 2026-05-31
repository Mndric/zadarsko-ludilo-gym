export interface Rezervacija {
  id: number
  user_id: number
  equipment_id: number
  reservation_date: string
}
 
export interface RezervacijaCreate {
  equipment_id: number
  reservation_date: string
}
