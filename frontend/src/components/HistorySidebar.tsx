import { useEffect, useState, useMemo } from 'react'
import { Trash2, ExternalLink, Clock, Search, Download, Building2, ChevronDown, ChevronRight } from 'lucide-react'
import { useAppStore } from '../store/useAppStore'
import { filterHistoryEntries, groupHistoryByCompany } from '../utils/historyGrouping'

export function HistorySidebar() {
  const { history, loadHistory, loadApplication, deleteApplication, exportHistory } = useAppStore()
  const [searchTerm, setSearchTerm] = useState('')
  const [expandedGroups, setExpandedGroups] = useState<Record<string, boolean>>({})

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  const filteredHistory = useMemo(() => filterHistoryEntries(history, searchTerm), [history, searchTerm])

  const groupedHistory = useMemo(() => groupHistoryByCompany(filteredHistory), [filteredHistory])

  // Initialize expanded state for new groups
  useEffect(() => {
    if (groupedHistory.length > 0) {
      setExpandedGroups(prev => {
        const next = { ...prev }
        groupedHistory.forEach(({ company }) => {
          if (next[company] === undefined) {
            // Expand by default if searching, or if it's the first group
            next[company] = searchTerm !== '' || Object.keys(prev).length === 0
          }
        })
        return next
      })
    }
  }, [groupedHistory, searchTerm])

  const toggleGroup = (company: string) => {
    setExpandedGroups(prev => ({ ...prev, [company]: !prev[company] }))
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  if (history.length === 0) {
    return null
  }

  return (
    <aside className="hidden lg:flex flex-col w-80 h-screen fixed left-0 top-0 bg-slate-900 border-r border-slate-800 overflow-y-auto z-10">
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-white flex items-center gap-2">
            <Clock size={20} className="text-emerald-400" />
            Histórico
          </h2>
          <button 
            onClick={exportHistory}
            className="p-2 text-slate-400 hover:text-emerald-400 hover:bg-slate-800 rounded-lg transition-colors"
            title="Exportar histórico (JSON)"
          >
            <Download size={18} />
          </button>
        </div>
        
        <div className="relative">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Buscar..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg py-2 pl-9 pr-3 text-sm text-slate-300 focus:outline-none focus:border-emerald-500/50 transition-colors"
          />
        </div>
      </div>
      
      <div className="flex-1 p-4 space-y-3">
        {groupedHistory.length === 0 ? (
          <p className="text-center text-sm text-slate-500 py-4">Nenhum item encontrado</p>
        ) : (
          groupedHistory.map(({ company, entries, applicationCount }) => (
            <div key={company} className="rounded-lg border border-slate-800 bg-slate-900/50 overflow-hidden">
              <button
                onClick={() => toggleGroup(company)}
                className="w-full flex items-center justify-between p-3 hover:bg-slate-800 transition-colors"
              >
                <div className="flex items-center gap-2 overflow-hidden">
                  <Building2 size={16} className="text-emerald-500 shrink-0" />
                  <span className="font-medium text-slate-200 truncate text-sm" title={company}>
                    {company}
                  </span>
                  <span className="text-xs text-slate-500 shrink-0">
                    ({applicationCount})
                  </span>
                </div>
                {expandedGroups[company] ? (
                  <ChevronDown size={16} className="text-slate-500 shrink-0" />
                ) : (
                  <ChevronRight size={16} className="text-slate-500 shrink-0" />
                )}
              </button>

              {expandedGroups[company] && (
                <div className="border-t border-slate-800 bg-slate-950/30">
                  {entries.map((entry) => (
                    <div 
                      key={entry.id}
                      className="group relative p-3 border-b border-slate-800/50 last:border-0 hover:bg-slate-800/50 transition-all cursor-pointer"
                      onClick={() => loadApplication(entry.id)}
                    >
                      <h3 className="font-medium text-slate-300 truncate pr-6 text-sm" title={entry.jobTitle}>
                        {entry.jobTitle}
                      </h3>
                      <div className="mt-2 flex items-center justify-between text-xs text-slate-500">
                        <span>{formatDate(entry.applicationDate)}</span>
                        
                        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                          <a 
                            href={entry.jobUrl} 
                            target="_blank" 
                            rel="noopener noreferrer"
                            className="p-1 hover:bg-slate-700 rounded text-slate-400 hover:text-emerald-400"
                            onClick={(e) => e.stopPropagation()}
                            title="Ver vaga original"
                          >
                            <ExternalLink size={12} />
                          </a>
                          <button
                            className="p-1 hover:bg-red-500/10 rounded text-slate-400 hover:text-red-400"
                            onClick={(e) => {
                              e.stopPropagation()
                              if (confirm('Tem certeza que deseja excluir este item?')) {
                                deleteApplication(entry.id)
                              }
                            }}
                            title="Excluir"
                          >
                            <Trash2 size={12} />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </aside>
  )
}
