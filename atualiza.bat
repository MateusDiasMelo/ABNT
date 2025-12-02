@echo off
setlocal enabledelayedexpansion

REM ===== CONFIGURAÇÕES =====
set FRONTEND_DIR=C:\Users\User\ABNT\frontend
set SERVER_USER=root
set SERVER_HOST=69.6.222.172
set SERVER_PORT=22022
set SERVER_FRONTEND_PATH=/var/www/abntx_frontend

echo ============================================
echo   DEPLOY ABNTX - FRONTEND + BACKEND
echo ============================================
echo.

pause

REM ===== FRONTEND: BUILD =====
echo [1/4] Indo para pasta do frontend: %FRONTEND_DIR%
cd /d "%FRONTEND_DIR%"
if errorlevel 1 (
    echo ERRO: Não consegui acessar %FRONTEND_DIR%
    pause
    exit /b 1
)

pause

echo [2/4] Instalando dependencias (npm install)...
npm install
if errorlevel 1 (
    echo ERRO no npm install
    pause
    exit /b 1
)

pause

echo [3/4] Gerando build (npm run build)...
npm run build
if errorlevel 1 (
    echo ERRO no npm run build
    pause
    exit /b 1
)

pause

if not exist "%FRONTEND_DIR%\dist" (
    echo ERRO: pasta dist nao encontrada apos o build.
    pause
    exit /b 1
)

echo.
echo ===== LIMPANDO FRONTEND ANTIGO NO SERVIDOR =====
ssh -p %SERVER_PORT% %SERVER_USER%@%SERVER_HOST% "rm -rf %SERVER_FRONTEND_PATH%/*"

pause

echo ===== ENVIANDO NOVO FRONTEND =====
scp -P %SERVER_PORT% -r "%FRONTEND_DIR%\dist\*" %SERVER_USER%@%SERVER_HOST%:%SERVER_FRONTEND_PATH%

pause

echo ===== ATUALIZANDO BACKEND NO SERVIDOR =====
ssh -p %SERVER_PORT% %SERVER_USER%@%SERVER_HOST% "/root/deploy_abntx.sh"

pause

echo ============================================
echo   DEPLOY CONCLUIDO COM SUCESSO! 🎉
echo   Site: https://abntx.com.br
echo ============================================

pause
