# ✅ Checklist de Teste - CV Sob Medida (Windows)

**Use este checklist para validar a instalação e testes**

---

## 📋 PRÉ-REQUISITOS

- [ ] Python 3.11+ instalado
- [ ] Node.js 20+ instalado
- [ ] Google API Key obtida (https://aistudio.google.com/app/apikey)
- [ ] Projeto clonado/baixado

---

## 🔧 SETUP INICIAL

- [ ] Executado `teste_rapido.bat`
- [ ] Ambiente virtual criado em `backend/.venv/`
- [ ] Dependências Python instaladas
- [ ] Arquivo `backend/.env` criado
- [ ] GOOGLE_API_KEY configurada no .env
- [ ] Validação passou (5/5 checks)

---

## 🧪 TESTES EXECUTADOS

- [ ] `validate_fixes.py` - Passou ✅
- [ ] `test_server.py` - Passou ✅
- [ ] `test_e2e_complete.py` - Passou ✅
- [ ] Arquivo `backend/test_output.json` criado
- [ ] Match score > 80

---

## 🌐 APLICAÇÃO WEB

- [ ] Backend iniciado (porta 8000)
- [ ] Frontend iniciado (porta 5173)
- [ ] Navegador abre em http://localhost:5173
- [ ] Interface carrega sem erros
- [ ] Console do navegador sem erros críticos

---

## 🎯 TESTE MANUAL NA INTERFACE

- [ ] Cole URL de vaga do LinkedIn
- [ ] Configure CV base
- [ ] Clique em "Gerar"
- [ ] Aguarde processamento (~40-60s)
- [ ] CV personalizado é exibido
- [ ] Carta de apresentação é exibida
- [ ] Dicas de networking são exibidas
- [ ] Score de compatibilidade é exibido
- [ ] Pode baixar/copiar os materiais

---

## ✅ VALIDAÇÃO DE QUALIDADE

### Output do Teste E2E

- [ ] Tempo de extração: 15-25s ✅
- [ ] Tempo de geração: 20-35s ✅
- [ ] Tempo total: < 120s ✅
- [ ] CV tem > 1000 caracteres ✅
- [ ] Cover letter tem > 500 caracteres ✅
- [ ] Match score entre 70-100 ✅
- [ ] Keywords da vaga aparecem no CV (> 50%) ✅

### Teste Manual

- [ ] CV menciona o nome da empresa
- [ ] CV está formatado em Markdown
- [ ] Habilidades do candidato foram preservadas
- [ ] Experiências foram adaptadas para a vaga
- [ ] Carta soa natural e personalizada
- [ ] Insights são relevantes

---

## 🐛 TROUBLESHOOTING (se necessário)

### Erros Comuns Resolvidos

- [ ] "Module api not found" → PYTHONPATH configurado
- [ ] "google_api_key not found" → .env configurado
- [ ] "gemini-1.5-flash 404" → Código atualizado para 2.5-flash
- [ ] "Port 8000 in use" → Processo anterior encerrado

---

## 📊 MÉTRICAS REGISTRADAS

| Métrica | Esperado | Obtido | Status |
|---------|----------|--------|--------|
| Tempo extração | < 30s | ___s | [ ] |
| Tempo geração | < 40s | ___s | [ ] |
| Tempo total | < 120s | ___s | [ ] |
| Match score | > 70 | ___ | [ ] |
| CV chars | > 1000 | ___ | [ ] |
| Cover letter chars | > 500 | ___ | [ ] |
| Validações passadas | 6/6 | ___/6 | [ ] |

---

## 📁 ARQUIVOS VERIFICADOS

### Criados/Modificados

- [ ] `backend/.venv/` (diretório)
- [ ] `backend/.env` (configuração)
- [ ] `backend/test_output.json` (resultado teste)
- [ ] `frontend/.env` (configuração)
- [ ] `frontend/node_modules/` (dependências)

### Validados

- [ ] `backend/src/core/config.py` (path absoluto)
- [ ] `backend/src/agents/extraction_agent.py` (gemini-2.5-flash)
- [ ] `backend/src/agents/generation_agent.py` (gemini-2.5-flash)

---

## 🎉 RESULTADO FINAL

### ✅ SUCESSO - Tudo Funcionando

- [ ] Todos os itens acima marcados
- [ ] Scripts batch funcionam
- [ ] Aplicação web funciona
- [ ] Testes passam consistentemente
- [ ] Qualidade dos outputs é boa

**Sistema pronto para uso/deploy!** 🚀

---

### ❌ PENDÊNCIAS

Se algum item falhou, anote aqui:

```
Problema:
_________________________________________________________________

Solução tentada:
_________________________________________________________________

Status:
_________________________________________________________________
```

---

## 📞 AJUDA ADICIONAL

Consulte:
- `QUICKSTART_WINDOWS.md` - Guia passo a passo
- `SCRIPTS_README.md` - Documentação dos scripts
- `DEBUGGING_REPORT.md` - Problemas conhecidos e soluções
- `README.md` - Documentação geral

---

**Data do teste:** ___/___/______  
**Testado por:** _______________________  
**Versão:** _______________________

---

💡 **Dica:** Imprima este checklist para acompanhar seu progresso!
