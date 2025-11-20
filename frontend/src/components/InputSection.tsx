import { useState, useRef } from 'react'
import { Link, ArrowRight, Loader2, FileText, ChevronDown, ChevronUp, Upload, CheckCircle2, Globe, MessageSquare, Sliders, HelpCircle } from 'lucide-react'
import { apiService } from '../services/api'

interface InputSectionProps {
  onSubmit: (url: string) => void
  cvText: string
  onCvChange: (text: string) => void
  language: string
  onLanguageChange: (language: string) => void
  tone: string
  onToneChange: (tone: string) => void
  variance: number
  onVarianceChange: (variance: number) => void
  isLoading?: boolean
  error?: string | null
}

export function InputSection({ 
  onSubmit, 
  cvText, 
  onCvChange, 
  language,
  onLanguageChange,
  tone,
  onToneChange,
  variance,
  onVarianceChange,
  isLoading = false, 
  error = null 
}: InputSectionProps) {
  const [url, setUrl] = useState('')
  const [showCv, setShowCv] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [isUploading, setIsUploading] = useState(false)
  const [showVarianceHelp, setShowVarianceHelp] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (url.trim()) {
      onSubmit(url)
    }
  }

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setIsUploading(true)
    try {
      const text = await apiService.extractCvText(file)
      onCvChange(text)
      setShowCv(true)
    } catch (err) {
      console.error('Failed to upload CV:', err)
      alert('Erro ao processar arquivo. Tente copiar e colar o texto.')
    } finally {
      setIsUploading(false)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
    }
  }

  const hasCv = cvText.trim().length > 0

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="mb-6">
        <button 
          onClick={() => setShowCv(!showCv)}
          className={`flex items-center gap-2 text-sm transition-colors mx-auto mb-2 ${
            hasCv ? 'text-emerald-400 hover:text-emerald-300' : 'text-slate-400 hover:text-emerald-400'
          }`}
        >
          {hasCv ? <CheckCircle2 size={16} /> : <FileText size={16} />}
          {showCv ? 'Ocultar Currículo Base' : 'Configurar Currículo Base'}
          {showCv ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>
        
        {showCv && (
          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 mb-4 animate-in fade-in slide-in-from-top-2">
            <div className="flex justify-between items-center mb-2">
              <label className="block text-sm font-medium text-slate-300 text-left">
                Cole o texto ou faça upload (PDF/DOCX/TXT):
              </label>
              <div className="relative">
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept=".pdf,.docx,.txt"
                  className="hidden"
                />
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isUploading}
                  className="flex items-center gap-2 text-xs bg-slate-800 hover:bg-slate-700 text-emerald-400 px-3 py-1.5 rounded-lg transition-colors disabled:opacity-50"
                >
                  {isUploading ? <Loader2 size={12} className="animate-spin" /> : <Upload size={12} />}
                  {isUploading ? 'Processando...' : 'Upload Arquivo'}
                </button>
              </div>
            </div>
            <textarea
              value={cvText}
              onChange={(e) => onCvChange(e.target.value)}
              placeholder="Resumo profissional, experiências, habilidades..."
              className="w-full h-48 p-3 rounded-lg bg-slate-950 border border-slate-700 text-slate-300 text-sm focus:outline-none focus:border-emerald-500 transition-colors resize-none"
            />
          </div>
        )}
      </div>

      {/* Advanced Settings */}
      <div className="mb-6">
        <button 
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center gap-2 text-sm text-slate-400 hover:text-emerald-400 transition-colors mx-auto mb-2"
        >
          <Sliders size={16} />
          {showAdvanced ? 'Ocultar Configurações Avançadas' : 'Configurações Avançadas'}
          {showAdvanced ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </button>
        
        {showAdvanced && (
          <div className="bg-slate-900 p-4 rounded-xl border border-slate-800 space-y-4 animate-in fade-in slide-in-from-top-2">
            
            {/* Language Selector */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-2">
                <Globe size={16} />
                Idioma do Output
              </label>
              <select 
                value={language}
                onChange={(e) => onLanguageChange(e.target.value)}
                className="w-full p-2 rounded-lg bg-slate-950 border border-slate-700 text-slate-300 text-sm focus:outline-none focus:border-emerald-500 transition-colors"
              >
                <option value="auto">Auto (detectar da vaga)</option>
                <option value="pt">Português</option>
                <option value="en">English</option>
                <option value="es">Español</option>
                <option value="fr">Français</option>
                <option value="de">Deutsch</option>
              </select>
            </div>

            {/* Tone Selector */}
            <div>
              <label className="flex items-center gap-2 text-sm font-medium text-slate-300 mb-2">
                <MessageSquare size={16} />
                Tom de Voz
              </label>
              <select 
                value={tone}
                onChange={(e) => onToneChange(e.target.value)}
                className="w-full p-2 rounded-lg bg-slate-950 border border-slate-700 text-slate-300 text-sm focus:outline-none focus:border-emerald-500 transition-colors"
              >
                <option value="professional">Professional</option>
                <option value="friendly">Friendly</option>
                <option value="formal">Formal</option>
                <option value="enthusiastic">Enthusiastic</option>
              </select>
            </div>

            {/* Variance Slider */}
            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="flex items-center gap-2 text-sm font-medium text-slate-300">
                  <Sliders size={16} />
                  Variância de Adaptação: {variance}
                </label>
                <button
                  type="button"
                  onMouseEnter={() => setShowVarianceHelp(true)}
                  onMouseLeave={() => setShowVarianceHelp(false)}
                  className="text-slate-400 hover:text-emerald-400 transition-colors relative"
                >
                  <HelpCircle size={16} />
                  {showVarianceHelp && (
                    <div className="absolute right-0 top-6 w-72 p-3 bg-slate-800 border border-slate-700 rounded-lg text-xs text-slate-300 z-10 shadow-xl">
                      <p className="font-semibold mb-1">Controla a flexibilidade de adaptação:</p>
                      <ul className="space-y-1 list-disc list-inside">
                        <li><strong>1-2:</strong> Fiel ao seu CV, apenas reorganiza</li>
                        <li><strong>3:</strong> Equilíbrio, adaptações sutis de stacks</li>
                        <li><strong>4-5:</strong> Maior liberdade, infere competências relacionadas</li>
                      </ul>
                    </div>
                  )}
                </button>
              </div>
              <input 
                type="range"
                min="1"
                max="5"
                step="1"
                value={variance}
                onChange={(e) => onVarianceChange(Number(e.target.value))}
                className="w-full h-2 bg-slate-700 rounded-lg appearance-none cursor-pointer slider"
                style={{
                  background: `linear-gradient(to right, #10b981 0%, #10b981 ${(variance - 1) * 25}%, #334155 ${(variance - 1) * 25}%, #334155 100%)`
                }}
              />
              <div className="flex justify-between text-xs text-slate-500 mt-1">
                <span>Estrito</span>
                <span>Equilibrado</span>
                <span>Criativo</span>
              </div>
            </div>
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
