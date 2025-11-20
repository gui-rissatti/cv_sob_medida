@echo off
REM ====================================================================
REM Iniciar Aplicacao Completa - CV Sob Medida
REM ====================================================================
REM Este script inicia backend e frontend em janelas separadas
REM ====================================================================

echo.
echo ====================================================================
echo    CV SOB MEDIDA - INICIALIZACAO COMPLETA
echo ====================================================================
echo.
echo Abrindo backend e frontend em janelas separadas...
echo.

REM Iniciar backend em nova janela
start "CV Sob Medida - Backend" cmd /k "%~dp0start_backend.bat"

REM Aguardar 5 segundos para backend iniciar
echo Aguardando backend iniciar...
timeout /t 5 /nobreak >nul

REM Iniciar frontend em nova janela
start "CV Sob Medida - Frontend" cmd /k "%~dp0start_frontend.bat"

echo.
echo ====================================================================
echo    SERVIDORES INICIADOS
echo ====================================================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Duas janelas foram abertas. Nao feche-as enquanto usa a aplicacao.
echo.
echo Para parar os servidores: Pressione CTRL+C em cada janela
echo.
echo ====================================================================
echo.

REM Aguardar mais 3 segundos e abrir navegador
timeout /t 3 /nobreak >nul
start http://localhost:5173

echo Navegador aberto!
echo.
pause
