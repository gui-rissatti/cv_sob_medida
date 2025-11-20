import { describe, expect, it } from 'vitest'
import type { ApplicationHistoryEntry } from '../types'
import { filterHistoryEntries, groupHistoryByCompany } from './historyGrouping'

const mockHistory: ApplicationHistoryEntry[] = [
  {
    id: '1',
    jobTitle: 'Data Engineer',
    companyName: 'Mercado Livre',
    applicationDate: '2025-01-02T10:00:00.000Z',
    jobUrl: 'https://jobs.meli.com/data-engineer',
    generatedAssetsId: 'assets-1',
  },
  {
    id: '2',
    jobTitle: 'Data Engineer',
    companyName: 'Mercado Livre',
    applicationDate: '2025-01-03T12:00:00.000Z',
    jobUrl: 'https://jobs.meli.com/data-engineer',
    generatedAssetsId: 'assets-2',
  },
  {
    id: '3',
    jobTitle: 'Analytics Lead',
    companyName: 'Mercado Livre',
    applicationDate: '2025-02-01T08:00:00.000Z',
    jobUrl: 'https://jobs.meli.com/analytics-lead',
    generatedAssetsId: 'assets-3',
  },
  {
    id: '4',
    jobTitle: 'Backend Engineer',
    companyName: 'Another Corp',
    applicationDate: '2024-12-01T10:00:00.000Z',
    jobUrl: 'https://jobs.another.com/backend-engineer',
    generatedAssetsId: 'assets-4',
  },
  {
    id: '5',
    jobTitle: 'Product Manager',
    companyName: '',
    applicationDate: '2025-03-01T10:00:00.000Z',
    jobUrl: 'https://jobs.unknown.com/product-manager',
    generatedAssetsId: 'assets-5',
  },
]

describe('filterHistoryEntries', () => {
  it('filters history by job title or company case-insensitively', () => {
    const filtered = filterHistoryEntries(mockHistory, 'mercado')
    expect(filtered).toHaveLength(3)
    expect(filtered.every((entry) => entry.companyName === 'Mercado Livre')).toBe(true)

    const filteredByTitle = filterHistoryEntries(mockHistory, 'backend')
    expect(filteredByTitle).toHaveLength(1)
    expect(filteredByTitle[0].jobTitle).toBe('Backend Engineer')
  })

  it('returns original history when search term is empty', () => {
    const filtered = filterHistoryEntries(mockHistory, '')
    expect(filtered).toEqual(mockHistory)
  })
})

describe('groupHistoryByCompany', () => {
  it('groups entries by company, counting total applications and sorting by recency', () => {
    const grouped = groupHistoryByCompany(mockHistory)

    expect(grouped).toHaveLength(3)
    expect(grouped[0].company).toBe('Outros')
    expect(grouped[0].applicationCount).toBe(1)

    const mercadoGroup = grouped.find((group) => group.company === 'Mercado Livre')
    expect(mercadoGroup).toBeDefined()
    expect(mercadoGroup?.entries).toHaveLength(3)
    expect(mercadoGroup?.applicationCount).toBe(3)
    expect(mercadoGroup?.entries[0].applicationDate).toBe('2025-02-01T08:00:00.000Z')

    const anotherGroup = grouped.find((group) => group.company === 'Another Corp')
    expect(anotherGroup?.applicationCount).toBe(1)
  })

  it('falls back to "Outros" when company name is empty', () => {
    const grouped = groupHistoryByCompany(mockHistory)
    const outrosGroup = grouped.find((group) => group.company === 'Outros')
    expect(outrosGroup).toBeDefined()
    expect(outrosGroup?.entries[0].jobTitle).toBe('Product Manager')
  })
})
