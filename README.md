# CV Sob Medida

Pipeline completo para extrair vagas via URL, gerar materiais personalizados com Google Gemini e entregar UI responsiva com histórico local.

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

uvicorn src.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Deploy

Consulte [DEPLOY.md](DEPLOY.md) para instruções de deploy em produção.

## Estrutura do Projeto

- `backend/`: API FastAPI, Agentes LangChain.
- `frontend/`: React, Vite, Tailwind, Zustand, IndexedDB.
- `shared/`: Tipos compartilhados.
- `specs/`: Documentação de design e tarefas.

## Licença

MIT
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
