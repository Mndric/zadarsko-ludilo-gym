import apiClient from '@/api/client'
import type { Trening } from '@/types/trening'

export const TreningService = {
  // GET /trainings
  async getAll(): Promise<Trening[]> {
    const response = await apiClient.get<Trening[]>('/trainings')
    return response.data
  },

  // POST /trainings
  async create(data: Omit<Trening, 'id'>): Promise<Trening> {
    const response = await apiClient.post<Trening>('/trainings', data)
    return response.data
  },

  // DELETE /trainings/{id}
  async delete(id: number): Promise<void> {
    await apiClient.delete(`/trainings/${id}`)
  }
}