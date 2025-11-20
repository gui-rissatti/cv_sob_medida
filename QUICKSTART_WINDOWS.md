# 🚀 Guia de Inicialização Rápida - Windows (Testes Offline)

**Para testar a aplicação localmente sem deploy**

---

## 🎯 MODO SUPER RÁPIDO (1 clique!)

Se você quer testar tudo de uma vez:

1. **Clique duplo em:** `teste_rapido.bat`
2. **Aguarde** a configuração automática
3. **Configure sua API key** quando solicitado
4. **Pronto!** Testes executados automaticamente

**Depois para usar a aplicação:**
- Clique duplo em: `start_app.bat` (abre backend + frontend + navegador)

---

## ⚡ Setup Manual Passo a Passo (5 minutos)

### 1️⃣ Pré-requisitos

Verifique se tem instalado:
```powershell
python --version  # Deve ser 3.11 ou superior
node --version    # Deve ser 20 ou superior
npm --version
```

Se não tiver, baixe:
- **Python:** https://www.python.org/downloads/
- **Node.js:** https://nodejs.org/

---

### 2️⃣ Clone o Repositório

```powershell
cd C:\Users\SEU_USUARIO\Documents
git clone https://github.com/gui-rissatti/cv_sob_medida.git
cd cv_sob_medida
```

---

## 🔧 Configuração Backend (2 minutos)

### Passo 1: Criar Ambiente Virtual

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
```

**Confirmação:** Você deve ver `(.venv)` no início da linha do terminal.

### Passo 2: Instalar Dependências

```powershell
pip install -r requirements.txt
```

### Passo 3: Configurar API Key

```powershell
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env com Notepad
notepad .env
```

**No arquivo .env, substitua:**
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

**Por sua chave real (obter em https://aistudio.google.com/app/apikey):**
```env
GOOGLE_API_KEY=AIzaSy...sua_chave_aqui
```

Salve e feche o Notepad.

---

## 🧪 Executar Testes (1 minuto)

### Teste Rápido de Configuração

```powershell
python validate_fixes.py
```

**Resultado esperado:**
```
✅ Arquivo .env encontrado
✅ GOOGLE_API_KEY configurada
✅ Modelo Gemini correto
✅ API key passada aos agentes
✅ Config usa path absoluto

RESULTADO: 5/5 validações passadas
✅ TODAS AS CORREÇÕES ESTÃO APLICADAS!
```

---

### Teste End-to-End Completo

```powershell
python test_e2e_complete.py
```

**Resultado esperado (demora ~40-60 segundos):**
```
====================================================================
TESTE END-TO-END COMPLETO - CV SOB MEDIDA
====================================================================

[ETAPA 1/4] Verificando saúde do backend...
✅ Backend está saudável e respondendo

[ETAPA 2/4] Extraindo detalhes da vaga do LinkedIn...
✅ Extração concluída em 17.60s

[ETAPA 3/4] Gerando materiais personalizados com IA...
✅ Geração concluída em 25.56s

[ETAPA 4/4] Validando qualidade dos outputs...
✅ CV contém keywords da vaga: 86.7%
✅ CV menciona a empresa: Sim
✅ Match score razoável (>50): 90/100

🎉 TODOS OS TESTES PASSARAM!
```

**📄 O resultado completo fica salvo em:** `backend/test_output.json`

---

## 🌐 Iniciar Aplicação Completa (Opcional)

### 🎯 Método 1: Automático (Recomendado)

**Clique duplo em:** `start_app.bat`

Este script:
- ✅ Inicia backend e frontend automaticamente
- ✅ Abre o navegador
- ✅ Tudo pronto em 10 segundos!

---

### 🔧 Método 2: Manual

Se quiser testar a interface web manualmente:

### Terminal 1 - Backend

**Opção A: Script automatizado**
```powershell
# Clique duplo em:
start_backend.bat
```

**Opção B: Manual**
```powershell
cd backend
.\.venv\Scripts\activate
$env:PYTHONPATH="$PWD\src"
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

**Aguarde ver:** `Uvicorn running on http://127.0.0.1:8000`

### Terminal 2 - Frontend

**Opção A: Script automatizado**
```powershell
# Clique duplo em:
start_frontend.bat
```

