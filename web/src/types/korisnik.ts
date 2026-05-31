export interface Korisnik {
  id: number;
  username: string;
  email?: string;
  role: 'admin' | 'user'; // Tvoj backend koristi 'admin' i 'user'
}