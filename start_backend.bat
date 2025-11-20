@echo off
REM ====================================================================
REM Iniciar Backend - CV Sob Medida
REM ====================================================================

setlocal

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%backend"

echo.
echo ====================================================================
echo    INICIANDO BACKEND - CV SOB MEDIDA
echo ====================================================================
echo.

REM Verificar ambiente virtual
if not exist ".venv\" (
    echo [ERRO] Ambiente virtual nao encontrado!
    echo Execute primeiro: teste_rapido.bat
    pause
    exit /b 1
)

REM Ativar ambiente virtual
call .venv\Scripts\activate.bat

REM Configurar PYTHONPATH
set "PYTHONPATH=%CD%\src"
echo PYTHONPATH configurado: %PYTHONPATH%
echo.

REM Verificar .env
if not exist ".env" (
    echo [ERRO] Arquivo .env nao encontrado!
    echo Configure sua GOOGLE_API_KEY antes de continuar.
    pause
    exit /b 1
)

echo Iniciando servidor backend na porta 8000...
echo.
echo [CTRL+C para parar o servidor]
echo.
echo ====================================================================
echo.

uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

pause
