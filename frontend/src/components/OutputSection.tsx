import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import { FileText, Mail, Users, Lightbulb, Copy, Check, Download } from 'lucide-react'
import type { GeneratedAssets } from '../types'
import { pdfService } from '../services/pdf'

interface OutputSectionProps {
  assets: GeneratedAssets
}

type Tab = 'cv' | 'coverLetter' | 'networking' | 'insights'

export function OutputSection({ assets }: OutputSectionProps) {
  const [activeTab, setActiveTab] = useState<Tab>('cv')
  const [copied, setCopied] = useState(false)

  const tabs: { id: Tab; label: string; icon: React.ElementType }[] = [
    { id: 'cv', label: 'Currículo', icon: FileText },
    { id: 'coverLetter', label: 'Carta', icon: Mail },
    { id: 'networking', label: 'Networking', icon: Users },
    { id: 'insights', label: 'Dicas', icon: Lightbulb },
  ]

  const getContent = () => {
    switch (activeTab) {
      case 'cv': return assets.cv
      case 'coverLetter': return assets.coverLetter
      case 'networking': return assets.networking
      case 'insights': return assets.insights
      default: return ''
    }
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(getContent())
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleDownloadPdf = () => {
    const content = getContent()
    const title = tabs.find(t => t.id === activeTab)?.label || 'Documento'
    pdfService.generatePdf(title, content)
  }

  return (
    <div className="w-full max-w-4xl mx-auto mt-12 bg-slate-900 rounded-xl border border-slate-800 overflow-hidden shadow-2xl">
      <div className="flex border-b border-slate-800 overflow-x-auto">
        {tabs.map((tab) => {
          const Icon = tab.icon
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2 px-6 py-4 text-sm font-medium transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-slate-800 text-emerald-400 border-b-2 border-emerald-400'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Icon size={18} />
              {tab.label}
            </button>
          )
        })}
        <div className="ml-auto flex items-center px-4">
          <div className="flex items-center gap-2 text-sm text-slate-400 bg-slate-950 px-3 py-1 rounded-full border border-slate-800">
            <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
            Match: {assets.matchScore}%
          </div>
        </div>
      </div>

      <div className="relative bg-slate-950 p-6 min-h-[500px] text-left">
        <div className="absolute top-4 right-4 flex gap-2">
          <button
            onClick={handleDownloadPdf}
            className="p-2 rounded-lg bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 transition-all border border-slate-700"
            title="Baixar PDF"
          >
            <Download size={18} />
          </button>
          <button
            onClick={handleCopy}
            className="p-2 rounded-lg bg-slate-800 text-slate-400 hover:text-white hover:bg-slate-700 transition-all border border-slate-700"
            title="Copiar conteúdo"
          >
            {copied ? <Check size={18} className="text-emerald-400" /> : <Copy size={18} />}
          </button>
        </div>
        
        <div className="prose prose-invert prose-slate max-w-none">
          <ReactMarkdown>{getContent()}</ReactMarkdown>
        </div>
      </div>
    </div>
  )
}
