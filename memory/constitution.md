# Vaga Certa Constitution

## Artigo I — Estrutura Minimalista
Todo desenvolvimento deve preservar a simplicidade arquitetural: apenas backend, frontend e shared types. Novos módulos exigem justificativa explícita.

## Artigo II — Test-First Obrigatório
Cada funcionalidade nasce de testes. Escreva testes que falham, valide com o Product Owner e só então implemente.

## Artigo III — Contratos Primeiro
Qualquer API pública deve ter contrato OpenAPI aprovado antes da implementação. Alterações de contrato precisam ser versionadas e documentadas.

## Artigo IV — Integração Real
Integrações externas (Google Gemini, job boards) devem ser exercitadas em testes de integração marcados e podem ser ignoradas apenas quando as credenciais não estiverem disponíveis.

## Artigo V — Observabilidade e Logs
Logs devem ser estruturados em JSON, com correlação entre requisições. Métricas de latência e health checks são obrigatórios antes de qualquer deploy.

## Artigo VI — Qualidade Contínua
Lint (ruff, ESLint), type checking (mypy, TypeScript strict) e cobertura >70% são gates para merge. Commits que quebram qualquer gate são revertidos imediatamente.

## Artigo VII — Performance e Resiliência
Backends devem responder <5s p95; frontend <3s FCP. Implementações precisam de retry/backoff configuráveis e validações multi-layer.

## Artigo VIII — CI/CD e Deploy
Toda alteração passa pelo pipeline GitHub Actions. Deploy só ocorre com pipeline verde, secrets configurados e rollback automatizado definido.

## Artigo IX — Governança
Esta constituição prevalece sobre outras práticas. Alterações exigem RFC documentada, aprovação do Product Owner e plano de migração.

**Version**: 1.0.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19
