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

  async generateMaterials(
    job: Job, 
    cvText: string,
    options: { language: string; tone: string; variance: number } = { language: 'auto', tone: 'professional', variance: 3 }
  ): Promise<GeneratedAssets> {
    const response = await api.post<GeneratedAssets>('/generate-materials', {
      job,
      profile: {
        cvText,
        language: options.language,
        tone: options.tone,
        variance: options.variance,
      },
    })
    return response.data
  },

  async extractCvText(file: File): Promise<string> {
    const formData = new FormData()
    formData.append('file', file)

    const response = await axios.post<{ text: string }>(`${API_URL}/extract-cv-text`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data.text
  },
}
