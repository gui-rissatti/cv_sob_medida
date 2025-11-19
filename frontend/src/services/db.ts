import { openDB, type DBSchema } from 'idb'
import type { Job, GeneratedAssets, ApplicationHistoryEntry } from '../types'

export interface FullApplication {
  id: string
  job: Job
  assets: GeneratedAssets
  createdAt: string
}

interface CVDBSchema extends DBSchema {
  applications: {
    key: string
    value: FullApplication
    indexes: { 'by-date': string }
  }
}

const DB_NAME = 'cv-sob-medida-db'
const DB_VERSION = 1

export const dbService = {
  async getDb() {
    return openDB<CVDBSchema>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        const store = db.createObjectStore('applications', {
          keyPath: 'id',
        })
        store.createIndex('by-date', 'createdAt')
      },
    })
  },

  async saveApplication(job: Job, assets: GeneratedAssets): Promise<string> {
    const db = await this.getDb()
    const id = crypto.randomUUID()
    const application: FullApplication = {
      id,
      job,
      assets,
      createdAt: new Date().toISOString(),
    }
    await db.put('applications', application)
    return id
  },

  async getAllApplications(): Promise<ApplicationHistoryEntry[]> {
    const db = await this.getDb()
    const applications = await db.getAllFromIndex('applications', 'by-date')
    return applications.reverse().map((app) => ({
      id: app.id,
      jobTitle: app.job.title,
      companyName: app.job.company,
      applicationDate: app.createdAt,
      jobUrl: app.job.url,
      generatedAssetsId: app.assets.jobId,
    }))
  },

  async getAllFullApplications(): Promise<FullApplication[]> {
    const db = await this.getDb()
    return db.getAll('applications')
  },

  async getApplication(id: string): Promise<FullApplication | undefined> {
    const db = await this.getDb()
    return db.get('applications', id)
  },
  
  async deleteApplication(id: string): Promise<void> {
    const db = await this.getDb()
    await db.delete('applications', id)
  }
}
