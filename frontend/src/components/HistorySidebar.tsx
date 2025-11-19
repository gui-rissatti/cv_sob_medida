import { useEffect, useState } from 'react'
import { Trash2, ExternalLink, Clock, Search, Download } from 'lucide-react'
import { useAppStore } from '../store/useAppStore'

export function HistorySidebar() {
  const { history, loadHistory, loadApplication, deleteApplication, exportHistory } = useAppStore()
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  const filteredHistory = history.filter(entry => 
    entry.jobTitle.toLowerCase().includes(searchTerm.toLowerCase()) ||
    entry.companyName.toLowerCase().includes(searchTerm.toLowerCase())
  )

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
        {filteredHistory.length === 0 ? (
          <p className="text-center text-sm text-slate-500 py-4">Nenhum item encontrado</p>
        ) : (
          filteredHistory.map((entry) => (
            <div 
              key={entry.id}
              className="group relative p-4 rounded-lg bg-slate-950 border border-slate-800 hover:border-emerald-500/50 transition-all cursor-pointer"
              onClick={() => loadApplication(entry.id)}
            >
              <h3 className="font-medium text-slate-200 truncate pr-6" title={entry.jobTitle}>
                {entry.jobTitle}
              </h3>
              <p className="text-sm text-slate-400 truncate">{entry.companyName}</p>
              <div className="mt-3 flex items-center justify-between text-xs text-slate-500">
                <span>{formatDate(entry.applicationDate)}</span>
                
                <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <a 
                    href={entry.jobUrl} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="p-1.5 hover:bg-slate-800 rounded text-slate-400 hover:text-emerald-400"
                    onClick={(e) => e.stopPropagation()}
                    title="Ver vaga original"
                  >
                    <ExternalLink size={14} />
                  </a>
                  <button
                    className="p-1.5 hover:bg-red-500/10 rounded text-slate-400 hover:text-red-400"
                    onClick={(e) => {
                      e.stopPropagation()
                      if (confirm('Tem certeza que deseja excluir este item?')) {
                        deleteApplication(entry.id)
                      }
                    }}
                    title="Excluir"
                  >
                    <Trash2 size={14} />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </aside>
  )
}
