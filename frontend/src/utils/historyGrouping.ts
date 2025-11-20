import type { ApplicationHistoryEntry } from '../types'

export interface CompanyHistoryGroup {
  company: string
  entries: ApplicationHistoryEntry[]
  applicationCount: number
  latestApplicationDate: string
}

const normalizeCompanyName = (name?: string) => name?.trim() || 'Outros'

export const filterHistoryEntries = (history: ApplicationHistoryEntry[], term: string) => {
  if (!term.trim()) {
    return history
  }

  const normalizedTerm = term.toLowerCase()
  return history.filter((entry) => {
    const jobTitle = entry.jobTitle.toLowerCase()
    const companyName = entry.companyName.toLowerCase()
    return jobTitle.includes(normalizedTerm) || companyName.includes(normalizedTerm)
  })
}

export const groupHistoryByCompany = (entries: ApplicationHistoryEntry[]): CompanyHistoryGroup[] => {
  const companyMap = new Map<string, ApplicationHistoryEntry[]>()

  entries.forEach((entry) => {
    const company = normalizeCompanyName(entry.companyName)
    const companyEntries = companyMap.get(company) ?? []
    companyEntries.push(entry)
    companyMap.set(company, companyEntries)
  })

  const companyGroups: CompanyHistoryGroup[] = Array.from(companyMap.entries()).map(([company, companyEntries]) => {
    const sortedEntries = [...companyEntries].sort((a, b) => {
      return new Date(b.applicationDate).getTime() - new Date(a.applicationDate).getTime()
    })

    return {
      company,
      entries: sortedEntries,
      applicationCount: sortedEntries.length,
      latestApplicationDate: sortedEntries[0]?.applicationDate ?? new Date(0).toISOString(),
    }
  })

  return companyGroups.sort((a, b) => {
    return new Date(b.latestApplicationDate).getTime() - new Date(a.latestApplicationDate).getTime()
  })
}
