# Claude Code Prompts Guide para cv_sob_medida

> Guia robusto de prompts para melhorias, refatorações e revisões usando Claude Code
> Baseado em melhores práticas do repositório [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

---

## 📋 Índice

1. [Princípios Fundamentais](#princípios-fundamentais)
2. [Prompts Generalistas](#prompts-generalistas)
3. [Orquestração de Agentes](#orquestração-de-agentes)
4. [Workflows Especializados](#workflows-especializados)
5. [Troubleshooting](#troubleshooting)

---

## 🎯 Princípios Fundamentais

### 1. **Clareza de Contexto**
- Sempre defina o objetivo claramente
- Forneça contexto sobre a arquitetura do projeto
- Especifique as restrições técnicas

### 2. **Separação de Responsabilidades**
- Use prompts especializados para diferentes partes do stack
- Isole problemas por camada (frontend, backend, infraestrutura)
- Orquestre tarefas complexas em múltiplas etapas

### 3. **Iteração Controlada**
- Valide alterações antes de commitar
- Use hooks para garantir qualidade
- Mantenha histórico de decisões

---

## 🔧 Prompts Generalistas

### 1. Análise Arquitetural

```
/analyze-architecture

Analise a arquitetura atual do projeto cv_sob_medida respondendo:

1. Mapeie todos os serviços (frontend, backend, shared, contracts)
2. Identifique dependências entre layers
3. Avalie separação de responsabilidades
4. Indique pontos de acoplamento
5. Sugeir refatorações para melhor modularização

Foco: Identificar oportunidades de improvement na estrutura atual.
Saída: Diagrama de dependências + recomendações prioritizadas.
```

### 2. Refatoração Progressiva

```
/refactor-module

Refatore o módulo [MODULO] com as seguintes etapas:

1. FASE 1 (Análise):
   - Mapeie responsabilidades atuais
   - Identifique código duplicado
   - Liste violações de padrões

2. FASE 2 (Planejamento):
   - Crie casos de teste
   - Defina estrutura alvo
   - Identifique breaking changes

3. FASE 3 (Execução):
   - Aplique alterações incrementais
   - Mantenha testes passando
   - Valide com hooks de qualidade

4. FASE 4 (Validação):
   - Verify testes passam
   - Execute linters
   - Document mudanças

Restricoes: Máximo 300 linhas por commit. Sem breaking changes sem approval.
```

### 3. Code Review Estruturado

```
/review-code

Revise o código no arquivo [ARQUIVO] sob estas dimensões:

✓ SEGURANÇA: Vulnerabilidades, injeção, auth, validação
✓ PERFORMANCE: Queries N+1, loops aninhados, memory leaks
✓ LEGIBILIDADE: Naming, complexidade, documentação
✓ TESTABILIDADE: Cobertura, mocks, isolamento de dependências
✓ MANUTENIBILIDADE: Reusabilidade, acoplamento, padrões
✓ TIPOS: Type safety (se aplicável), unions evitadas

Saída: Matriz de achados com severidade e sugestões de fix.
```

### 4. Testes Unitários

```
/generate-tests

Gere testes abrangentes para [ARQUIVO]:

1. CASOS POSITIVOS: Fluxos felizes, casos nominais
2. CASOS NEGATIVOS: Erro handling, edge cases
3. CASOS LIMITE: Boundary values, valores nulos/vazios
4. MOCKS: Isole dependências externas
5. COBERTURA: Alvo >= 80% de cobertura

Tecnologia: Detecte framework atual ([pytest/jest/unittest])
Padrão: Arrange-Act-Assert com nomes descritivos
```

### 5. Documentação Técnica

```
/document-module

Genere documentação técnica para [MODULO]:

1. README.md: Setup, uso, dependências
2. API.md: Assinaturas, parâmetros, retornos
3. ARCHITECTURE.md: Decisões de design, trade-offs
4. EXAMPLES.md: Exemplos práticos de uso
5. TROUBLESHOOTING.md: Problemas comuns e soluções

Nível: Assumir leitor tem conhecimento básico do domínio
Incluir: Diagramas ASCII quando apropriado
```

### 6. Type Safety (TypeScript/Python)

```
/add-types

Augmente [ARQUIVO] com type annotations:

1. Function signatures: todos os parâmetros e retornos
2. Variables: tipos complexos e unions
3. Generics: use quando apropriado para reusabilidade
4. Interfaces: defina contratos claros
5. Type Guards: validação em runtime quando necessário

Validar: Nenhum `any` sem justificativa em comentário
Ferramentas: mypy (Python) / TypeScript strict (TS)
```

### 7. Performance & Optimization

```
/optimize-performance

Otimize [ARQUIVO] focando em:

1. ALGORITMOS: Reduza complexidade O(n) quando possível
2. QUERIES: N+1 queries, índices faltantes, eager loading
3. CACHING: Oportunidades de memoização
4. MEMORY: Memory leaks, grandes objetos desnecessários
5. ASYNC: Paralelize quando viável, evite bloqueios

Medir: Benchmark antes/depois (tempo e memória)
Limite: Não sacrifique legibilidade sem ganho > 20%
```

---

## 🤖 Orquestração de Agentes

### Multi-Agent Workflow

```
/orchestrate-improvement

Execute melhorias no [MODULO] com orquestração de agentes:

🔍 AGENT 1 - ANÁLISE:
   - Mapear estrutura e dependências
   - Identificar problemas técnicos
   - Avaliar complexidade

🏗️ AGENT 2 - PLANEJAMENTO:
   - Definir estágios de refatoração
   - Criar plano de testes
   - Documentar trade-offs

💻 AGENT 3 - DESENVOLVIMENTO:
   - Implementar mudanças
   - Passar testes incrementalmente
   - Manter histórico de commits

✅ AGENT 4 - VALIDAÇÃO:
   - Rodar suite completa de testes
   - Executar linters e formatters
   - Validar documentação

📊 AGENT 5 - RELATÓRIO:
   - Sumarizar mudanças
   - Comparar antes/depois
   - Listar impactos potenciais
```

### Agentes Especializados por Stack

#### Backend (Python/FastAPI)
```
/backend-specialist

Agente especialista em backend. Responda com:
- API design best practices
- Async/await patterns
- Database optimization
- Error handling standards
- Dependency injection
```

#### Frontend (TypeScript/React)
```
/frontend-specialist

Agente especialista em frontend. Responda com:
- Component composition
- State management
- Performance optimization
- Accessibility compliance
- Testing strategies
```

#### Infrastructure
```
/infra-specialist

Agente especialista em infraestrutura. Responda com:
- Docker best practices
- CI/CD optimization
- Deployment strategies
- Security hardening
- Monitoring setup
```

---

## 🎓 Workflows Especializados

### Workflow: Preparar PR com Qualidade

```
/prepare-quality-pr

Prepare branch atual para PR seguindo este workflow:

1. /code-analysis
   └─ Executar análise estática completa
   
2. /auto-fix
   └─ Aplicar fixes automáticos (linters, formatters)
   
3. /generate-tests
   └─ Cobrir código novo com testes
   
4. /review-code
   └─ Revisar antes de submeter
   
5. /update-docs
   └─ Documentar mudanças
   
6. /commit-with-message
   └─ Criar commit descritivo com emoji
   └─ Padrão: [type]: descrição (ex: refactor: simplify auth)
```

### Workflow: Onboard Feature Rapidamente

```
/feature-sprint

Execute sprint de feature end-to-end:

Etapa 1: ESPECIFICAÇÃO
  /create-spec
  - Defina requirements
  - Crie cases de uso
  - Mapear dados necessários

Etapa 2: DESIGN
  /design-solution
  - Architecture sketch
  - Database schema
  - API contracts

Etapa 3: IMPLEMENTAÇÃO
  /implement-feature
  - Backend: modelos, serializers, endpoints
  - Frontend: componentes, forms, integração
  - Testes: unitários + integração

Etapa 4: VALIDAÇÃO
  /validate-feature
  - Testes passam
  - Docs atualizados
  - Performance acceptable

Etapa 5: MERGE
  /merge-with-confidence
  - Squash commits se necessário
  - Crie changelog entry
  - Tag release se ready
```

### Workflow: Debug Production Issue

```
/debug-production

Investigue issue em produção sistematicamente:

🔴 ETAPA 1: ISOLAMENTO
  - Obter stack trace/logs completos
  - Replicar localmente
  - Identificar padrão

🟠 ETAPA 2: ROOT CAUSE
  - Trace fluxo de código
  - Examine dados correlatos
  - Valide assumptions

🟡 ETAPA 3: FIX ESTRATÉGICO
  - Solução temporária vs. permanente
  - Backfill dados se necessário
  - Teste exaustivamente

🟢 ETAPA 4: PREVENT
  - Adicione testes que falham com bug
  - Implemente validações
  - Monitor similar issues

🔵 ETAPA 5: POST-MORTEM
  - Document lessons learned
  - Update runbooks
  - Train team
```

---

## 🚨 Troubleshooting

### Quando Claude gera código subótimo

```
⚠️ PROBLEMA: Código muito complexo
SOLUÇÃO:
  /simplify-solution
  - Quebre em funções menores
  - Use abstrações existentes
  - Reduce nesting
  - Add clarifying comments

⚠️ PROBLEMA: Type errors após geração
SOLUÇÃO:
  /fix-types
  - Run type checker
  - Add explicit annotations
  - Check generic constraints
  - Validate discriminated unions

⚠️ PROBLEMA: Testes falhando
SOLUÇÃO:
  /fix-tests
  - Re-run com verbose output
  - Check mock setups
  - Validate test data
  - Add debugger statements
```

### Escalação para AI Engineer Review

```
Quando envolver um AI Engineer:

✓ Complex refactors (> 500 linhas affected)
✓ Performance-critical sections
✓ Security-sensitive code
✓ Architectural changes
✓ Cross-stack coordination needed
✓ CI/CD pipeline modifications

Incluir no PR:
- Design doc (WHY e não apenas WHAT)
- Benchmark results (se performance-critical)
- Deployment plan (se infrastructure change)
- Rollback strategy
```

---

## 📚 Referências Rápidas

### Estrutura do cv_sob_medida
```
cv_sob_medida/
├── backend/           # API Python/FastAPI
├── frontend/          # UI TypeScript/React
├── shared/            # Código compartilhado
├── contracts/         # OpenAPI/GraphQL specs
├── memory/            # Context & memory management
├── .specify/          # Test specifications
└── specs/             # Feature specifications
```

### Comando Rápido: Primeira Execução

```bash
# Clone e setup
git clone <repo>
cd cv_sob_medida

# Setup backend
cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Setup frontend
cd ../frontend && npm install

# Run services
# Terminal 1: cd backend && python main.py
# Terminal 2: cd frontend && npm run dev
```

---

## 🎯 Próximos Passos

1. **Criar `.claude/commands`** para automatizar prompts frequentes
2. **Setup hooks** para validação antes de commits
3. **Documentar CLAUDE.md** com especificidades do projeto
4. **Treinar agentes sub** para funções específicas

---

**Última atualização**: 2025-11-25
**Mantenedor**: @gui-rissatti
