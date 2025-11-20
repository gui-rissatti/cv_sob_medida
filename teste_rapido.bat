@echo off
REM ====================================================================
REM Script de Teste Rápido - CV Sob Medida
REM ====================================================================
REM Este script automatiza o setup e execução de testes no Windows
REM ====================================================================

setlocal EnableDelayedExpansion

echo.
echo ====================================================================
echo    CV SOB MEDIDA - TESTE RAPIDO AUTOMATIZADO
echo ====================================================================
echo.

REM Detectar diretório do script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Verificar se estamos no diretório correto
if not exist "backend\" (
    echo [ERRO] Diretorio backend nao encontrado!
    echo Execute este script a partir do diretorio raiz do projeto.
    pause
    exit /b 1
)

echo [1/5] Verificando pre-requisitos...
echo ====================================================================

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Baixe em: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python instalado

REM Verificar ambiente virtual
if not exist "backend\.venv\" (
    echo [AVISO] Ambiente virtual nao encontrado. Criando...
    cd backend
    python -m venv .venv
    cd ..
    echo [OK] Ambiente virtual criado
) else (
    echo [OK] Ambiente virtual encontrado
)

echo.
echo [2/5] Ativando ambiente virtual e instalando dependencias...
echo ====================================================================

cd backend

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Verificar se requirements.txt existe
if not exist "requirements.txt" (
    echo [ERRO] requirements.txt nao encontrado!
    pause
    exit /b 1
)

REM Instalar dependências (silenciosamente, só mostra erros)
echo Instalando dependencias... (pode demorar alguns minutos)
pip install -q -r requirements.txt 2>&1 | findstr /i "error failed"
if errorlevel 1 (
    echo [OK] Dependencias instaladas
) else (
    echo [AVISO] Alguns pacotes podem ter falhado
)

echo.
echo [3/5] Verificando configuracao...
echo ====================================================================

REM Verificar .env
if not exist ".env" (
    echo [AVISO] Arquivo .env nao encontrado!
    if exist ".env.example" (
        echo Copiando .env.example para .env...
        copy .env.example .env >nul
        echo.
        echo [ATENCAO] Configure sua GOOGLE_API_KEY no arquivo .env
        echo           Abra o arquivo backend\.env e adicione sua chave
        echo           Obtenha em: https://aistudio.google.com/app/apikey
        echo.
        echo Pressione qualquer tecla apos configurar...
        pause >nul
    ) else (
        echo [ERRO] .env.example tambem nao encontrado!
        pause
        exit /b 1
    )
)

REM Executar script de validação
echo Validando configuracao...
python validate_fixes.py
if errorlevel 1 (
    echo.
    echo [ERRO] Validacao falhou!
    echo Revise o arquivo .env e certifique-se de ter configurado a API key.
    pause
    exit /b 1
)

echo.
echo [4/5] Executando teste basico...
echo ====================================================================

python test_server.py
if errorlevel 1 (
    echo [ERRO] Teste basico falhou!
    pause
    exit /b 1
)

echo.
echo [5/5] Executando teste completo end-to-end...
echo ====================================================================
echo [AVISO] Este teste pode demorar 40-60 segundos...
echo.

python test_e2e_complete.py
set TEST_RESULT=!errorlevel!

echo.
echo ====================================================================
echo    RESULTADO FINAL
echo ====================================================================

if !TEST_RESULT! equ 0 (
    echo.
    echo  [32m *** SUCESSO! TODOS OS TESTES PASSARAM! *** [0m
    echo.
    echo  O resultado completo foi salvo em: backend\test_output.json
    echo.
    echo  Proximos passos:
    echo    1. Para iniciar o backend: start_backend.bat
    echo    2. Para iniciar o frontend: start_frontend.bat
    echo    3. Acesse: http://localhost:5173
    echo.
) else (
    echo.
    echo  [31m *** FALHA! ALGUNS TESTES NAO PASSARAM! *** [0m
    echo.
    echo  Verifique os erros acima e:
    echo    1. Confirme que a GOOGLE_API_KEY esta correta no .env
    echo    2. Verifique sua conexao com a internet
    echo    3. Rode novamente: teste_rapido.bat
    echo.
)

echo ====================================================================
echo.
pause
exit /b !TEST_RESULT!
