# 🎯 Scripts de Inicialização Rápida - Windows

## 📦 Scripts Disponíveis

### 1️⃣ `teste_rapido.bat` - Setup e Testes Automáticos
**O que faz:**
- ✅ Verifica Python instalado
- ✅ Cria ambiente virtual (se não existir)
- ✅ Instala dependências
- ✅ Configura .env
- ✅ Valida configuração
- ✅ Executa teste end-to-end completo

**Como usar:**
```
Duplo clique no arquivo teste_rapido.bat
```

**Quando usar:**
- Primeira vez configurando o projeto
- Após fazer mudanças no código
- Para validar que tudo está funcionando

---

### 2️⃣ `start_app.bat` - Iniciar Aplicação Completa
**O que faz:**
- ✅ Inicia backend (porta 8000)
- ✅ Inicia frontend (porta 5173)
- ✅ Abre navegador automaticamente

**Como usar:**
```
Duplo clique no arquivo start_app.bat
```

**Quando usar:**
- Para usar a aplicação web completa
- Depois de ter executado teste_rapido.bat com sucesso

---

### 3️⃣ `start_backend.bat` - Apenas Backend
**O que faz:**
- ✅ Ativa ambiente virtual
- ✅ Configura PYTHONPATH
- ✅ Inicia servidor FastAPI na porta 8000

**Como usar:**
```
Duplo clique no arquivo start_backend.bat
```

**Quando usar:**
- Para testar apenas a API
- Para desenvolver o backend

---

### 4️⃣ `start_frontend.bat` - Apenas Frontend
**O que faz:**
- ✅ Instala dependências npm (primeira vez)
- ✅ Configura .env
- ✅ Inicia servidor Vite na porta 5173

**Como usar:**
```
Duplo clique no arquivo start_frontend.bat
```

**Quando usar:**
- Para desenvolver o frontend
- Backend já está rodando separadamente

---

## 🚀 Fluxo Recomendado

### Primeira Vez

1. **Duplo clique em:** `teste_rapido.bat`
2. **Configure API key** quando solicitado
3. **Aguarde testes** passarem
4. **Pronto!** ✅

### Uso Diário

1. **Duplo clique em:** `start_app.bat`
2. **Aguarde** ~10 segundos
3. **Navegador abre automaticamente** em http://localhost:5173
4. **Use a aplicação!** 🎉

---

## 🔧 Requisitos

Antes de usar os scripts, certifique-se de ter:

- ✅ **Python 3.11+** - https://www.python.org/downloads/
- ✅ **Node.js 20+** - https://nodejs.org/
- ✅ **Google API Key** - https://aistudio.google.com/app/apikey

---

## 📋 O que cada script cria/modifica

| Script | Cria/Modifica |
|--------|---------------|
| `teste_rapido.bat` | `backend/.venv/`, `backend/.env` (se não existir) |
| `start_backend.bat` | Nada (só usa arquivos existentes) |
| `start_frontend.bat` | `frontend/node_modules/`, `frontend/.env` |
| `start_app.bat` | Nada (apenas chama outros scripts) |

---

## 🐛 Problemas Comuns

### "Python não encontrado"
**Solução:** Instale Python 3.11+ de https://www.python.org/downloads/

### "Node não encontrado"
**Solução:** Instale Node.js 20+ de https://nodejs.org/

### "google_api_key not found"
**Solução:** 
1. Abra `backend\.env`
2. Substitua `your_gemini_api_key_here` pela sua chave real
3. Obtenha em: https://aistudio.google.com/app/apikey

### "Port 8000 already in use"
**Solução:**
```powershell
netstat -ano | findstr :8000
taskkill /PID <NUMERO> /F
```

---

## 📖 Documentação Completa

Para instruções detalhadas, veja:
- **Windows:** `QUICKSTART_WINDOWS.md`
- **Geral:** `README.md`
- **Debugging:** `DEBUGGING_REPORT.md`

---

## ✅ Validação

Após executar `teste_rapido.bat`, você deve ver:

```
====================================================================
   RESULTADO FINAL
====================================================================

 *** SUCESSO! TODOS OS TESTES PASSARAM! ***

 O resultado completo foi salvo em: backend\test_output.json

 Proximos passos:
   1. Para iniciar o backend: start_backend.bat
   2. Para iniciar o frontend: start_frontend.bat
   3. Acesse: http://localhost:5173

====================================================================
```

---

## 🎓 Dicas

💡 **Para debug:** Abra os scripts .bat com um editor de texto para ver/modificar comandos

💡 **Logs:** Os scripts mostram mensagens coloridas (verde=sucesso, vermelho=erro)

💡 **Para parar servidores:** Pressione `CTRL+C` na janela do script

💡 **Múltiplas execuções:** Pode rodar `teste_rapido.bat` quantas vezes quiser

---

**Criado para facilitar testes offline no Windows!** 🚀
