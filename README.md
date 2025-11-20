# CV Sob Medida

Pipeline completo para extrair vagas via URL, gerar materiais personalizados com Google Gemini e entregar UI responsiva com histórico local.

---

## 🚀 Início Rápido (Windows)

**2 cliques para testar:**

1. **Duplo clique:** `teste_rapido.bat` (setup + testes)
2. **Duplo clique:** `start_app.bat` (usa a aplicação)

**Mais informações:** [QUICKSTART_WINDOWS.md](QUICKSTART_WINDOWS.md) | [Índice Completo de Docs](DOCS_INDEX.md)

---

## Funcionalidades

- **Extração de Vagas**: Suporte a LinkedIn, Indeed, Glassdoor, etc.
- **Geração de Materiais**: Currículo, Carta de Apresentação, Dicas de Networking e Insights.
- **Histórico Local**: Salva suas aplicações no navegador (IndexedDB).
- **Exportação**: Baixe em PDF ou JSON.

## Requisitos

- Python 3.11+
- Node.js 20+
- Google Gemini API Key

## Configuração Rápida

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

pip install -r requirements.txt
cp .env.example .env
# Edite .env com sua GOOGLE_API_KEY

# IMPORTANTE: Configure PYTHONPATH antes de iniciar
$env:PYTHONPATH="$PWD\src"  # Windows PowerShell
# export PYTHONPATH="$PWD/src"  # Linux/macOS

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Nota:** A aplicação agora usa `gemini-2.5-flash` (modelo atualizado para 2025).

### Frontend

```bash
cd frontend
npm install

# Crie arquivo .env com a URL do backend
echo "VITE_API_URL=http://localhost:8000" > .env

npm run dev
```

Acesse: http://localhost:5173

## Deploy

Consulte [DEPLOY.md](DEPLOY.md) para instruções de deploy em produção.

## Estrutura do Projeto

- `backend/`: API FastAPI, Agentes LangChain.
- `frontend/`: React, Vite, Tailwind, Zustand, IndexedDB.
- `shared/`: Tipos compartilhados.
- `specs/`: Documentação de design e tarefas.

## 📚 Documentação

### Para Começar
- **[QUICKSTART_WINDOWS.md](QUICKSTART_WINDOWS.md)** - Guia rápido para Windows (testes offline)
- **[SCRIPTS_README.md](SCRIPTS_README.md)** - Documentação dos scripts batch automatizados

### Para Desenvolvedores
- **[DEBUGGING_REPORT.md](DEBUGGING_REPORT.md)** - Relatório técnico completo de debugging
- **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** - Resumo executivo das correções
- **[CHECKLIST_TESTES.md](CHECKLIST_TESTES.md)** - Checklist de validação

### Scripts Batch (Windows)
- `teste_rapido.bat` - Setup completo + testes automatizados
- `start_app.bat` - Inicia backend + frontend + navegador
- `start_backend.bat` - Inicia apenas o backend
- `start_frontend.bat` - Inicia apenas o frontend

## Licença

MIT

## Troubleshooting

### Erro: "Module 'api' not found"
**Solução:** Configure `PYTHONPATH` antes de iniciar o backend:
```bash
# Windows PowerShell
$env:PYTHONPATH="$PWD\src"
uvicorn app.main:app --reload

# Linux/macOS
export PYTHONPATH="$PWD/src"
uvicorn app.main:app --reload
```

### Erro: "google_api_key not found"
**Solução:** Verifique se o arquivo `.env` existe em `backend/` e contém:
```
GOOGLE_API_KEY=sua_chave_aqui
```

### Erro: "404 models/gemini-1.5-flash not found"
**Solução:** O código já foi atualizado para `gemini-2.5-flash`. Se ainda ocorrer, atualize os arquivos:
- `backend/src/agents/extraction_agent.py`
- `backend/src/agents/generation_agent.py`

### Frontend não conecta ao backend
**Solução:** Crie `frontend/.env` com:
```
VITE_API_URL=http://localhost:8000
```

## Testes

Para validar que tudo está funcionando:

```bash
cd backend
python test_e2e_complete.py
```

Deve mostrar: `🎉 TODOS OS TESTES PASSARAM!`

---

**Para relatório completo de debugging:** Consulte [DEBUGGING_REPORT.md](DEBUGGING_REPORT.md)
cd backend
ruff check .
mypy .
pytest -m "not integration" --cov=. --cov-report=term

# Testes de integração (requer GOOGLE_API_KEY válido)
pytest -m integration

# Frontend
cd frontend
npm run lint
npm run type-check
npm run test:coverage
```

## CI/CD e Secrets
Workflow principal em `.github/workflows/ci.yml` valida backend e frontend (lint, tipos, testes, cobertura). Configure em **Settings → Secrets and variables → Actions**:
- `GOOGLE_API_KEY`
- `LANGCHAIN_API_KEY` (opcional)
- `VERCEL_TOKEN`, `RENDER_API_KEY` para os jobs de deploy (em breve)

Com todos os checks verdes e health checks respondendo `200 OK`, o deploy automatizado pode ser acionado.
