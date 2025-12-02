@echo off
setlocal enabledelayedexpansion

REM ===== CONFIGURAÇÕES =====
set FRONTEND_DIR=C:\Users\User\ABNT\frontend
set SERVER_USER=root
set SERVER_HOST=69.6.222.172
set SERVER_PORT=22022
set SERVER_FRONTEND_PATH=/var/www/abntx_frontend

echo ============================================
echo       DEPLOY ABNTX - FRONTEND + BACKEND
echo ============================================
echo.

echo [1/6] Verificando pasta do frontend...
if not exist "%FRONTEND_DIR%" (
    echo ERRO: pasta do frontend nao encontrada!
    pause
    exit /b
)
cd /d "%FRONTEND_DIR%"

echo [2/6] Instalando dependencias (npm install)...
call npm install
echo (OK)

echo [3/6] Gerando build (npm run build)...
call npm run build
if not exist "%FRONTEND_DIR%\dist" (
    echo ERRO: build NAO gerado!
    pause
    exit /b
)

echo [4/6] Limpando frontend antigo no servidor...
ssh -p %SERVER_PORT% %SERVER_USER%@%SERVER_HOST% "rm -rf %SERVER_FRONTEND_PATH%/*"

echo [5/6] Enviando novo build...
scp -P %SERVER_PORT% -r "%FRONTEND_DIR%\dist\*" %SERVER_USER%@%SERVER_HOST%:%SERVER_FRONTEND_PATH%/
if errorlevel 1 (
    echo ERRO ao enviar arquivos para o servidor!
    pause
    exit /b
)

echo [6/6] Atualizando backend...
ssh -p %SERVER_PORT% %SERVER_USER%@%SERVER_HOST% "bash /root/deploy_abntx.sh"

echo.
echo ============================================
echo   DEPLOY FINALIZADO COM SUCESSO! 🎉
echo ============================================
pause
