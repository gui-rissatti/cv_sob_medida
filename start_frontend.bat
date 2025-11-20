@echo off
REM ====================================================================
REM Iniciar Frontend - CV Sob Medida
REM ====================================================================

setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%frontend"

echo.
echo ====================================================================
echo    INICIANDO FRONTEND - CV SOB MEDIDA
echo ====================================================================
echo.

REM Verificar Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Node.js nao encontrado!
    echo Baixe em: https://nodejs.org/
    pause
    exit /b 1
)

REM Verificar se node_modules existe
if not exist "node_modules\" (
    echo Instalando dependencias do frontend...
    echo (isso pode demorar alguns minutos na primeira vez)
    echo.
    call npm install
    if errorlevel 1 (
        echo [ERRO] Falha ao instalar dependencias!
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencias instaladas
    echo.
)

REM Verificar/criar .env
if not exist ".env" (
    echo Criando arquivo .env...
    echo VITE_API_URL=http://localhost:8000 > .env
    echo [OK] Arquivo .env criado
    echo.
)

echo Iniciando servidor frontend na porta 5173...
echo.
echo Apos iniciar, acesse: http://localhost:5173
echo.
echo [CTRL+C para parar o servidor]
echo.
echo ====================================================================
echo.

npm run dev

pause
