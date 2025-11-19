import axios from 'axios'
import type { Job, GeneratedAssets } from '../types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  async extractJobDetails(url: string): Promise<Job> {
    const response = await api.post<Job>('/extract-job-details', { url })
    return response.data
  },

  async generateMaterials(job: Job, cvText: string): Promise<GeneratedAssets> {
    const response = await api.post<GeneratedAssets>('/generate-materials', {
      job,
      profile: {
        cvText,
      },
    })
    return response.data
  },
}
