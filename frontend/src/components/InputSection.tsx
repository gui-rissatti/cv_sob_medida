import { useState } from 'react'
import { Link, ArrowRight, Loader2, FileText, ChevronDown, ChevronUp } from 'lucide-react'

interface InputSectionProps {
  onSubmit: (url: string) => void
  cvText: string
  onCvChange: (text: string) => void
  isLoading?: boolean
  error?: string | null
}

export function InputSection({ onSubmit, cvText, onCvChange, isLoading = false, error = null }: InputSectionProps) {
  const [url, setUrl] = useState('')
  const [showCv, setShowCv] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (url.trim()) {
      onSubmit(url)
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="mb-6">
        <button 
          onClick={() => setShowCv(!showCv)}
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-emerald-400 transition-colors mx-auto mb-2"
        >
          <FileText size={16} />
          {showCv ? 'Ocultar Currículo Base' : 'Configurar Currículo Base'}
          {showCv ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>
        
        {showCv && (
          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 mb-4 animate-in fade-in slide-in-from-top-2">
            <label className="block text-sm font-medium text-slate-300 mb-2 text-left">
              Cole o texto do seu currículo aqui:
            </label>
            <textarea
              value={cvText}
              onChange={(e) => onCvChange(e.target.value)}
              placeholder="Resumo profissional, experiências, habilidades..."
              className="w-full h-48 p-3 rounded-lg bg-slate-950 border border-slate-700 text-slate-300 text-sm focus:outline-none focus:border-emerald-500 transition-colors resize-none"
            />
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="relative flex items-center">
        <div className="absolute left-4 text-slate-400">
          <Link size={20} />
        </div>
        <input
          type="url"
          placeholder="Cole a URL da vaga aqui (LinkedIn, Indeed, Glassdoor...)"
          className="w-full h-14 pl-12 pr-32 rounded-full bg-slate-900 border border-slate-700 text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={isLoading}
          required
        />
        <button
          type="submit"
          disabled={isLoading || !url.trim()}
          className="absolute right-2 h-10 px-6 rounded-full bg-emerald-500 hover:bg-emerald-400 text-slate-900 font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              <span>Analisando</span>
            </>
          ) : (
            <>
              <span>Gerar</span>
              <ArrowRight size={18} />
            </>
          )}
        </button>
      </form>
      
      {error && (
        <div className="mt-4 p-4 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm text-left">
          <p className="font-semibold">Erro ao processar URL</p>
          <p>{error}</p>
        </div>
      )}
      
      <div className="mt-6 flex flex-wrap justify-center gap-2 text-xs text-slate-500">
        <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-800">LinkedIn</span>
        <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-800">Indeed</span>
        <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-800">Glassdoor</span>
        <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-800">Gupy</span>
        <span className="px-3 py-1 rounded-full bg-slate-900 border border-slate-800">Vagas.com</span>
      </div>
    </div>
  )
}