**Opção B: Manual**

Abra **outro PowerShell** e execute:

```powershell
cd frontend
npm install  # Só na primeira vez
npm run dev
```

**Aguarde ver:** `Local: http://localhost:5173/`

### Acessar Aplicação

Abra no navegador: **http://localhost:5173**

---

## 🎯 Testar Manualmente na Interface

1. **Cole uma URL de vaga** (ex: LinkedIn, Indeed)
2. **Configure seu CV base** (clique em "Configurar Currículo Base")
3. **Clique em "Gerar"**
4. **Aguarde ~40 segundos**
5. **Veja os materiais gerados:**
   - CV personalizado
   - Carta de apresentação
   - Dicas de networking
   - Score de compatibilidade

---

## 🐛 Resolução de Problemas

### Erro: "Module 'api' not found"

**Solução:**
```powershell
$env:PYTHONPATH="C:\Users\SEU_USUARIO\Documents\cv_sob_medida\backend\src"
```

### Erro: "google_api_key not found"

**Solução:**
1. Verifique se `.env` existe em `backend/`
2. Abra `.env` e confirme que tem sua chave real
3. Execute `python validate_fixes.py` para confirmar

### Erro: "Port 8000 already in use"

**Solução:**
```powershell
# Matar processo usando a porta
netstat -ano | findstr :8000
taskkill /PID <NUMERO_DO_PID> /F
```

### Frontend não conecta ao backend

**Solução:**
```powershell
# Criar arquivo frontend/.env
cd frontend
echo VITE_API_URL=http://localhost:8000 > .env
```

---

## 📊 Scripts de Teste Disponíveis

### Scripts Batch Automatizados (Windows)

| Script | Descrição | Uso |
|--------|-----------|-----|
| `teste_rapido.bat` | **Setup + Testes completos** | Duplo clique |
| `start_app.bat` | **Inicia tudo** (backend+frontend) | Duplo clique |
| `start_backend.bat` | Inicia só o backend | Duplo clique |
| `start_frontend.bat` | Inicia só o frontend | Duplo clique |

### Scripts Python (Para testes específicos)

| Script | Descrição | Tempo |
|--------|-----------|-------|
| `validate_fixes.py` | Valida configuração | ~1s |
| `test_server.py` | Testa health do backend | ~2s |
| `test_integration.py` | Testa com URL real | ~20s |
| `test_e2e_complete.py` | **Teste completo** | ~45s |
| `check_gemini_models.py` | Lista modelos Gemini | ~3s |

---

## 📋 Checklist de Validação

Antes de considerar tudo funcionando, confirme:

- [ ] `validate_fixes.py` passa (5/5)
- [ ] `test_e2e_complete.py` passa (6/6)
- [ ] Arquivo `test_output.json` foi criado
- [ ] Match score > 50 (idealmente > 80)
- [ ] CV gerado tem > 1000 caracteres
- [ ] Tempo total < 120 segundos

---

## 🎓 Dicas de Uso

### Para Testes Rápidos

Use `test_integration.py` - mais rápido que o E2E completo.

### Para Validar Antes de Commit

```powershell
python validate_fixes.py
```

### Para Ver Modelos Gemini Disponíveis

```powershell
python check_gemini_models.py
```

### Para Debug Detalhado

Adicione logs no código e rode com:
```powershell
$env:LOG_LEVEL="DEBUG"
python test_e2e_complete.py
```

---

## 📞 Ajuda Adicional

- **Documentação completa:** `DEBUGGING_REPORT.md`
- **Resumo executivo:** `EXECUTIVE_SUMMARY.md`
- **Troubleshooting:** `README.md`

---

## ✅ Resultado Esperado

Após seguir este guia, você deve ter:

1. ✅ Backend funcionando localmente
2. ✅ Testes E2E passando
3. ✅ CV gerado a partir de vaga real
4. ✅ Score de compatibilidade 80-90+
5. ✅ Aplicação testada e validada

**Tempo total:** ~10-15 minutos ⏱️

---

## 🚀 Próximo Passo

Depois de validar localmente, você pode:
- Fazer modificações no código
- Rodar testes novamente
- Fazer commit das alterações
- Preparar para deploy em produção

**Boa sorte!** 🎉
